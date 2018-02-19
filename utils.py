import random
import json
import pandas as pd
import re
import io
from collections import OrderedDict

# defaults = json.load('defaults.json')


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
        """This should be the 'average' given in WotC manuals."""
        return int(self.size / 2) + 1

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
    rating_to_xp = json.load(open('challenge_rating_to_xp.json', 'r'))

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
    def __init__(self, name, description_template, is_legendary=False, **kwargs):
        self.name = name
        self.description_template = description_template
        self.description = {}
        self.is_legendary = is_legendary
        self.update_description(**kwargs)

    def update_description(self, **kwargs):
        try:
            self.description = self.description_template.format(**kwargs)
        except KeyError as e:
            print('Missing values for updating action description template:')
            print(e)

    def __str__(self):
        if self.is_legendary:
            return '**{}.** {}'.format(self.name, self.description)
        return '***{}.*** {}'.format(self.name, self.description)

    def __repr__(self):
        return 'Action<name="{}", description="{}">'.format(self.name, self.description)


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
