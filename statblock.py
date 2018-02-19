import random
import re
import math
from collections import defaultdict
from utils import Dice
from utils import AbilityScore
from utils import ChallengeRating
from utils import Action
from utils import parse_table
from utils import format_modifier


def parse_resist_or_immunity(text: str) -> list:
    # TODO Ordering for this stuff is not super intuitive, should maybe consider creating a class for this rather than
    # always trying to keep in mind that the bludgeoning/piercing/slashing damage thing comes last after a semicolon
    bps_resistance = ''
    text_list = text.split(';')
    if len(text_list) > 1:  # This grabs the weird stuff, like 'b, p, and s from nonmagical weapons'
        bps_resistance = ', '.join([t.strip() for t in text_list[1:]])
    else:
        if 'bludg' in text_list[0] or 'slash' in text_list[0] or 'pierc' in text_list[0]:
            bps_resistance = text_list[0].strip()

    resistances = text_list[0].strip().split(',')
    if bps_resistance != '':
        resistances += [bps_resistance]

    return resistances


def parse_actions(lines: list, is_legendary=False):
    name_sym = '***'
    if is_legendary:
        name_sym = '**'

    actions = []
    while lines:
        if '###' in lines[0]:
            break

        curr_line = lines.pop(0)
        if curr_line.count(name_sym) == 0:
            if actions:
                if actions[-1].description:
                    # if actions[-1].description[-1] != '\n':
                        # actions[-1].description += '\n'
                    actions[-1].description += curr_line.strip('>').strip()
            continue

        curr_line = curr_line.strip('>').strip().lstrip('*')
        action_name, action_description = curr_line.split(name_sym)
        action_name = action_name.strip().strip('.')
        action_description = action_description.strip()
        actions.append(Action(action_name, action_description, is_legendary))

    return actions, lines


def random_name() -> str:
    first_name = random.choice(['Mike', 'Adam', 'Luke', 'Kevin', 'Gary'])
    last_name = random.choice(['Mearls', 'Koebel', 'Crane', 'Crawford', 'Gygax'])
    return '{} {}'.format(first_name, last_name)


class Statblock(object):
    # FIXME Might be better to redo this as just a dictionary. Could load in defaults from external json.
    #   Type-hinting is kind of fun, though.
    def __init__(self, name: str = None, size: str = 'Medium', primary_type: str = 'Humanoid',
                 secondary_type: str = '',
                 alignment: str = 'unaligned', armor_class: int = 10, armor_class_type: str = '',
                 hit_points: int = None, hit_point_bonus: int = 0, hit_dice: Dice = None, speed: int = 30,
                 climb_speed: int = 0,
                 fly_speed: int = 0, swim_speed: int = 0, ability_scores: dict = None,
                 damage_vulnerabilities: list = None, damage_resistances: list = None,
                 damage_immunities: list = None, condition_immunities: list = None, saving_throws: dict = None,
                 skills: dict = None, blindsight: int = 0, darkvision: int = 0, tremorsense: int = 0,
                 truesight: int = 0,
                 passive_perception: int = None, languages: list = None, telepathy: int = 0,
                 challenge: ChallengeRating = None,
                 abilities: list = None, actions: list = None, bonus_actions: list = None,
                 reactions: list = None, legendary_actions: list = None, num_legendary: int = 3, proficiency=0):

        self.name = name if name is not None else random_name()
        self.size = size
        self.primary_type = primary_type
        self.secondary_type = secondary_type
        self.alignment = alignment
        self.armor_class = armor_class
        self.armor_class_type = armor_class_type
        self.hit_point_bonus = hit_point_bonus
        self.hit_dice = Dice.from_string('1d8') if hit_dice is None else hit_dice
        self.speed = speed
        self.climb_speed = climb_speed
        self.fly_speed = fly_speed
        self.swim_speed = swim_speed

        self.ability_scores = defaultdict(AbilityScore)
        if ability_scores is not None:
            for key, value in ability_scores.items():
                self.ability_scores[key] = value
        else:
            self.ability_scores['STR'] = AbilityScore('Strength', 10)
            self.ability_scores['DEX'] = AbilityScore('Dexterity', 10)
            self.ability_scores['CON'] = AbilityScore('Constitution', 10)
            self.ability_scores['INT'] = AbilityScore('Intelligence', 10)
            self.ability_scores['WIS'] = AbilityScore('Wisdom', 10)
            self.ability_scores['CHA'] = AbilityScore('Charisma', 10)

        if hit_points is None:
            self.calc_hit_points()
        else:
            self.hit_points = hit_points

        self.saving_throws = defaultdict(int)
        if saving_throws is not None:
            for key, value in saving_throws.items():
                self.saving_throws[key] = value

        self.skills = defaultdict(int)
        if skills is not None:
            for key, value in skills.items():
                self.skills[key] = value

        self.damage_vulnerabilities = damage_vulnerabilities if damage_vulnerabilities is not None else []
        self.damage_resistances = damage_resistances if damage_resistances is not None else []
        self.damage_immunities = damage_immunities if damage_immunities is not None else []
        self.condition_immunities = condition_immunities if condition_immunities is not None else []

        self.blindsight = blindsight
        self.darkvision = darkvision
        self.tremorsense = tremorsense
        self.truesight = truesight

        self.__passive_perception = passive_perception

        self.languages = languages if languages is not None else ['Common']
        self.telepathy = telepathy
        # self.languages = languages if languages is not None else defaults['languages']
        self.challenge = challenge if challenge is not None else ChallengeRating('1')

        self.abilities = abilities
        self.actions = actions
        self.bonus_actions = bonus_actions
        self.reactions = reactions
        self.legendary_actions = legendary_actions

        self.num_legendary = num_legendary

        self.__proficiency = proficiency

    def calc_challenge(self):
        # TODO
        self.challenge = self.challenge

    def calc_hit_points(self):
        """Sets hit points using hit dice and either hit point bonus or constitution modifier."""
        self.hit_points = self.hit_dice.roll()
        if self.hit_point_bonus != 0:
            self.hit_points += self.hit_point_bonus
        elif self.ability_scores.get('CON') is not None:
            self.hit_points += self.ability_scores['CON']

    @property
    def passive_perception(self):
        if self.__passive_perception is None:
            return 10 + self.ability_scores['WIS'] + self.skills.get('Perception', 0)

        return self.__passive_perception

    @property
    def proficiency(self):
        """If proficiency wasn't set explicitly, calculates based on # of hit dice."""
        if not self.__proficiency:
            return 2 + int(max(math.floor(self.hit_dice.count - 1 / 4), 0))

    @proficiency.setter
    def proficiency(self, proficiency):
        self.__proficiency = proficiency

    def to_dict(self):
        # FIXME This is stupid, should have just stuffed attributes into a dict in the first place, there are way too
        # many of them
        return self.parse_markdown(self.to_markdown())

    @classmethod
    def from_markdown(cls, text: str):
        values = cls.parse_markdown(text)
        return cls(**values)

    @staticmethod
    def parse_markdown(text: str):
        # TODO Really should have done this with regex instead, would be more succinct and flexible
        values = {}

        lines = text.split('\n')
        try:
            curr_line = lines.pop(0)
            while curr_line.strip().startswith('_'):
                curr_line = lines.pop(0)

            # assert curr_line.strip().endswith('_')

            curr_line = curr_line.replace('> ##', '')
            values['name'] = curr_line.strip()

            curr_line = lines.pop(0)
            curr_line = curr_line.strip('>').strip().strip('*').strip().split(',')
            if len(curr_line) < 2:
                size_and_types = curr_line[0].strip()
                values['alignment'] = 'Unaligned'
            else:
                size_and_types, alignment = curr_line
                values['alignment'] = alignment.strip()

            size_and_types = size_and_types.split()
            if len(size_and_types) == 2:
                values['size'], values['primary_type'] = size_and_types
            elif len(size_and_types) == 3:
                values['size'], values['primary_type'], values['secondary_type'] = size_and_types
                values['secondary_type'] = values['secondary_type'].rstrip('(').lstrip(')')

            lines.pop(0)
            # assert curr_line.strip().endswith('_')

            curr_line = lines.pop(0)
            curr_line = curr_line.replace('> - **Armor Class** ', '').strip().split()
            if len(curr_line) >= 2:
                values['armor_class'] = int(curr_line[0])
                values['armor_class_type'] = ' '.join(curr_line[1:]).lstrip('(').rstrip(')')
            elif len(curr_line) == 1:
                values['armor_class'] = int(curr_line[0])

            curr_line = lines.pop(0)
            curr_line = curr_line.replace('> - **Hit Points** ', '').strip().split()
            if len(curr_line) >= 2:
                values['hit_points'] = int(curr_line[0])
                if len(curr_line) >= 4:
                    values['hit_dice'] = Dice.from_string(curr_line[1].lstrip('('))
                    values['hit_point_bonus'] = int(curr_line[3].rstrip(')'))
                else:
                    values['hit_dice'] = Dice.from_string(curr_line[1].lstrip('(').rstrip(')'))

            elif len(curr_line) == 1:
                values['hit_points'] = int(curr_line[0])

            curr_line = lines.pop(0)
            curr_line = curr_line.replace('> - **Speed** ', '')
            speeds = curr_line.replace('ft.', '').split(',')
            for speed_text in speeds:
                if len(speed_text.strip().split()) == 1:
                    values['speed'] = int(speed_text.strip())
                elif speed_text.strip().lower().startswith('climb'):
                    values['climb_speed'] = int(speed_text.strip().split()[1])
                elif speed_text.strip().lower().startswith('swim'):
                    values['swim_speed'] = int(speed_text.strip().split()[1])
                elif speed_text.strip().lower().startswith('fly'):
                    values['fly_speed'] = int(speed_text.strip().split()[1])
                else:
                    print('Warning: Couldn\'t parse speed {}'.format(speed_text))

            lines.pop(0)
            # assert curr_line.strip().endswith('_')

            curr_line = lines.pop(0).strip('>')
            ab_score_table_lines = []
            while curr_line.strip().startswith('|'):
                ab_score_table_lines.append(curr_line)
                curr_line = lines.pop(0).strip('>')

            score_tab = parse_table(ab_score_table_lines)

            values['ability_scores'] = {}
            for ab_score_name in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']:
                ab_score = AbilityScore(ab_score_name)
                score_val = score_tab.pop(ab_score.short_name, [None])[0]
                if score_val is not None:
                    ab_score.value = int(score_val.split()[0])
                values['ability_scores'][ab_score.short_name] = ab_score

            for ab_score_name in list(score_tab.keys()):
                ab_score = AbilityScore(ab_score_name)
                score_val = score_tab.pop(ab_score.short_name, [None])[0]
                if score_val is not None:
                    ab_score.value = int(score_val.split()[0])
                values['ability_scores'][ab_score.short_name] = ab_score

            if lines[0].rstrip('>').strip().startswith('_'):
                lines.pop(0)

            if 'Skills' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Skills** ', '')
                skill_texts = curr_line.split(',')

                values['skills'] = {}
                for skill_text in skill_texts:
                    skill_name, skill_mod = skill_text.split()
                    values['skills'][skill_name] = int(skill_mod)

            if 'Saving' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Saving Throws** ', '')
                save_texts = curr_line.split(',')

                values['saving_throws'] = {}
                for save_text in save_texts:
                    save_name, save_mod = save_text.split()
                    values['saving_throws'][save_name] = int(save_mod)

            if 'Damage Vuln' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Damage Vulnerabilities** ', '')
                values['damage_vulnerabilities'] = parse_resist_or_immunity(curr_line)

            if 'Damage Resist' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Damage Resistances** ', '')
                values['damage_resistances'] = parse_resist_or_immunity(curr_line)

            if 'Damage Immun' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Damage Immunities** ', '')
                values['damage_immunities'] = parse_resist_or_immunity(curr_line)

            if 'Condition Immun' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Damage Immunities** ', '')
                values['condition_immunities'] = curr_line.strip().split(',')

            if 'Senses' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Senses** ', '')
                sense_texts = curr_line.split(',')

                for sense_text in sense_texts:
                    sense_text = sense_text.replace('ft.', '').strip().split()
                    if sense_text[0].lower() == 'blindsight':
                        values['blindsight'] = int(sense_text[1])
                    if sense_text[0].lower() == 'truesight':
                        values['truesight'] = int(sense_text[1])
                    if sense_text[0].lower() == 'darkvision':
                        values['darkvision'] = int(sense_text[1])
                    if sense_text[0].lower() == 'tremorsense':
                        values['tremorsense'] = int(sense_text[1])
                    if sense_text[0] == 'passive':
                        values['passive_perception'] = int(sense_text[2])

            if 'Languages' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Languages** ', '')
                values['languages'] = [curr_line.strip()]

            if 'Challenge' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Challenge** ', '')
                challenge = curr_line.strip().split()[0]
                values['challenge'] = ChallengeRating(challenge)

            while lines[0].strip('>').strip().startswith('_'):
                lines.pop(0)

            values['abilities'], lines = parse_actions(lines)
            while lines:
                curr_line = lines.pop(0)
                if '### Actions' in curr_line:
                    values['actions'], lines = parse_actions(lines)
                elif '### Bonus Actions' in curr_line:
                    values['bonus_actions'], lines = parse_actions(lines)
                elif '### Reactions' in curr_line:
                    values['reactions'], lines = parse_actions(lines)
                elif '### Legendary Actions' in curr_line:
                    while not lines[0].strip('>').strip().startswith('*'):
                        num_leg = re.search(r'can take (\d+) legendary actions', lines.pop(0))
                        if num_leg:
                            values['num_legendary'] = int(num_leg.groups()[0])
                    values['legendary_actions'], lines = parse_actions(lines, is_legendary=True)

        except Exception as e:
            print('\nRemaining lines:')
            for line in lines:
                print(line)

            print('Error parsing Statblock from markdown. Exception: ')
            raise e

        return values

    def to_markdown(self) -> str:
        lines = ['## {}'.format(self.name)]

        type_line = '*{} {}'.format(self.size, self.primary_type)
        if self.secondary_type:
            type_line += ' ({})'.format(self.secondary_type)
        type_line += (', {}*'.format(self.alignment))
        lines.append(type_line)

        lines.append('___')

        ac_line = '- **Armor Class** {}'.format(self.armor_class)
        if self.armor_class_type:
            ac_line += ' ({})'.format(self.armor_class_type)
        lines.append(ac_line)

        hp_line = '- **Hit Points** {}'.format(self.hit_points)
        if self.hit_dice:
            hp_line += ' ({}'.format(self.hit_dice)
            if self.hit_point_bonus:
                if self.hit_point_bonus > 0:
                    hp_line += ' + {})'.format(self.hit_point_bonus)
                else:
                    hp_line += ' - {})'.format(self.hit_point_bonus)
            else:
                hp_line += ')'
        lines.append(hp_line)

        speed_line = '- **Speed** {} ft.'.format(self.speed)
        if self.climb_speed:
            speed_line += (', climb {} ft.'.format(self.climb_speed))
        if self.fly_speed:
            speed_line += (', fly {} ft.'.format(self.fly_speed))
        if self.swim_speed:
            speed_line += (', swim {} ft.'.format(self.swim_speed))
        lines.append(speed_line)

        lines.append('___')

        ab_score_names = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
        for key in sorted(self.ability_scores.keys()):
            if key not in ab_score_names:
                ab_score_names.append(key)
        lines.append('|' + '|'.join(ab_score_names) + '|')

        lines.append(''.join(['|:---:'] * len(ab_score_names)) + '|')

        ab_score_line = '|'
        for ab in ab_score_names:
            ab_score_line += '{} ({})|'.format(self.ability_scores[ab].value,
                                               format_modifier(self.ability_scores[ab].modifier))
        lines.append(ab_score_line)

        lines.append('___')

        if self.saving_throws:
            if any([v > 0 for v in self.saving_throws.values()]):
                save_line = '- **Saving Throws** '
                save_line += ', '.join(['{} {}'.format(save, format_modifier(modifier)) for save, modifier in
                                       sorted(self.saving_throws.items(), key=lambda x: x[0])])
                lines.append(save_line)

        if self.skills:
            if any([v > 0 for v in self.skills.values()]):
                skill_line = '- **Skills** '
                skill_line += ', '.join(['{} {}'.format(skill, format_modifier(modifier)) for skill, modifier in
                                        sorted(self.skills.items(), key=lambda x: x[0])])
                lines.append(skill_line)

        if self.damage_vulnerabilities:
            dv_line = '- **Damage Vulnerabilities** '
            if 'bludg' in self.damage_vulnerabilities[-1] or 'pierc' in self.damage_vulnerabilities[-1] \
                    or 'slash' in self.damage_vulnerabilities[-1]:
                dv_line += ', '.join(sorted(self.damage_vulnerabilities[:-1]))
                dv_line += '; {}'.format(self.damage_vulnerabilities[-1])
            else:
                dv_line += ', '.join(sorted(self.damage_vulnerabilities))
            lines.append(dv_line)

        if self.damage_resistances:
            dr_line = '- **Damage Resistances** '
            if 'bludg' in self.damage_resistances[-1] or 'pierc' in self.damage_resistances[-1] \
                    or 'slash' in self.damage_resistances[-1]:
                dr_line += ', '.join(sorted(self.damage_resistances[:-1]))
                dr_line += '; {}'.format(self.damage_resistances[-1])
            else:
                dr_line += ', '.join(sorted(self.damage_resistances))
            lines.append(dr_line)

        if self.damage_immunities:
            di_line = '- **Damage Immunities** '
            if 'bludg' in self.damage_immunities[-1] or 'pierc' in self.damage_immunities[-1] \
                    or 'slash' in self.damage_immunities[-1]:
                di_line += ', '.join(sorted(self.damage_immunities[:-1]))
                di_line += '; {}'.format(self.damage_immunities[-1])
            else:
                di_line += ', '.join(sorted(self.damage_immunities))
            lines.append(di_line)

        if self.condition_immunities:
            lines.append('- **Condition Immunities** {}'.format(', '.join(sorted(self.condition_immunities))))

        sense_line = '- **Senses** '
        senses = []
        if self.blindsight:
            senses.append('blindsight {} ft.'.format(self.blindsight))
        if self.darkvision:
            senses.append('darkvision {} ft.'.format(self.darkvision))
        if self.tremorsense:
            senses.append('tremorsense {} ft.'.format(self.tremorsense))
        if self.truesight:
            senses.append('truesight {} ft.'.format(self.truesight))
        senses.append('passive Perception {}'.format(self.passive_perception))

        if senses:
            sense_line += ', '.join(senses)
            lines.append(sense_line)

        lang_line = '- **Languages** {}'.format(', '.join(sorted(self.languages)))
        if self.telepathy:
            lang_line += ' , telepathy {} ft.'.format(self.telepathy)
        lines.append(lang_line)

        lines.append('- **Challenge** {} ({:,} XP)'.format(self.challenge.rating, self.challenge.xp))

        lines.append('___')

        if self.abilities:
            for action in self.abilities:
                # These might get a little more complicated in future, so we will let the Action class do formatting
                lines.append(str(action))
                if lines[-1].strip() != '':
                    lines.append('')

        if self.actions:
            lines.append('### Actions')
            for action in self.actions:
                lines.append(str(action))
                if lines[-1].strip() != '':
                    lines.append('')

        if self.bonus_actions:
            lines.append('### Bonus Actions')
            for action in self.bonus_actions:
                lines.append(str(action))
                if lines[-1].strip() != '':
                    lines.append('')

        if self.reactions:
            lines.append('### Reactions')
            for action in self.reactions:
                lines.append(str(action))
                if lines[-1].strip() != '':
                    lines.append('')

        if self.legendary_actions:
            lines.append('### Legendary Actions')
            lines.append('')
            lines.append('This creature can take {} legendary actions, choosing from the options below. Only one '
                         'legendary action can be used at a time and only at the end of another creature\'s turn. This '
                         'creature regains spent legendary actions at the start of its turn.'.format(self.num_legendary))
            if lines[-1].strip() != '':
                lines.append('')
            for action in self.legendary_actions:
                lines.append(str(action))
                lines.append('')

        return '\n'.join(['___', '___'] + ['> ' + line for line in lines])
