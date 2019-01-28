import random
import re
import math
import logging
from collections import defaultdict
from copy import deepcopy
from typing import Callable  # don't remove, used in docstrings
from utils import Dice
from utils import AbilityScore
from utils import ChallengeRating
from utils import Action
from utils import parse_table
from utils import format_modifier
from utils import size_min, size_max, size_name_to_val, size_val_to_name


def parse_resist_or_immunity(text: str) -> set:
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

    # logging.debug(f'parse_resist_or_immunity({text}) -> {resistances}')
    return set(resistances)


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

    logging.debug(f'parse_actions(lines={lines},\n is_legendary={is_legendary}) -> {actions}, {lines}')
    return actions, lines


def random_name() -> str:
    first_name = random.choice(['Mike', 'Adam', 'Luke', 'Kevin', 'Gary'])
    last_name = random.choice(['Mearls', 'Koebel', 'Crane', 'Crawford', 'Gygax'])
    return '{} {}'.format(first_name, last_name)


class Statblock(object):
    # FIXME Might be better to redo this as just a dictionary. Could load in defaults from external json.
    #   Type-hinting is kind of fun, though.
    def __init__(self, name: str = None, size: int = 2, primary_type: str = 'Humanoid',
                 secondary_type: str = '',
                 alignment: str = 'unaligned', armor_class: int = 10, armor_class_type: str = '',
                 hit_points: int = None, hit_point_bonus: int = 0, hit_dice: Dice = None, speed: int = 30,
                 climb_speed: int = 0,
                 fly_speed: int = 0, swim_speed: int = 0, ability_scores: dict = None,
                 damage_vulnerabilities: set = None, damage_resistances: set = None,
                 damage_immunities: set = None, condition_immunities: set = None, saving_throws: dict = None,
                 skills: dict = None, blindsight: int = 0, darkvision: int = 0, tremorsense: int = 0,
                 truesight: int = 0,
                 passive_perception: int = None, languages: list = None, telepathy: int = 0,
                 challenge: ChallengeRating = None,
                 abilities: list = None, actions: list = None, bonus_actions: list = None,
                 reactions: list = None, legendary_actions: list = None, num_legendary: int = 3, proficiency=0,
                 applied_tags: list = None,
                 original_text: str = None,
                 **additional_skills):

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
        if additional_skills is not None:
            for key, value in additional_skills.items():
                self.skills[key] = value

        self.damage_vulnerabilities = damage_vulnerabilities if damage_vulnerabilities is not None else set()
        self.damage_resistances = damage_resistances if damage_resistances is not None else set()
        self.damage_immunities = damage_immunities if damage_immunities is not None else set()
        self.condition_immunities = condition_immunities if condition_immunities is not None else set()

        self.blindsight = blindsight
        self.darkvision = darkvision
        self.tremorsense = tremorsense
        self.truesight = truesight

        self.__passive_perception = passive_perception

        self.languages = languages if languages is not None else ['Common']
        self.telepathy = telepathy
        # self.languages = languages if languages is not None else defaults['languages']
        self.challenge = challenge if challenge is not None else ChallengeRating('1')

        self.features = abilities
        self.actions = actions
        self.bonus_actions = bonus_actions
        self.reactions = reactions
        self.legendary_actions = legendary_actions

        self.num_legendary = num_legendary
        self.__proficiency = proficiency
        self.applied_tags = applied_tags if applied_tags is not None else []
        self.base_natural_armor = 0

        self.original_text = original_text if original_text is not None else ''

    def get_substitutable_values(self):
        values = {}
        for ab_score in self.ability_scores.values():
            values[ab_score.name] = ab_score.value
            values[ab_score.short_name] = ab_score.modifier
        for skill, skill_mod in self.skills.items():
            values[skill] = skill_mod
        values['proficiency'] = self.proficiency
        values['prof'] = self.proficiency
        values['size_mod'] = self.size_mod
        values['size'] = size_val_to_name[self.size]
        return values

    def calc_challenge(self):
        # TODO
        self.challenge = self.challenge

    def calc_hit_points(self):
        """Sets hit points using hit dice and either hit point bonus or constitution modifier."""
        try:
            original_hp = self.hit_points
        except AttributeError:
            original_hp = '<unset>'
        self.hit_points = self.hit_dice.upper_average()
        if self.hit_point_bonus != 0:
            self.hit_points += self.hit_point_bonus
        elif self.ability_scores.get('CON') is not None:
            self.hit_points += self.ability_scores['CON']
        logging.debug(f'calc_hit_points() updated hp from {original_hp} to {self.hit_points}')

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

    def add_damage_resistance(self, damage_type):
        if damage_type in self.damage_resistances:
            self.damage_resistances.remove(damage_type)
            self.damage_immunities.add(damage_type)
        elif damage_type in self.damage_vulnerabilities:
            self.damage_vulnerabilities.discard(damage_type)
        elif damage_type in self.damage_immunities:
            pass
        else:
            self.damage_resistances.add(damage_type)
        return self

    def add_damage_vulnerability(self, damage_type):
        if damage_type in self.damage_resistances:
            self.damage_resistances.remove(damage_type)
        elif damage_type in self.damage_vulnerabilities:
            pass
        elif damage_type in self.damage_immunities:
            self.damage_immunities.remove(damage_type)
            self.damage_resistances.add(damage_type)
        else:
            self.damage_vulnerabilities.add(damage_type)
        return self

    def size_mod(self):
        """Can be used to calculate the number of damage dice to roll based on a creature's size."""
        if self.size == 0:  # tiny
            return 0
        if self.size in {1, 2}:  # small or medium
            return 1
        if self.size == 3:  # large
            return 2
        if self.size == 4:  # huge
            return 3
        if self.size == 5:  # gargantuan
            return 4

    @classmethod
    def from_markdown(cls, text: str = '', filename=''):
        if filename:
            logging.debug(f'New Statblock from file f{filename}.')
            with open(filename) as file_handle:
                text = file_handle.read()
        else:
            logging.debug('New Statblock from text.')
        if not text and not filename:
            raise RuntimeError('Either text or filename must be specified.')

        sb = Statblock(original_text=text)

        lines = text.split('\n')
        try:
            curr_line = lines.pop(0)
            while curr_line.strip().startswith('_'):
                curr_line = lines.pop(0)

            # assert curr_line.strip().endswith('_')

            curr_line = curr_line.replace('> ##', '')
            sb.name = curr_line.strip()
            logging.debug(f'Parsed name "{sb.name}"')

            curr_line = lines.pop(0)
            curr_line = curr_line.strip('>').strip().strip('*').strip().split(',')
            if len(curr_line) < 2:
                size_and_types = curr_line[0].strip()
                sb.alignment = 'Unaligned'
            else:
                size_and_types, alignment = curr_line
                sb.alignment = alignment.strip()
            logging.debug(f'Parsed alignment "{sb.alignment}"')

            size_and_types = size_and_types.split()
            if len(size_and_types) == 2:
                sb.size, sb.primary_type = size_and_types
            elif len(size_and_types) == 3:
                sb.size, sb.primary_type, sb.secondary_type = size_and_types
                sb.secondary_type = sb.secondary_type.replace('(', '').replace(')', '').strip()
            logging.debug(f'Parsed types "{sb.primary_type}", "{sb.secondary_type}""')

            sb.size = max(size_name_to_val.get(sb.size, -1), size_min)
            sb.size = min(sb.size, size_max)
            logging.debug(f'Parsed size "{size_val_to_name[sb.size]}"')

            lines.pop(0)
            # assert curr_line.strip().endswith('_')

            curr_line = lines.pop(0)
            curr_line = curr_line.replace('> - **Armor Class** ', '').strip().split()
            if len(curr_line) >= 2:
                sb.armor_class = int(curr_line[0])
                sb.armor_class_type = ' '.join(curr_line[1:]).lstrip('(').rstrip(')')
            elif len(curr_line) == 1:
                sb.armor_class = int(curr_line[0])
            logging.debug(f'Parsed AC "{sb.armor_class}", "{sb.armor_class_type}"')

            curr_line = lines.pop(0)
            curr_line = curr_line.replace('> - **Hit Points** ', '').strip().split()
            if len(curr_line) >= 2:
                sb.hit_points = int(curr_line[0])
                if len(curr_line) >= 4:
                    sb.hit_dice = Dice.from_string(curr_line[1].lstrip('('))
                    sb.hit_point_bonus = int(curr_line[3].rstrip(')'))
                else:
                    sb.hit_dice = Dice.from_string(curr_line[1].lstrip('(').rstrip(')'))
            elif len(curr_line) == 1:
                sb.hit_points = int(curr_line[0])
            logging.debug(f'Parsed HP "{sb.hit_points}"')
            logging.debug(f'Parsed HP bonus "{sb.hit_point_bonus}"')
            logging.debug(f'Parsed hit dice "{sb.hit_dice}"')

            curr_line = lines.pop(0)
            curr_line = curr_line.replace('> - **Speed** ', '')
            speeds = curr_line.replace('ft.', '').split(',')
            for speed_text in speeds:
                if len(speed_text.strip().split()) == 1:
                    sb.speed = int(speed_text.strip())
                elif speed_text.strip().lower().startswith('climb'):
                    sb.climb_speed = int(speed_text.strip().split()[1])
                elif speed_text.strip().lower().startswith('swim'):
                    sb.swim_speed = int(speed_text.strip().split()[1])
                elif speed_text.strip().lower().startswith('fly'):
                    sb.fly_speed = int(speed_text.strip().split()[1])
                else:
                    print('Warning: Couldn\'t parse speed {}'.format(speed_text))
            logging.debug(f'Parsed speed="{sb.speed}", fly="{sb.fly_speed}", swim="{sb.swim_speed}", '
                          f'climb="{sb.climb_speed}"')

            lines.pop(0)
            # assert curr_line.strip().endswith('_')

            curr_line = lines.pop(0).strip('>')
            ab_score_table_lines = []
            while curr_line.strip().startswith('|'):
                ab_score_table_lines.append(curr_line)
                curr_line = lines.pop(0).strip('>')

            score_table = parse_table(ab_score_table_lines)

            for ab_score_name in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']:
                ab_score = AbilityScore(ab_score_name)
                score_val = score_table.pop(ab_score.short_name, [None])[0]
                if score_val is not None:
                    ab_score.value = int(score_val.split()[0])
                sb.ability_scores[ab_score.short_name] = ab_score

            for ab_score_name in list(score_table.keys()):
                ab_score = AbilityScore(ab_score_name)
                score_val = score_table.pop(ab_score.short_name, [None])[0]
                if score_val is not None:
                    ab_score.value = int(score_val.split()[0])
                sb.ability_scores[ab_score.short_name] = ab_score
            logging.debug(f'Parsed ability scores "{sb.ability_scores}"')

            if 'natural armor' in sb.armor_class_type:
                sb.base_natural_armor = sb.armor_class - sb.ability_scores['DEX'].modifier
                logging.debug(f'Parsed base natural armor "{sb.base_natural_armor}"')

            if lines[0].rstrip('>').strip().startswith('_'):
                lines.pop(0)

            if 'Saving' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Saving Throws** ', '')
                save_texts = curr_line.split(',')
                for save_text in save_texts:
                    save_name, save_mod = save_text.split()
                    sb.saving_throws[save_name] = int(save_mod)
            logging.debug(f'Parsed saving throws "{sb.saving_throws}"')

            if 'Skills' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Skills** ', '')
                skill_texts = curr_line.split(',')
                for skill_text in skill_texts:
                    skill_name, skill_mod = skill_text.split()
                    sb.skills[skill_name] = int(skill_mod)
            logging.debug(f'Parsed skills "{sb.skills}"')

            if 'Damage Vuln' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Damage Vulnerabilities** ', '')
                sb.damage_vulnerabilities = parse_resist_or_immunity(curr_line)
            logging.debug(f'Parsed damage vulns "{sb.damage_vulnerabilities}"')

            if 'Damage Resist' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Damage Resistances** ', '')
                sb.damage_resistances = parse_resist_or_immunity(curr_line)
            logging.debug(f'Parsed damage resistances "{sb.damage_resistances}"')

            if 'Damage Immun' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Damage Immunities** ', '')
                sb.damage_immunities = parse_resist_or_immunity(curr_line)
            logging.debug(f'Parsed damage immunities "{sb.damage_immunities}"')

            if 'Condition Immun' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Condition Immunities** ', '')
                sb.condition_immunities = [c.strip() for c in curr_line.strip().split(',') if c.strip()]
            logging.debug(f'Parsed condition immunities "{sb.condition_immunities}"')

            if 'Senses' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Senses** ', '')
                sense_texts = curr_line.split(',')

                for sense_text in sense_texts:
                    sense_text = sense_text.replace('ft.', '').strip().split()
                    if sense_text[0].lower() == 'blindsight':
                        sb.blindsight = int(sense_text[1])
                    if sense_text[0].lower() == 'truesight':
                        sb.truesight = int(sense_text[1])
                    if sense_text[0].lower() == 'darkvision':
                        sb.darkvision = int(sense_text[1])
                    if sense_text[0].lower() == 'tremorsense':
                        sb.tremorsense = int(sense_text[1])
                    if sense_text[0] == 'passive':
                        sb.__passive_perception = int(sense_text[2])
            logging.debug(
                f'Parsed senses blindsight={sb.blindsight}, truesight={sb.truesight}, darkvision={sb.darkvision},'
                f'tremorsense={sb.tremorsense}, passive perception={sb.__passive_perception}')

            if 'Languages' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Languages** ', '')
                sb.languages = [lang.strip() for lang in curr_line.split(',') if 'telepathy' not in lang]
                if 'telepathy' in curr_line:
                    try:
                        sb.telepathy = int(re.search(r'telepathy (\d+) ft', curr_line).group(1))
                    except AttributeError:
                        sb.telepathy = 60  # TODO need an external default file
            if len(sb.languages) == 1:
                if re.search(r'[A-Za-z0-9]', sb.languages[0]) is None:  # check for something like '-'
                    sb.languages = []
            logging.debug(f'Parsed languages "{sb.languages}"')
            logging.debug(f'Parsed telepathy "{sb.telepathy}"')

            if 'Challenge' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Challenge** ', '')
                challenge = curr_line.strip().split()[0]
                sb.challenge = ChallengeRating(challenge)
            logging.debug(f'Parsed CR "{sb.challenge.rating}"')

            if 'Tags' in lines[0]:
                curr_line = lines.pop(0).replace('> - **Tags** ', '')
                sb.applied_tags = [Tag(tag_name.strip()) for tag_name in curr_line.split(',')]
            logging.debug(f'Parsed tags "{sb.applied_tags}""')

            if not lines:
                return sb

            while lines[0].strip('>').strip().startswith('_'):
                lines.pop(0)
                if not lines:
                    return sb

            sb.features, lines = parse_actions(lines)
            while lines:
                curr_line = lines.pop(0)
                if '## Actions' in curr_line:
                    sb.actions, lines = parse_actions(lines)
                elif '## Bonus Actions' in curr_line:
                    sb.bonus_actions, lines = parse_actions(lines)
                elif '## Reactions' in curr_line:
                    sb.reactions, lines = parse_actions(lines)
                elif '## Legendary Actions' in curr_line:
                    while not lines[0].strip('>').strip().startswith('*'):
                        num_leg = re.search(r'can take (\d+) legendary actions', lines.pop(0))
                        if num_leg:
                            sb.num_legendary = int(num_leg.groups()[0])
                    sb.legendary_actions, lines = parse_actions(lines, is_legendary=True)
            logging.debug(f'Parsed features={sb.features}, actions={sb.actions}, bonus actions={sb.bonus_actions},'
                          f'legendary actions={sb.legendary_actions}, num legendary={sb.num_legendary}')

        except Exception as e:
            print('\nRemaining lines:')
            for line in lines:
                print(line)

            print('Error parsing Statblock from markdown. Exception: ')
            raise e

        return sb

    def to_markdown(self) -> str:
        lines = ['## {}'.format(self.name)]

        type_line = '*{} {}'.format(size_val_to_name.get(self.size, 'Medium'), self.primary_type)
        if self.secondary_type:
            type_line += ' ({})'.format(self.secondary_type)
        type_line += (', {}*'.format(self.alignment))
        lines.append(type_line)

        lines.append('___')

        if 'natural armor' in self.armor_class_type:
            ac_line = '- **Armor Class** {}'.format(self.base_natural_armor + self.ability_scores['DEX'].modifier)
        else:
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
            vulns = self.damage_vulnerabilities.copy()
            has_bps = False
            for vuln in list(vulns):
                if 'bludg' in vuln or 'pierc' in vuln or 'slash' in vuln and len(self.damage_vulnerabilities) > 1:
                    vulns.remove(vuln)
                    dv_line += ', '.join(sorted(vulns))
                    dv_line += '; {}'.format(vuln)
                    has_bps = True
            if not has_bps:
                dv_line += ', '.join(sorted(vulns))
            lines.append(dv_line)

        if self.damage_resistances:
            dr_line = '- **Damage Resistances** '
            vulns = self.damage_resistances.copy()
            has_bps = False
            for vuln in list(vulns):
                if 'bludg' in vuln or 'pierc' in vuln or 'slash' in vuln and len(self.damage_resistances) > 1:
                    vulns.remove(vuln)
                    dr_line += ', '.join(sorted(vulns))
                    dr_line += '; {}'.format(vuln)
                    has_bps = True
            if not has_bps:
                dr_line += ', '.join(sorted(vulns))
            lines.append(dr_line)

        if self.damage_immunities:
            di_line = '- **Damage Immunities** '
            vulns = self.damage_immunities.copy()
            has_bps = False
            for vuln in list(vulns):
                if ('bludg' in vuln or 'pierc' in vuln or 'slash' in vuln) and len(self.damage_immunities) > 1:
                    vulns.remove(vuln)
                    di_line += ', '.join(sorted(vulns))
                    di_line += '; {}'.format(vuln)
                    has_bps = True
            if not has_bps:
                di_line += ', '.join(sorted(vulns))
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

        if self.languages:
            lang_line = '- **Languages** {}'.format(', '.join(sorted(self.languages)))
        else:
            lang_line = '- **Languages** -'
        if self.telepathy:
            lang_line += ', telepathy {} ft.'.format(self.telepathy)
        lines.append(lang_line)

        lines.append('- **Challenge** {} ({:,} XP)'.format(self.challenge.rating, self.challenge.xp))

        if self.applied_tags:
            lines.append('- **Tags** {}'.format(', '.join([t.name for t in self.applied_tags])))

        lines.append('___')

        if self.features:
            for action in self.features:
                # These might get a little more complicated in future, so we will let the Action class do formatting
                action.update_description(self.get_substitutable_values())
                lines.append(str(action))
                if lines[-1].strip() != '':
                    lines.append('')

        if self.actions:
            lines.append('### Actions')
            for action in self.actions:
                action.update_description(self.get_substitutable_values())
                for line in str(action).splitlines():
                    lines.append(line)
                if lines[-1].strip() != '':
                    lines.append('')

        if self.bonus_actions:
            lines.append('### Bonus Actions')
            for action in self.bonus_actions:
                action.update_description(self.get_substitutable_values())
                for line in str(action).splitlines():
                    lines.append(line)
                if lines[-1].strip() != '':
                    lines.append('')

        if self.reactions:
            lines.append('### Reactions')
            for action in self.reactions:
                action.update_description(self.get_substitutable_values())
                for line in str(action).splitlines():
                    lines.append(line)
                if lines[-1].strip() != '':
                    lines.append('')

        if self.legendary_actions:
            lines.append('### Legendary Actions')
            lines.append('')
            lines.append('This creature can take {} legendary actions, choosing from the options below. Only one '
                         'legendary action can be used at a time and only at the end of another creature\'s turn. This '
                         'creature regains spent legendary actions at the start of its turn.'.format(self.num_legendary)
                         )
            if lines[-1].strip() != '':
                lines.append('')
            for action in self.legendary_actions:
                action.update_description(self.get_substitutable_values())
                for line in str(action).splitlines():
                    lines.append(line)
                lines.append('')

        return '\n'.join(['___', '___'] + ['> ' + line for line in lines])


def default_on_overwrite(tag, other_tag, statblock: Statblock):
    # When I'm overwritten, remove me!
    return default_remove(tag, statblock), True

def default_remove(tag, statblock: Statblock) -> Statblock:
    if statblock.original_text is None:
        logging.warning('Cannot remove tag, no original text for this Statblock.')
        return statblock

    new_sb = Statblock.from_markdown(statblock.original_text)
    text_tags = [tag.name for tag in new_sb.applied_tags]
    for applied_tag in statblock.applied_tags:
        if applied_tag.name == tag.name or applied_tag.name in text_tags:
            continue
        new_sb = applied_tag.apply(new_sb)
    return new_sb


class Tag(object):
    def __init__(self, name, effect_text='', weight=10, on_apply=None, stacks=False, overwrites=None,
                 overwritten_by=None, on_stack=None, on_overwrite=None, remove=None, requires=None):
        """Used for applying various little thematic changes to monster statblocks.

        Args:
            name (str): Name of the Tag
            effect_text (str):  Human-readable description of what the Tag does, e.g. "add cold resistance"
            weight (float): How likely it is to roll this tag on a table compared to other tags on the table.
            on_apply (Callable[[Statblock], Statblock]): Function which modifies a statblock, e.g. add 'cold' to its
                                                            set of resistances
            stacks (bool):  If True, calls on_stack() when applying the Tag. This would be useful for something like
                                a fire resistance Tag which is applied twice, which we would like to become fire
                                immunity.
            overwrites (set):   Labels for Tags which should interact with this Tag when it is applied, e.g. if we are
                                    adding the 'hideous' Tag to a Statblock which already has the 'beautiful' Tag, we
                                    might want to undo the 'beautiful' Tag's effects in addition to applying the effects
                                    of the 'hideous' Tag (or not apply the effects of hideous at all). We could use a
                                    label like 'appearance' for both of the Tags, or we could just use the names of the
                                    Tags as triggering labels.
            overwritten_by (set):   Labels for Tags which this Tag should interact with when they are applied.
            on_stack (Callable[[Statblock], Statblock]):    Called when this Tag is applied on a Statblock which already
                                                                has the Tag.
            on_overwrite (Callable[[Tag, Statblock], Tuple(Statblock, bool)]):   See apply() to understand when this is
                                                                                    called. Should return a modified
                                                                                    Statblock and True or unmodified
                                                                                    Statblock and False.
            remove (Callable[[Statblock], Statblock]):  Callable that should return a Statblock with the effects of
                                                        this Tag undone. By default, this is done by taking the base
                                                        statblock and reapplying every tag but this one.
            requires (set): Set of tag names which this Tag requires in order to be applied
        """
        self.name = name
        self.effect_text = effect_text
        self.weight = weight
        self.on_apply = on_apply
        if on_apply is None:
            self.on_apply = lambda sb: sb
        else:
            self.on_apply = on_apply
        self.stacks = stacks
        self.overwrites = set() if overwrites is None else overwrites
        self.overwritten_by = set() if overwritten_by is None else overwritten_by
        self.requires = set() if requires is None else requires
        if on_stack is None:
            self.on_stack = lambda sb: sb
        else:
            self.on_stack = on_stack

        if remove is None:
            self.remove = default_remove
        else:
            self.remove = remove

        if on_overwrite is None:
            self.on_overwrite = default_on_overwrite
        else:
            self.on_overwrite = on_overwrite

    def __repr__(self):
        return 'Tag<name="{}", effect_text="{}", on_apply={}, stacks={}, overwrites={}, overwritten_by={}, ' \
               'on_stack={}, on_overwrite={}, remove={}>'.format(self.name, self.effect_text, self.on_apply,
                                                                 self.stacks, self.overwrites, self.overwritten_by,
                                                                 self.on_stack, self.on_overwrite, self.remove)

    def apply(self, statblock: Statblock) -> Statblock:
        if self.name in statblock.applied_tags:
            if self.stacks:
                statblock = self.on_stack(statblock)
            else:
                return statblock

        if self.requires:
            old_names = [tag.name for tag in statblock.applied_tags]
            if not all([required_tag in old_names for required_tag in self.requires]):
                return statblock

        for old_tag in statblock.applied_tags:
            for label in old_tag.overwritten_by:
                if label in self.overwrites:
                    statblock, keep_applying = old_tag.on_overwrite(old_tag, self, statblock)
                    if not keep_applying:
                        return statblock

        statblock = self.on_apply(statblock)
        statblock.applied_tags.append(self)
        return statblock

    @staticmethod
    def get_text_table(tag_list: list) -> str:
        if isinstance(tag_list, dict):
            tag_list = list(tag_list.values())

        out_str = '| d1000 | Tag | Description | '
        out_str += '|:-:|:-:|:-:|'
        total_weight = 0
        for tag in tag_list:
            out_str += '{}-{} | {} | {}'.format(total_weight, tag.weight - 1, tag.name, tag.effect_text)
            total_weight += tag.weight
        return out_str

    @staticmethod
    def get_dict_table(tag_list: list) -> dict:
        if isinstance(tag_list, dict):
            tag_list = list(tag_list.values())

        total_weight = sum([tag.weight for tag in tag_list])
        out_dict = {}
        for tag in tag_list:
            tag_dict = {'weight': '{:.1%}'.format(tag.weight / total_weight), 'effect': tag.effect_text,
                        'stacks': str(tag.stacks), 'requires': tag.requires}
            out_dict[tag.name] = tag_dict
        return out_dict
