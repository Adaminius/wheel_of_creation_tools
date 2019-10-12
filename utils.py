import csv
import random
import json
import sys
import pandas as pd
import re
import io
import math
import logging
from collections import OrderedDict, defaultdict
from os import path

package_directory = path.dirname(path.abspath(__file__))

size_val_to_name = {0:  'Tiny',
                    1:  'Small',
                    2:  'Medium',
                    3:  'Large',
                    4:  'Huge',
                    5:  'Gargantuan',
                    }
size_name_to_val = dict([(val, key) for key, val in size_val_to_name.items()])
size_min = 0
size_max = 5

num_to_english = {0: 'zero',
                  1: 'one',
                  2: 'two',
                  3: 'three',
                  4: 'four',
                  5: 'five',
                  6: 'six',
                  7: 'seven',
                  8: 'eight',
                  9: 'nine',
                  }

# doesn't include bludgeoning, piercing, and slashing
damage_types = ['acid', 'cold', 'fire', 'force', 'lightning', 'necrotic', 'poison', 'psychic', 'radiant', 'thunder']


def setup_logging(debug=True, filename=''):
    log_level = logging.DEBUG if debug else logging.INFO
    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    if filename:
        logging.basicConfig(filename=filename, level=log_level, format=log_format)
    else:
        logging.basicConfig(stream=sys.stderr, level=log_level, format=log_format)


def ordinal(num: str):
    if isinstance(num, int):
        num = str(num)
    if isinstance(num, float):
        num = str(int(num))
    mapping = {
        '1': 'st',
        '2': 'nd',
        '3': 'rd'
    }
    mapping = defaultdict(lambda: 'th', mapping)
    return f'{num}{mapping[num[-1]]}'


class RollableTable(object):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    @classmethod
    def from_markdown(cls, text: str):
        df = pd.DataFrame.from_csv(io.StringIO(text), sep='|')
        df.columns = df.columns.str.strip()
        return cls(df=df)

    @staticmethod
    def convert_weight(s: str):
        if '-' not in s:
            return 1
        lower, upper = s.split('-')
        return int(upper) - int(lower) + 1

    def roll(self):
        if re.search(r'\d*d\d+', self.df.columns[0]):
            return self.df.iloc[:, 1:].sample(1, weights=[self.convert_weight(s) for s in self.df.values[:, 0]])
        return self.df.sample(1)


class Dice(object):
    """This class represents groups of dice, e.g. '4d6'"""
    def __init__(self, count: int, size: int):
        # FIXME should go back and change this class to support e.g. '3d6 + 2d4 + 1' as one 'Dice' object?
        self.count = count
        self.size = size

    @classmethod
    def from_string(cls, s: str):
        """E.g. 'd6' or '3d8'"""
        s = s.lower().split('d')
        if len(s) == 1:
            return cls(count=1, size=int(s[0]))
        if s[0] == '':
            return cls(count=1, size=int(s[1]))

        return cls(count=int(s[0]), size=int(s[1]))

    def upper_average(self):
        """This is the "average" given in D&D books"""
        return math.ceil((self.size * self.count + self.count) / 2)

    def roll(self):
        return sum([random.randint(1, self.size) for _ in range(self.count)])

    def __repr__(self):
        return '{}d{}'.format(self.count, self.size)


class AbilityScore(object):
    """In D&D, ability scores like Strength have a value and a modifier determined by that value.
    The modifier is what's actually added to your dice rolls. We typically refer to the modifier as
    a short name like 'STR' and the value as e.g. 'Strength'"""
    def __init__(self, name: str='Foobar', value: int=10, short_name: str=''):
        self.name = name
        if short_name == '':
            self.short_name = name[:3].upper()
        else:
            self.short_name = short_name
        self.value = int(value)

    @property
    def modifier(self) -> int:
        return int(self.value / 2) - 5

    def __add__(self, other):
        return self.modifier + other

    def __radd__(self, other):
        return self.modifier + other

    def __mul__(self, other):
        return self.modifier * other

    def __rmul__(self, other):
        return self.modifier * other

    def __repr__(self):
        return 'AbilityScore<name="{}", value="{}", short_name="{}">'.format(self.name, self.value, self.short_name)


class ChallengeRating(object):
    """How powerful a monster is determines how much experience it's worth."""
    rating_to_xp = json.load(open(path.join(package_directory, 'challenge_rating_to_xp.json'), 'r'))

    @classmethod
    def float_cr_to_cr(cls, cr: int):
        """Convert int-style CRs to [1/2, 1/4, 1/8, 0]-style Challenge Rating class objects."""
        if cr < 2:
            cr = '0'
        elif cr < 3:
            cr = '1/8'
        elif cr < 4:
            cr = '1/4'
        elif cr < 5:
            cr = '1/2'
        else:
            cr = str(int(math.floor(cr - 4)))
        return cls(cr)

    @staticmethod
    def damage_to_cr(damage: int) -> float:
        """Returns the expected CR based on the damage-per-round a creature can do. Uses "float cr",
        [0, -1, -2, -3] represent CRs of [1/2, 1/4, 1/8, 0] respectively. Better for averaging.
        Args:
            damage

        Returns:
            Float representing CR (NOT a Challenge Rating object)
        """
        bounds = [1, 3, 5, 8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86, 92, 98, 104, 116, 122, 140, 158, 176,
                  194, 212, 230, 248, 266, 284, 302, 320, 336, 352, 400, 500, 600]
        for i, bound in enumerate(bounds):
            if damage <= bound:
                return i + 1
        return len(bounds) + 1

    @staticmethod
    def attack_to_cr(attack: int) -> float:
        """Returns the expected CR based on creature's attack. Uses "float cr",
        [0, -1, -2, -3] represent CRs of [1/2, 1/4, 1/8, 0] respectively. Better for averaging.
        Args:
            attack

        Returns:
            Float representing CR (NOT a Challenge Rating object)
        """
        if attack < 3:
            return 1
        if attack == 3:
            return 4
        if attack == 4:
            return 7
        if attack == 5:
            return 8
        if attack == 6:
            return 10
        if attack == 7:
            return 13
        if attack == 8:
            return 17
        if attack == 9:
            return 20
        if attack == 10:
            return 12.5
        if attack == 11:
            return 27
        if attack == 12:
            return 29
        if attack == 13:
            return 32
        if attack == 14:
            return 35
        return 38

    @staticmethod
    def save_dc_to_cr(save_dc: int) -> float:
        """Returns the expected CR based on creature's save_dc. Uses "float cr",
        [0, -1, -2, -3] represent CRs of [1/2, 1/4, 1/8, 0] respectively. Better for averaging.
        Args:
            save_dc

        Returns:
            Float representing CR (NOT a Challenge Rating object)
        """
        if save_dc < 13:
            return 1
        if save_dc == 13:
            return 4
        if save_dc == 14:
            return 8
        if save_dc == 15:
            return 10
        if save_dc == 16:
            return 13
        if save_dc == 17:
            return 15.5
        if save_dc == 18:
            return 19.5
        if save_dc == 19:
            return 22.5
        if save_dc == 20:
            return 26
        if save_dc == 21:
            return 29
        if save_dc == 22:
            return 32
        if save_dc == 23:
            return 34
        return 38

    @staticmethod
    def hp_to_cr(hp: int) -> float:
        """Returns the expected CR based on creature's hit points. Uses "float cr",
        [0, -1, -2, -3] represent CRs of [1/2, 1/4, 1/8, 0] respectively. Better for averaging.
        Args:
            hp

        Returns:
            Float representing CR (NOT a Challenge Rating object)
        """
        bounds = [6, 12, 24, 48, 85, 100, 115, 130, 145, 160, 175, 190, 205, 220, 235, 250, 265, 280, 295, 310, 325,
                  340, 355, 400, 445, 490, 535, 580, 625, 670, 715, 760, 805, 850, 900, 1000, 1100, 1200, 1300]
        for i, bound in enumerate(bounds):
            if hp <= bound:
                return i + 1
        return len(bounds) + 1

    @staticmethod
    def ac_to_cr(ac: int) -> float:
        """Returns the expected CR based on creature's armor class. Uses "float cr",
        [0, -1, -2, -3] represent CRs of [1/2, 1/4, 1/8, 0] respectively. Better for averaging.
        Args:
            ac

        Returns:
            Float representing CR (NOT a Challenge Rating object)
        """
        if ac < 13:
            return 1
        if ac == 13:
            r = range(2, 8)
            return sum(r) / len(r)
        if ac == 14:
            r = range(8, 9)
            return sum(r) / len(r)
        if ac == 15:
            r = range(9, 12)
            return sum(r) / len(r)
        if ac == 16:
            r = range(12, 14)
            return sum(r) / len(r)
        if ac == 17:
            r = range(14, 17)
            return sum(r) / len(r)
        if ac == 18:
            r = range(17, 21)
            return sum(r) / len(r)
        if ac == 19:
            r = range(21, 26)
            return sum(r) / len(r)
        if ac > 19:
            return 29

    def __init__(self, rating: str):
        self.rating = str(rating)
        self.xp = self.rating_to_xp.get(rating, 0)

    def __str__(self):
        if self.xp != 0:
            return '{} ({:,} XP)'.format(self.rating, self.xp)
        else:
            return self.rating

    def __repr__(self):
        return 'ChallengeRating<rating="{}", xp="{}">'.format(self.rating, self.xp)


class Feature(object):
    """The special features and abilities a monster has, including features, actions, bonus actions, reactions,
    and legendary actions. This class substitutes values into its description template when updated in-between
    pairs of curly braces, e.g. '***Smite.*** Deal {STR + 2} damage' will substitute in a statblock's strength
    modifier and add 2 to it. This recalculated value is what is actually shown in the __repr__ of the object.
    Expressions in parentheses '()' are also recalculated here. Both the value and the expression for an expression
    in parentheses are in the final __repr__.
    Args:
        name:   Appears bolded and italicized at the start of an action/feature description.
        description_template:   Describes what the action does. Can have substitutable values in '{}'
        can_multiattack:    Should this be included in the multiattack action? Default for attacks True, other False
        effect_ac:  when calculating CR (see Statblock.challenge), this value is added to effective AC
        effect_hp:  when calculating CR, effective hp is recalculated as (1 + effect_hp) * hp
        effect_damage:  when calculating CR, effective damage is recalculated as (1 + effect_damage) * damage
        effect_attack:  when calculating CR, this value is added to effective attack bonus
        legendary_cost: If this feature is in a statblock's Actions, Bonus Actions, or Reactions and the statblock
                            has num_legendary_actions >= legendary_cost, this feature will be added to statblock's
                            legendary actions with the specified cost. If the cost is 0, this feature will not be
                            added to the legendary actions.
    """
    def __init__(self, name: str, description_template: str, can_multiattack: bool = None,
                 effect_ac: float=0, effect_hp: float=0, effect_damage: float=0, effect_attack: float=0,
                 legendary_cost: int=0):
        self.name = name
        self.description_template = description_template
        self.description = ''

        self.is_attack = False
        if 'weapon attack' in self.description_template.lower():
            self.is_attack = True

        self.can_multiattack = can_multiattack  # i.e., should this be included in the multiattack action?
        if can_multiattack is None:
            if self.is_attack:
                self.can_multiattack = True
            else:
                self.can_multiattack = False

        self.legendary_cost = legendary_cost

        self.effect_ac = effect_ac
        self.effect_hp = effect_hp
        self.effect_damage = effect_damage
        self.effect_attack = effect_attack

        # just grab the first one we see
        self.damage_formula = re.search(r'[+\-]?\d+\s+\(([A-z0-9+\-\s{}]+)\)[A-z0-9 ]+damage', self.description_template)
        if self.damage_formula is None:
            self.damage_formula = '-1'
        else:
            self.damage_formula = self.damage_formula.group(1)

        self.attack_bonus_formula = re.search(r'([+\-]\d+) to hit', self.description_template)
        if self.attack_bonus_formula is not None:
            self.attack_bonus_formula = self.attack_bonus_formula.group(1)
        else:
            self.attack_bonus_formula = re.search(r'({[^{}]+}) to hit', self.description_template)
            if self.attack_bonus_formula is not None:
                self.attack_bonus_formula = str(self.attack_bonus_formula.group(1))
            else:
                self.attack_bonus_formula = '-1'

        self.dc_formula = re.search(r'DC (\d+)', self.description_template)
        if self.dc_formula is not None:
            self.dc_formula = int(self.dc_formula.group(1))
        else:
            self.dc_formula = re.search(r'DC ({[^{}]+})', self.description_template)
            if self.dc_formula is not None:
                self.dc_formula = self.dc_formula.group(1)
            else:
                self.dc_formula = '-1'

    def update_description(self, values: dict):
        description = substitute_values(self.description_template, values)
        matches = re.findall(r'([+\-]?\d+\s+\(([A-z0-9+\-\s]+)\))', description)
        for match in matches:
            total = max(1, process_operands([op.strip() for op in match[1].split()], values))
            pretty = match[1].replace('+ -', '- ')  # turn adding negative numbers into subtracting positive
            pretty = pretty.replace('- -', '+ ')  # turn subtracting negative numbers into adding positive
            description = description.replace(match[0], '{} ({})'.format(total, pretty))

        self.description = description

    def legendary_str(self):
        if self.legendary_cost > 1:
            return '**{} (Costs {} Actions).** {}'.format(self.name,  self.legendary_cost, self.description)
        return '**{}.** {}'.format(self.name, self.description)

    def __str__(self):
        return '***{}.*** {}'.format(self.name, self.description)

    def __repr__(self):
        return 'Feature<name="{}", description="{}">'.format(self.name, self.description)


# Loads in some frequently referenced actions for tag tables to make use of
common_features = {}
with open(path.join(package_directory, 'common_features.csv')) as file_handle:
    reader = csv.DictReader(file_handle)
    for row in reader:
        name = str(row['name'])
        description_template = str(row['description_template'])

        legendary_cost = float(row['legendary_cost']) if row['legendary_cost'] else 0
        effect_ac = float(row['effect_ac']) if row['effect_ac'] else 0
        effect_hp = float(row['effect_hp']) if row['effect_hp'] else 0
        effect_damage = float(row['effect_damage']) if row['effect_damage'] else 0
        effect_attack = float(row['effect_attack']) if row['effect_attack'] else 0
        common_features[name] = Feature(name=name,
                                        description_template=description_template,
                                        legendary_cost=legendary_cost,
                                        effect_ac=effect_ac,
                                        effect_hp=effect_hp,
                                        effect_damage=effect_damage,
                                        effect_attack=effect_attack
                                        )


def parse_table(lines: list) -> OrderedDict:
    table = OrderedDict()

    header_line = lines[0]
    data_lines = lines[2:]

    column_names = [col.strip() for col in header_line.strip().strip('|').split('|')]
    for col in column_names:
        table[col] = []

    for line in data_lines:
        line = [val.strip() for val in line.strip().strip('|').split('|')]
        for i, col in enumerate(column_names):
            table[col].append(line[i])

    return table


def format_modifier(modifier: int) -> str:
    """Add a plus sign '+' in front of a modifier if it's positive."""
    modifier = int(modifier)
    if modifier >= 0:
        return '+' + str(modifier)
    return str(modifier)


def process_operands(operands: list, values: dict):
    """Basic arithmetic and variable substitution"""
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
            total += int(operand) * next_mul
            continue
        except ValueError:
            pass

        if re.search(r'\d*d\d+', operand):
            total += Dice.from_string(operand).upper_average() * next_mul
            next_mul = 1
            continue

        if operand in values.keys():
            try:
                total += values[operand]
                continue
            except Exception as e:
                print(e)
                print(operands)
                raise e

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


def substitute_values(template, values):
    """Fill in things in '{}', e.g. '{prof + STR + 8}'"""
    out_str = template
    operand_groups = re.findall(r'{([^{}]+)}',  template)
    totals = []
    for operands in operand_groups:
        operands = [op.strip() for op in operands.split() if op.strip()]
        totals.append(process_operands(operands, values))

    match = re.search(r'{([^{}]+)}', template)

    try:
        while match:
            out_str = out_str.replace(match.group(0), str(totals.pop(0)))
            match = re.search(r'{([^{}]+)}', out_str)

    except KeyError as e:
        print('Missing substitutable values for updating statblock template (e.g. {prof + STR}).')
        print(e)

    return out_str
