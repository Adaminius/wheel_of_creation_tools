import re
from statblock import Statblock
from utils import Action
from utils import process_operands
from utils import Dice


class Tag(object):
    def __init__(self, name, effect_text):
        self.name = name
        self.effect_text = effect_text

    def __repr__(self):
        return 'Tag<name="{}", effect_text="{}">'.format(self.name, self.effect_text)

    @classmethod
    def from_table_line(cls, line: str):
        """e.g. |too many eyes|increase Perception skill by 2 * proficiency|"""
        _, name, effect_text = line[1:][:-1].split('|')
        return cls(name=name, effect_text=effect_text)

    @staticmethod
    def normalize_key(key: str, values: dict) -> str:
        # original_key = key
        key = key.strip().lower().replace(' ', '_')

        if key == 'hp':
            return 'hit_points'
        if key == 'ac':
            return 'armor_class'
        if key == 'ac_type':
            return 'armor_class_type'
        if key == 'legendary_actions':
            return 'num_legendary'

        # if key in values.keys():
        return key

        # return original_key.strip()

    def apply(self, block: Statblock) -> Statblock:
        """Return a new Statblock with effects of this tag applied."""
        effects = [e.strip() for e in self.effect_text.split(';')]
        new_block = Statblock(**block.to_dict())

        for effect in effects:
            values = new_block.to_dict()

            print(new_block.skills)

            # ----  Number-like tag operations  ---- #
            inc_dec_search = re.search(r'(increase|decrease)\s+\b(.*)\s*by\s*(.*)', effect)
            if inc_dec_search:
                new_block = self.inc_or_dec(values, inc_dec_search)
                continue

            set_search = re.search(r'(set)\s+\b(.*)\s*to\s*(.*)', effect)
            if set_search:
                new_block = self.set(values, set_search)
                continue

            reset_search = re.search(r'(reset)\s+\b(.*)', effect)
            if reset_search:
                new_block = self.reset(values, reset_search)
                continue

            # ----  List-like tag operations    ---- #
            add_bps_search = re.search(r'add\s+(resistance|immunity|vulnerability)\s+to\s+bludgeoning,\s+piercing,*'
                                       r'\s+and\s+slashing\s+damage\s+from\s+(.*)', effect)
            if add_bps_search:
                new_block = self.add_bps(values, add_bps_search)
                continue

            remove_bps_search = re.search(r'remove\s+(resistance|immunity|vulnerability)\s+to\s+bludgeoning,\s+piercing,*'
                                       r'\s+and\s+slashing\s+damage\s+from\s+(.*)', effect)
            if remove_bps_search:
                new_block = self.remove_bps(values, remove_bps_search)
                continue

            add_vuln_search = re.search(r'add\s+(resistance|immunity|vulnerability)\s+to\s+(.*)\s+damage', effect)
            if add_vuln_search:
                new_block = self.add_vuln_res_immun(values, add_vuln_search)
                continue

            remove_vuln_search = re.search(r'remove\s+(resistance|immunity|vulnerability)\s+to\s+(.*)\s+damage', effect)
            if remove_vuln_search:
                new_block = self.remove_vuln_res_immun(values, remove_vuln_search)
                continue

            add_cond_search = re.search('add\s+immunity\s+to\s+(.*)', effect)
            if add_cond_search:
                new_block = self.add_cond(values, add_cond_search)
                continue

            remove_cond_search = re.search('add\s+immunity\s+to\s+(.*)', effect)
            if remove_cond_search:
                new_block = self.remove_cond(values, add_cond_search)
                continue

            clear_search = re.search(r'clear\s+(condition immunities|damage immunities|damage resistances|'
                                     r'damage vulnerabilities|abilities|actions|bonus actions|reactions|'
                                     r'legendary actions)', effect)
            if clear_search:
                new_block = self.clear_listlike(values, clear_search)
                continue

            add_lang_search = re.search(r'add\s+language\s+(.*)', effect)
            if add_lang_search:
                new_block = self.add_lang(values, add_lang_search)
                continue

            add_ability_search = re.search(r'add\s+ability(.*):\s+(.*)', effect)
            if add_ability_search:
                new_block = self.add_action_or_ability(values, add_ability_search, 'abilities')
                continue

            add_action_search = re.search(r'add\s+action(.*):\s+(.*)', effect)
            if add_action_search:
                new_block = self.add_action_or_ability(values, add_action_search, 'actions')
                continue

            add_bonus_action_search = re.search(r'add\s+bonus\s+action(.*):\s+(.*)', effect)
            if add_bonus_action_search:
                new_block = self.add_action_or_ability(values, add_bonus_action_search, 'bonus_actions')
                continue

            add_reaction_search = re.search(r'add\s+reaction(.*):\s+(.*)', effect)
            if add_ability_search:
                new_block = self.add_action_or_ability(values, add_reaction_search, 'reactions')
                continue

            add_legendary_action_search = re.search(r'add\s+legendary\s+action(.*):\s+(.*)', effect)
            if add_legendary_action_search:
                new_block = self.add_action_or_ability(values, add_legendary_action_search, 'legendary_actions')
                continue

            set_alignment_search = re.search(r'(.*)-aligned', effect)
            if set_alignment_search:
                new_block = self.set_alignment(values, set_alignment_search)
                continue

            print('Could not parse "{}"'.format(effect))

        new_block.calc_challenge()
        return new_block

    def inc_or_dec(self, values: dict, search_result) -> Statblock:
        inc_or_dec, key, operands = search_result.groups()

        inc_or_dec = -1 if inc_or_dec == 'decrease' else 1

        key = self.normalize_key(key, values)
        operands = process_operands(operands.split(), values)

        if key in values.keys():
            values[key] += inc_or_dec * operands
        elif key[:3].upper() in values.get('ability_scores', {}).keys():
            values['ability_scores'][key[:3].upper()].value += inc_or_dec * operands
        elif key in values.get('skills', {}).keys():
            values['skills'][key] += inc_or_dec * operands
        elif key in values.get('saving_throws', {}).keys():
            values['skills'][key] += inc_or_dec * operands
        else:
            values[key] = values.get(key, 0) + inc_or_dec * operands
        # else:
        #     raise KeyError('Unrecognized key "{}" for operation "increase/decrease".'.format(key))

        return Statblock(**values)

    def set(self, values: dict, search) -> Statblock:
        _, key, operands = search.groups()
        key = self.normalize_key(key, values)

        if key == 'type':
            types = operands.split('(')
            if len(types) == 1:
                values['primary_type'] = operands
            else:
                values['primary_type'] = types[0].strip()
                values['secondary_type'] = types[1].strip().strip(')').strip()

            return Statblock(**values)

        if key == 'hit_dice':
            values['hit_dice'] = Dice.from_string(operands.strip())
            return Statblock(**values)

        operands = process_operands(operands.split(), values)

        if key in values.keys():
            values[key] = operands
        elif key[:3].upper() in values.get('ability_scores', {}).keys():
            values['ability_scores'][key[:3].upper()].value = operands
        elif key in values.get('skills', {}).keys():
            values['skills'][key] = operands
        elif key in values.get('saving_throws', {}).keys():
            values['skills'][key] = operands
        elif key == 'hit_point_bonus':
            values['hit_point_bonus'] = operands
        else:
            raise KeyError('Unrecognized key "{}" for operation "set".'.format(key))

        return Statblock(**values)

    def reset(self, values: dict, search) -> Statblock:
        _, key = search.groups()
        key = self.normalize_key(key, values)

        if key == 'hit_points':
            new_block = Statblock(**values)
            new_block.calc_hit_points()
            return new_block

        raise KeyError('Unrecognized key "{}" for operation "reset".'.format(key))

    def add_bps(self, values: dict, search) -> Statblock:
        field, key = search.groups()

        full_key = 'bludgeoning, piercing, and slashing damage from {}'.format(key)

        vuln_set = set(values.get('damage_vulnerabilities', []))
        res_set = set(values.get('damage_resistances', []))
        immun_set = set(values.get('damage_immunities', []))

        if field == 'vulnerability':
            for vuln in list(vuln_set):
                if 'bludg' in vuln:
                    vuln_set.remove(vuln)
            for res in list(res_set):
                if 'bludg' in res:
                    res_set.remove(res)
            for imm in list(immun_set):
                if 'bludg' in immun_set:
                    immun_set.remove(imm)
            vuln_set.add(full_key)
            values['damage_vulnerabilities'] = list(vuln_set)
            values['damage_resistances'] = list(res_set)
            values['damage_immunities'] = list(immun_set)

        elif field == 'resistance':
            already_immune = False
            for imm in list(immun_set):
                if key in imm:
                    already_immune = True
                    break
                if 'bludg' in imm:
                    immun_set.remove(imm)
            for vuln in list(vuln_set):
                if 'bludg' in vuln:
                    vuln_set.remove(vuln)
            for res in list(res_set):
                if already_immune:
                    break
                if 'bludg' in res:
                    res_set.remove(res)
            if not already_immune:
                res_set.add(full_key)
            values['damage_vulnerabilities'] = list(vuln_set)
            values['damage_resistances'] = list(res_set)
            values['damage_immunities'] = list(immun_set)

        else:
            for vuln in list(vuln_set):
                if 'bludg' in vuln:
                    vuln_set.remove(vuln)
            for res in list(res_set):
                if 'bludg' in res:
                    res_set.remove(res)
            for imm in list(immun_set):
                if 'bludg' in immun_set:
                    immun_set.remove(imm)
            immun_set.add(full_key)
            values['damage_vulnerabilities'] = list(vuln_set)
            values['damage_resistances'] = list(res_set)
            values['damage_immunities'] = list(immun_set)

        return Statblock(**values)

    def remove_bps(self, values: dict, search) -> Statblock:
        field, key = search.groups()

        vuln_set = set(values.get('damage_vulnerabilities', []))
        res_set = set(values.get('damage_resistances', []))
        immun_set = set(values.get('damage_immunities', []))

        if field == 'vulnerability':
            for vuln in list(vuln_set):
                if 'bludg' in vuln:
                    if key in vuln:
                        vuln_set.remove(vuln)
        elif field == 'resistance':
            for res in list(res_set):
                if 'bludg' in res:
                    if key in res:
                        res_set.remove(res)
        else:
            for imm in list(immun_set):
                if 'bludg' in imm:
                    if key in imm:
                        immun_set.remove(imm)

        values['damage_vulnerabilities'] = list(vuln_set)
        values['damage_resistances'] = list(res_set)
        values['damage_immunities'] = list(immun_set)

        return Statblock(**values)

    def add_vuln_res_immun(self, values: dict, search) -> Statblock:
        field, keys = search.groups()

        if 'bludgeoning, piercing, and slashing da' in keys:
            bps = 'bludgeoning, piercing, and slashing da' + keys.split('bludgeoning, piercing, and slashing da')[-1]
            keys = keys.split('bludgeoning, piercing, and slashing da')[0].split(',') + [bps]
        else:
            keys = keys.split(',')

        keys = [key.strip() for key in keys if key.strip()]

        vuln_set = set(values.get('damage_vulnerabilities', []))
        res_set = set(values.get('damage_resistances', []))
        immun_set = set(values.get('damage_immunities', []))

        if field == 'vulnerability':
            for key in keys:
                vuln_set.add(key)
                if key in res_set:
                    res_set.remove(key)
                if key in immun_set:
                    immun_set.remove(key)
            values['damage_vulnerabilities'] = list(vuln_set)
            values['damage_resistances'] = list(res_set)
            values['damage_immunities'] = list(immun_set)

        elif field == 'resistance':
            for key in keys:
                if key in immun_set:
                    pass
                elif key in vuln_set:
                    vuln_set.remove(key)
                    res_set.add(key)
                else:
                    res_set.add(key)
            values['damage_vulnerabilities'] = list(vuln_set)
            values['damage_resistances'] = list(res_set)
            values['damage_immunities'] = list(immun_set)

        else:
            for key in keys:
                immun_set.add(key)
                if key in vuln_set:
                    vuln_set.remove(key)
                if key in res_set:
                    res_set.remove(key)
            values['damage_vulnerabilities'] = list(vuln_set)
            values['damage_resistances'] = list(res_set)
            values['damage_immunities'] = list(immun_set)

        return Statblock(**values)

    def remove_vuln_res_immun(self, values: dict, search) -> Statblock:
        field, keys = search.groups()

        if 'bludgeoning, piercing, and slashing da' in keys:
            bps = 'bludgeoning, piercing, and slashing da' + keys.split('bludgeoning, piercing, and slashing da')[-1]
            keys = keys.split('bludgeoning, piercing, and slashing da')[0].split(',') + [bps]
        else:
            keys = keys.split(',')

        keys = [key.strip() for key in keys if key.strip()]

        vuln_set = set(values.get('damage_vulnerabilities', []))
        res_set = set(values.get('damage_resistances', []))
        immun_set = set(values.get('damage_immunities', []))

        if field == 'vulnerability':
            for key in keys:
                vuln_set.remove(key)
        elif field == 'resistance':
            for key in keys:
                res_set.remove(key)
        else:
            for key in keys:
                immun_set.remove(key)

        values['damage_vulnerabilities'] = list(vuln_set)
        values['damage_resistances'] = list(res_set)
        values['damage_immunities'] = list(immun_set)

        return Statblock(**values)

    def clear_listlike(self, values: dict, search):
        field = search.groups()[0]

        if field == 'condition immunities':
            values['condition_immunities'] = []
        elif field == 'damage immunities':
            values['damage_immunities'] = []
        elif field == 'damage vulnerabilities':
            values['damage_vulnerabilities'] = []
        else:
            values['damage_resistances'] = []

        return Statblock(**values)

    def add_cond(self, values: dict, search):
        keys = [k.strip() for k in search.groups()[0].split(',') if k.strip()]
        cond_set = set(values.get('condition_immunities', []))

        for key in keys:
            cond_set.add(key)

        values['condition_immunities'] = list(cond_set)

        return Statblock(**values)

    def remove_cond(self, values: dict, search):
        keys = [k.strip() for k in search.groups()[0].split(',') if k.strip()]
        cond_set = set(values.get('condition_immunities', []))

        for key in keys:
            cond_set.remove(key)

        values['condition_immunities'] = list(cond_set)

        return Statblock(**values)

    def add_lang(self, values: dict, search):
        key = search.groups()[0].strip()
        lang_set = set(values['languages'])
        lang_set.add(key)
        values['languages'] = list(lang_set)

        return Statblock(**values)

    def add_action_or_ability(self, values: dict, search, which):
        action_name, action_effect = search.groups()

        if which.startswith('legen'):
            is_legendary = True
        else:
            is_legendary = False

        if values.get(which) is not None:
            values[which].append(Action(action_name, description_template=action_effect, is_legendary=is_legendary))

        return Statblock(**values)

    def clear_actions_or_abilities(self, values: dict, which):
        values[which] = []
        return Statblock(**values)

    def set_alignment(self, values: dict, search):
        new_alignment = search.groups()[0]
        values['alignment'] = new_alignment.strip()
        return Statblock(**values)

def read_tag_table(text: str) -> list:
    tags = []
    for line in text.splitlines()[2:]:
        tags.append(Tag.from_table_line(line))
    return tags
