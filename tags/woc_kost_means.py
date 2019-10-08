from utils import common_features
from utils import Feature
from statblock import Statblock
from statblock import Tag
from statblock import Loot

img_url = ''
all_tags = []
table_name = 'WoC: Kostlyavets Means'
table_description = \
"""While the undead can arise from any corpse improperly disposed of, "Kostlyavtsi" refers to a particularly powerful 
and intelligent group. The dark powers of a Kostlyavets magi allow them to command lesser undead and 
to mantle new Kostlyavtsi, should they encounter (or produce) a body whose spirit has yet to depart. A Kostlyavets 
feeds the the anger and greed of such spirits until they are turned into their service, then preserves, 
enhances, and mutates their bodies and minds, giving them power and cunning beyond their reach in life. They are an 
ever-present threat in the Ring of Earth, and though their ultimate goals are unknown, they seem to be working toward
a common purpose.
"""

def modify_loot_properties(sb: Statblock, loot_name, key, value):
    for loot in sb.loot:
        if loot.name.lower().strip() == loot_name.lower().strip():
            loot.properties[key] = value


def make_minion(name, type_, ac=10, damage='d6 + 1', speed=30, size='Medium', features=None, physical=2, mental=0,
                vulnerabilities=None, immunities=None, ranged=0):
    vulnerable = f' Vulnerable to {", ".join(vulnerabilities)}.' if vulnerabilities is not None else ''
    immune = f' Immune to {", ".join(immunities)}.' if immunities is not None else ''
    feature = f' Has the {", ".join(features)} features.' if features is not None else ''  # should always be something in parent statblock
    ranged_attack = f' Ranged {ranged}/{2 * ranged} ft.' if ranged > 0 else ''
    text = f'**{name}** *{size.capitalize()} {type_}*. AC {ac}. Speed {speed} ft.{vulnerable}{immune}{feature} Add ' \
           f'{physical} to all attacks and STR/DEX/CON skill checks and saving throws. Add {mental} ' \
           f'to all INT/WIS/CHA skill ' \
           f'checks and saving throws. Melee 5 ft.{ranged_attack} Deals 8 ({damage}) with all attacks. Dies when it ' \
           f'takes damage twice, takes damage of a type it is vulnerable to once, or is critically hit once.'
    return text


def apply(sb: Statblock) -> Statblock:
    sb.primary_type = 'undead'
    sb.secondary_type = 'Kostlyavets'
    sb.languages.append('Kostki')
    sb.languages.append('languages it knew life')
    sb.condition_immunities.add('poisoned')
    sb.knowledge_dc_mod += 3
    min_scores = {
        'STR': 10,
        'DEX': 4,
        'CON': 10,
        'INT': 12,
        'WIS': 8,
        'CHA': 8,
    }
    for name, score in min_scores.items():
        sb.ability_scores[name].value = max(sb.ability_scores[name].value, min_scores[name])
    sb.add_damage_resistance('necrotic')
    sb.add_damage_resistance('necrotic')
    sb.add_damage_resistance('poison')
    sb.add_damage_resistance('poison')
    sb.add_damage_vulnerability('radiant')
    sb.darkvision += 60
    sb.actions.append(common_features['Command Undead'])
    sb.loot.append(Loot('ink of shadows',
                        properties={'dc': lambda s: f'DC {s.base_knowledge_dc} Refine check with alchemist\'s '
                                                    f'supplies or calligrapher\'s supplies to extract.'}))
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
    sb.features.append(common_features['Undead Fortitude'])
    sb.ability_scores['STR'].value += 2
    sb.ability_scores['CON'].value += 4
    return sb
all_tags.append(Tag('meaty', 'gain the Undead Fortitude feature; +4 Constitution; +2 Strength', on_apply=apply,
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

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['STR'].value += 4
    sb.ability_scores['CON'].value += 2
    sb.add_damage_vulnerability('fire')
    sb.condition_immunities.add('paralyzed')
    sb.condition_immunities.add('frightened')
    sb.condition_immunities.add('charmed')
    feat = Feature(name='Horrifying Glare',
                   description_template='This creature targets one creature it can see within 60 feet of it. That '
                                        'creature must succeed on a DC {8 + prof + INT} Wisdom saving throw or '
                                        'become frightened until the end of this creature\'s next turn. If that '
                                        'creature fails the saving throw by 5 or more, it becomes paralyzed instead. '
                                        'A target that succeeds on the saving throw is immune to Horrifying Glare for '
                                        'the next 24 hours.',
                   can_multiattack=True,
                   legendary_cost=1,
                   )
    sb.actions.append(feat)
    return sb
all_tags.append(Tag('mummified', 'vulnerability to fire damage; immunity to the paralyzed, frightened, and charmed '
                                 'conditions; add a Horrifying Glare action; '
                                 '+4 Strength; +2 Constitution',
                    on_apply=apply, weight=40, overwritten_by={'undead form'}, overwrites={'undead form'}))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 4
    sb.ability_scores['WIS'].value += 2
    sb.add_damage_resistance('fire')
    sb.add_damage_resistance('acid')
    sb.add_damage_resistance('lightning')
    sb.add_damage_resistance('thunder')
    sb.add_damage_resistance('cold')
    sb.add_damage_resistance('cold')
    sb.add_damage_resistance('bludgeoning, piercing, and slashing damage from nonmagical attacks')
    sb.condition_immunities.add('paralyzed')
    sb.condition_immunities.add('frightened')
    sb.condition_immunities.add('charmed')
    sb.condition_immunities.add('exhaustion')
    sb.condition_immunities.add('grappled')
    sb.condition_immunities.add('petrified')
    sb.condition_immunities.add('poisoned')
    sb.condition_immunities.add('prone')
    sb.condition_immunities.add('restrained')
    feat = Feature(name='Incorporeal Movement',
                   description_template='This creature can move through other creatures and objects as if they were '
                                        'difficult terrain. It takes 5 (1d10) force damage if it ends its turn inside '
                                        'an object.')
    sb.features.append(feat)
    return sb
all_tags.append(Tag('ghostly', 'immunity to cold damage; resistance to acid, fire, lightning, and thunder damage; '
                               'resistance to bludgeoning, piercing, and slashing damage from nonmagical attacks; '
                               'immunity to many conditions; '
                               'add the Incorporeal Movement feature; '
                               '+4 Charisma; +2 Wisdom',
                    on_apply=apply, weight=40, overwritten_by={'undead form'}, overwrites={'undead form'}))

def apply(sb: Statblock) -> Statblock:
    minion = make_minion(
        name='Zombie Minion',
        type_='undead',
        ac=10,
        damage='d6 + 1',
        speed=20,
        physical=2,
        mental=-2,
        vulnerabilities=['radiant'],
        immunities=['poison', 'necrotic'],
    )
    feat = Feature(name='Overlord',
                   description_template='This creature can conjure a group 2 (1d4 + 1) zombie minions 1/day. Their '
                                        f'statistics are: {minion}',
                   can_multiattack=False)
    sb.actions.append(feat)
    return sb
all_tags.append(Tag('overlord', 'can conjure zombie minions',
                    on_apply=apply, weight=10, overwritten_by={'minions'}, overwrites={'minions'}))

all_tags = dict([(tag.name, tag) for tag in all_tags])
