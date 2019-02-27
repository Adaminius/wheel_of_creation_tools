from utils import common_features
from utils import Feature
from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'WoC: Fey Means'
table_description = ''


def apply(sb: Statblock) -> Statblock:
    sb.primary_type = 'fey'
    sb.add_damage_resistance('bludgeoning, piercing, and slashing damage from weapons not made of thokcha')
    sb.add_damage_vulnerability('psychic')
    sb.languages.append('Sylvan')
    min_scores = {
        'STR': 6,
        'DEX': 12,
        'CON': 6,
        'INT': 3,
        'WIS': 6,
        'CHA': 12
    }
    for name, score in min_scores.items():
        sb.ability_scores[name].value = max(sb.ability_scores[name].value, min_scores[name])
    return sb
all_tags.append(Tag('fey', 'Fey type; resistance to bludgeoning, piercing, and slashing damage from weapons not made '
                           'of thokcha; vulnerability to psychic damage; speaks Sylvan; set minimum ability scores',
                    weight=0, on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 2
    return sb
all_tags.append(Tag('beautiful', '+2 to Charisma', on_apply=apply))


all_tags = dict([(tag.name, tag) for tag in all_tags])
