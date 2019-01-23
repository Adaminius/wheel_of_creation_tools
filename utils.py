import csv
import random
import json
import sys
import pandas as pd
import re
import io
import math
import logging
from collections import OrderedDict
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


def setup_logging(debug=True, filename=''):
    log_level = logging.DEBUG if debug else logging.INFO
    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    if filename:
        logging.basicConfig(filename=filename, level=log_level, format=log_format)
    else:
        logging.basicConfig(stream=sys.stderr, level=log_level, format=log_format)

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
    def __init__(self, count: int, size: int):
        # FIXME should go back and change this class to support e.g. '3d6 + 2d4 + 1' as one 'Dice' object
        self.count = count
        self.size = size

    @classmethod
    def from_string(cls, s: str):
        """E.g. 'd6' or '3d8'"""
        s = s.lower().split('d')
        if len(s) == 1:
            return cls(count=1, size=int(s[0]))

        return cls(count=int(s[0]), size=int(s[1]))

    def upper_average(self):
        """This should be the average given in WotC manuals"""
        return math.ceil((self.size * self.count + self.count) / 2)

    def roll(self):
        return sum([random.randint(1, self.size) for _ in range(self.count)])

    def __repr__(self):
        return '{}d{}'.format(self.count, self.size)


class AbilityScore(object):
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

    def __repr__(self):
        return 'AbilityScore<name="{}", value="{}", short_name="{}">'.format(self.name, self.value, self.short_name)


class ChallengeRating(object):
    rating_to_xp = json.load(open(path.join(package_directory, 'challenge_rating_to_xp.json'), 'r'))

    def __init__(self, rating: str):
        self.rating = str(rating)
        self.xp = self.rating_to_xp.get(rating, 0)

    def __str__(self):
        if self.xp != 0:
            '{} ({:,} XP)'.format(self.rating, self.xp)
        else:
            return self.rating

    def __repr__(self):
        return 'ChallengeRating<rating="{}", xp="{}">'.format(self.rating, self.xp)


class Action(object):
    def __init__(self, name: str, description_template: str, is_legendary: bool = False, **kwargs):
        self.name = name
        self.description_template = description_template
        self.description = ''
        self.is_legendary = is_legendary

    def update_description(self, values: dict):
        description = self.description_template

        try:
            operand_groups = re.findall(r'{([^{}]+)}', self.description_template)
            totals = []
            for operands in operand_groups:
                operands = [op.strip() for op in operands.split() if op.strip()]
                totals.append(process_operands(operands, values))

            match = re.search(r'{([^{}]+)}', description)
            while match:
                description = description.replace(match.group(0), str(totals.pop(0)))
                match = re.search(r'{([^{}]+)}', description)

        except KeyError as e:
            print('Missing values for updating action description template.')
            print(e)

        matches = re.findall(r'([+\-]?\d+\s+\(([A-z0-9+\-\s]+)\))', description)
        for match in matches:
            total = process_operands([op.strip() for op in match[1].split()], values)
            pretty = match[1].replace('+ -', '- ')  # turn adding negative numbers into subtracting positive
            pretty = pretty.replace('- -', '+ ')  # turn subtracting negative numbers into adding positive
            description = description.replace(match[0], '{} ({})'.format(total, pretty))

        self.description = description

    def __str__(self):
        if self.is_legendary:
            return '**{}.** {}'.format(self.name, self.description)
        return '***{}.*** {}'.format(self.name, self.description)

    def __repr__(self):
        return 'Action<name="{}", description="{}">'.format(self.name, self.description)


common_actions = {}
with open('common_actions.csv') as file_handle:
    reader = csv.DictReader(file_handle)
    for row in reader:
        name = str(row['name'])
        description_template = str(row['description_template'])
        if isinstance(row['is_legendary'], bool):
            is_legendary = row['is_legendary']
        else:
            is_legendary = 'alse' in row['is_legendary']
        common_actions[name] = Action(name=name, description_template=description_template, is_legendary=is_legendary)


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
    modifier = int(modifier)
    if modifier >= 0:
        return '+' + str(modifier)
    return str(modifier)


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
