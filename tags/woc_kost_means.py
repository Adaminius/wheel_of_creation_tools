from utils import common_actions
from utils import Feature
from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'WoC: Kostlyavets Means'
table_description = \
"""While the undead can arise from any corpse improperly disposed of, "Kostlyavtsi" refers to a particularly powerful 
and intelligent group of vengeful ghosts. The dark powers of a Kostlyavets magi allow them to command lesser undead and 
to mantle new Kostlyavtsi, should they encounter (or produce) a body whose spirit has yet to depart. A Kostlyavets 
feeds the the anger and greed of such spirits until they are turned into their service, then preserves, 
enhances, and mutates their bodies and minds, giving them power and cunning beyond their reach in life. They are an 
ever-present threat in the Ring of Earth, and though their ultimate goals are unknown, they seem to be working toward
a common purpose.
"""


def apply(sb: Statblock) -> Statblock:
    sb.primary_type = 'undead'
    sb.secondary_type = 'Kostlyavets'
    sb.languages.append('Kostki')
    sb.languages.append('languages it knew life')
    sb.condition_immunities.add('poisoned')
    sb.add_damage_resistance('necrotic')
    sb.add_damage_resistance('necrotic')
    sb.add_damage_resistance('poison')
    sb.add_damage_resistance('poison')
    sb.add_damage_vulnerability('radiant')
    sb.darkvision += 60
    sb.actions.append(common_actions['Command Undead'])
    return sb
all_tags.append(Tag('Kostlyavets',
                    'undead type; Kostlyavets subtype; immunity to necrotic and poison damage; speaks Kostki and '
                    'whatever languages it knew in life; gains the Command Undead action; darkvision 60 ft.; '
                    'immunity to the poisoned condition;'
                    'vulnerability to radiant damage',
                    weight=0, on_apply=apply))


def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['INT'].value += 2
    return sb
all_tags.append(Tag('foul cunning', '+2 to Intelligence', on_apply=apply, stacks=True))


def apply(sb: Statblock) -> Statblock:
    sb.features.append(common_actions['Undead Fortitude'])
    sb.ability_scores['STR'].value += 4
    sb.ability_scores['CON'].value += 2
    return sb
all_tags.append(Tag('meaty', 'gain the Undead Fortitude feature; +4 Strength; +2 Constitution', on_apply=apply,
                    weight=40, overwritten_by={'undead form'}, overwrites={'undead form'}))


def apply(sb: Statblock) -> Statblock:
    sb.add_damage_resistance('piercing')
    sb.add_damage_resistance('slashing')
    sb.add_damage_vulnerability('bludgeoning')
    sb.ability_scores['DEX'].value += 4
    sb.ability_scores['CON'].value += 2
    return sb
all_tags.append(Tag('skeletal', 'vulnerability to bludgeoning damage; resistance to piercing and slashing damage; '
                                '+4 Dexterity; +2 Constitution',
                    on_apply=apply, weight=40, overwritten_by={'undead form'}, overwrites={'undead form'}))

all_tags = dict([(tag.name, tag) for tag in all_tags])
