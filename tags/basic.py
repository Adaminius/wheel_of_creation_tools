from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'Basic Operations'
table_description = 'Very basic operations, just in case you want randomness or if you don\'t want to mess with the ' \
                    'input statblock directly.'

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
