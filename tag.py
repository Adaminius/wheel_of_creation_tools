import re
from statblock import Statblock
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
        original_key = key
        key = key.strip().lower().replace(' ', '_')

        if key == 'hp':
            return 'hit_points'
        if key == 'ac':
            return 'armor_class'
        if key == 'ac_type':
            return 'armor_class_type'

        if key in values.keys():
            return key

        return original_key.strip()

    @staticmethod
    def process_operands(operands: list, values: dict):
        total = 0
        next_mul = 1
        for operand in operands:
            operand = operand.replace('ft.', '').strip()

            if operand == '':
                continue

            if operand == '+':
                next_mul = 1
                continue

            if operand == '-':
                next_mul = -1
                continue

            try:
                total += int(operand)
                continue
            except ValueError:
                pass

            if re.search(r'\d*d\d+', operand):
                total += Dice.from_string(operand).roll() * next_mul
                next_mul = 1
                continue

            if operand in values.keys():
                total += values[operand]
                continue

            if 'ability_scores' in values.keys():
                if operand in values['ability_scores'].keys():
                    total += values['ability_scores'][operand].modifier * next_mul
                    next_mul = 1
                    continue
                if operand[:3].upper() in values['ability_scores'].keys():
                    total += values['ability_scores'][operand].value * next_mul
                    next_mul = 1
                    continue

            if 'skills' in values.keys():
                if operand in values['skills'].keys():
                    total += values['skills'][operand] * next_mul
                    next_mul = 1
                    continue

            raise RuntimeError('Couldn\'t parse operand {} of operands {}'.format(operand, operands))

        return total

    def apply(self, block: Statblock) -> Statblock:
        """Return a new Statblock with effects of this tag applied."""
        effects = [e.strip() for e in self.effect_text.split(';')]
        new_block = Statblock(**block.to_dict())

        for effect in effects:
            values = new_block.to_dict()

            # ----  Number-like tag operations  ---- #
            inc_dec_search = re.search(r'\b(increase|decrease)\b\s*\b(.*)\s*by\s*(.*)', effect)
            if inc_dec_search:
                new_block = self.inc_or_dec(values, inc_dec_search)
                continue

            set_search = re.search(r'\b(set)\b\s*\b(.*)\s*to\s*(.*)', effect)
            if set_search:
                new_block = self.set(values, set_search)
                continue

            reset_search = re.search(r'\b(reset)\b\s*\b(.*)', effect)
            if reset_search:
                new_block = self.reset(values, reset_search)
                continue

            # ----  List-like tag operations    ---- #
            # Damage vulnerability, resistance, immunity
            # |clear damage resistances|remove all damage resistances|
            # |add resistance to foo, bar damage|adds "foo" and "bar" to damage resistances, and removes them from vulnerabilities|
            # |add immunity to foo, bar damage|adds "foo" and "bar" to damage immunities, removes them from resist/vuln|
            # |add vulnerability to foo, bar damage|adds "foo" and "bar" to damage vulnerabilities, removes from resist/immune|
            # |remove vulnerability to foo, bar damage||
            # |add resistance to bludgeoning, piercing, and slashing damage from...|special case for resist/immune/vulnerable|
            # |add immunity to foo, bar|adds "foo" and "bar" to condition immunities|

            add_vuln_search = re.search(r'\badd\s+(resistance|immunity|vulnerability)\s+to\s+(.*)\s+damage', effect)
            if add_vuln_search:
                new_block = self.add_vuln_res_immun(values, add_vuln_search)
                continue

            # Other tag operations

        new_block.calc_challenge()
        return new_block

    def inc_or_dec(self, values: dict, search_result) -> Statblock:
        inc_or_dec, key, operands = search_result.groups()

        inc_or_dec = -1 if inc_or_dec == 'decrease' else 1

        key = self.normalize_key(key, values)
        operands = self.process_operands(operands.split(), values)

        if key in values.keys():
            values[key] += inc_or_dec * operands
        elif key[:3].upper() in values.get('ability_scores', {}).keys():
            values['ability_scores'][key[:3].upper()].value += inc_or_dec * operands
        elif key in values.get('skills', {}).keys():
            values['skills'][key] += inc_or_dec * operands
        elif key in values.get('saving_throws', {}).keys():
            values['skills'][key] += inc_or_dec * operands
        else:
            raise KeyError('Unrecognized key "{}" for operation "increase/decrease".'.format(key))

        return Statblock(**values)

    def set(self, values: dict, search) -> Statblock:
        _, key, operands = search.groups()
        key = self.normalize_key(key, values)
        operands = self.process_operands(operands.split(), values)

        if key in values.keys():
            values[key] = operands
        elif key[:3].upper() in values.get('ability_scores', {}).keys():
            values['ability_scores'][key[:3].upper()].value = operands
        elif key in values.get('skills', {}).keys():
            values['skills'][key] = operands
        elif key in values.get('saving_throws', {}).keys():
            values['skills'][key] = operands
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

    # Damage vulnerability, resistance, immunity
    # |clear damage resistances|remove all damage resistances|
    # |add resistance to foo, bar damage|adds "foo" and "bar" to damage resistances, and removes them from vulnerabilities|
    # |add immunity to foo, bar damage|adds "foo" and "bar" to damage immunities, removes them from resist/vuln|
    # |add vulnerability to foo, bar damage|adds "foo" and "bar" to damage vulnerabilities, removes from resist/immune|
    # |remove vulnerability to foo, bar damage||
    # |add resistance to bludgeoning, piercing, and slashing damage from...|special case for resist/immune/vulnerable|
    # |add immunity to foo, bar|adds "foo" and "bar" to condition immunities|

    # add_vul_search = re.search(r'\badd\s+(resistance|immunity|vulnerability)\s+to\s+(.*)\s+damage', effect)

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

        print(values['damage_resistances'])
        print('foo')

        return Statblock(**values)


def read_tag_table(text: str) -> list:
    tags = []
    for line in text.splitlines()[2:]:
        tags.append(Tag.from_table_line(line))
    return tags

    #
    # def __init__(self, name: str = None, size: str = 'Medium', primary_type: str = 'Humanoid',
    #              secondary_type: str = '',
    #              alignment: str = 'Chaotic Evil', armor_class: int = 10, armor_class_type: str = '',
    #              hit_points: int = None, hit_point_bonus: int = 0, hit_dice: Dice = None, speed: int = 30,
    #              climb_speed: int = 0,
    #              fly_speed: int = 0, swim_speed: int = 0, ability_scores: dict = None, damage_resistances: list = None,
    #              damage_immunities: list = None, condition_immunities: list = None, saving_throws: dict = None,
    #              skills: dict = None, blindsight: int = 0, darkvision: int = 0, tremorsense: int = 0,
    #              truesight: int = 0,
    #              passive_perception: int = None, languages: list = None, telepathy: int = 0,
    #              challenge: ChallengeRating = None,
    #              abilities: list = None, actions: list = None, bonus_actions: list = None,
    #              reactions: list = None, legendary_actions: list = None, num_legendary: int = 3):
