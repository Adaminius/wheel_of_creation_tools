from statblock import Statblock
from statblock import Tag
from utils import Feature

all_tags = []
table_name = 'Misc'
table_description = 'Simple or unflavored operations'

def apply(sb: Statblock) -> Statblock:
    sb.legendary_actions.append(Feature('Attack', 'This creature makes a melee attack.', effect_damage=.5))
    return sb
all_tags.append(Tag('legendary attacker', effect_text='add an attack legendary action', weight=10,
                    stacks=True, on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.num_legendary += 1
    return sb
all_tags.append(Tag('legendary', effect_text='increase number of legendary actions by 1', weight=10,
                    stacks=True, on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.size += 1
    return sb
all_tags.append(Tag('+Size', effect_text='increase size by 1 step', weight=10,
                    stacks=True, on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.size -= 1
    return sb
all_tags.append(Tag('-Size', effect_text='decrease size by 1 step', weight=10,
                    stacks=True, on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.bonus_multiattacks += 1
    return sb
all_tags.append(Tag('+Multiattack', effect_text='can make 1 additional attack with its multiattack action', weight=10,
                    stacks=True, on_apply=apply))


def apply(sb: Statblock) -> Statblock:
    sb.bonus_multiattacks -= 1
    return sb
all_tags.append(Tag('-Multiattack', effect_text='can make 1 less attack with its multiattack action', weight=10,
                    stacks=True, on_apply=apply))


def basic_add_apply(ability_score):
    def apply(sb: Statblock) -> Statblock:
        sb.ability_scores[ability_score].value += 1
        return sb
    return apply


all_tags.append(Tag('+Strength', effect_text='+1 Strength', weight=10, stacks=True, on_apply=basic_add_apply('STR')))
all_tags.append(Tag('+Dexterity', effect_text='+1 Dexterity', weight=10, stacks=True, on_apply=basic_add_apply('DEX')))
all_tags.append(Tag('+Constitution', effect_text='+1 Constitution', weight=10, stacks=True, on_apply=basic_add_apply('CON')))
all_tags.append(Tag('+Intelligence', effect_text='+1 Intelligence', weight=10, stacks=True, on_apply=basic_add_apply('INT')))
all_tags.append(Tag('+Wisdom', effect_text='+1 Wisdom', weight=10, stacks=True, on_apply=basic_add_apply('WIS')))
all_tags.append(Tag('+Charisma', effect_text='+1 Charisma', weight=10, stacks=True, on_apply=basic_add_apply('CHA')))


def basic_subtract_apply(ability_score):
    def apply(sb: Statblock) -> Statblock:
        sb.ability_scores[ability_score].value -= 1
        return sb
    return apply


all_tags.append(Tag('-Strength', effect_text='-1 Strength', weight=10, stacks=True, on_apply=basic_subtract_apply('STR')))
all_tags.append(Tag('-Dexterity', effect_text='-1 Dexterity', weight=10, stacks=True, on_apply=basic_subtract_apply('DEX')))
all_tags.append(Tag('-Constitution', effect_text='-1 Constitution', weight=10, stacks=True, on_apply=basic_subtract_apply('CON')))
all_tags.append(Tag('-Intelligence', effect_text='-1 Intelligence', weight=10, stacks=True, on_apply=basic_subtract_apply('INT')))
all_tags.append(Tag('-Wisdom', effect_text='-1 Wisdom', weight=10, stacks=True, on_apply=basic_subtract_apply('WIS')))
all_tags.append(Tag('-Charisma', effect_text='-1 Charisma', weight=10, stacks=True, on_apply=basic_subtract_apply('CHA')))

all_tags = dict([(tag.name, tag) for tag in all_tags])
