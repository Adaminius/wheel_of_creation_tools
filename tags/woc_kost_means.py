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


def has_tag(sb: Statblock, name: str):
    for tag in sb.applied_tags:
        if tag.name == name:
            return True
    return False


def make_minion(name, type_, ac='{prof + 10}', damage='d4 + {prof}', speed=30, size='Medium', features=None,
                physical='{prof}', mental='0',
                vulnerabilities=None, damage_immunities=None, ranged=0, melee_type='bludgeoning',
                ranged_type='bludgeoning', condition_immunities=None):
    # vulnerable = f'&emsp;Vulnerable to {", ".join(vulnerabilities)}.\n\n' if vulnerabilities is not None else ''
    immune = f'{"/".join(damage_immunities)} damage ' if damage_immunities is not None else ''
    cond_immune = f'{"and " if damage_immunities else ""}{"/".join(condition_immunities)} conditions. ' if condition_immunities is not None else ''
    feature = f'&emsp;Has the {", ".join(features)} features.\n\n' if features is not None else ''
    ranged_attack = f' Ranged {ranged_type} {ranged}/{2 * ranged} ft.' if ranged > 0 else ''
    vuln = f', **{"/".join(vulnerabilities)}** damage once,' if vulnerabilities else ''
    text = f'\n\n' \
           f'**{name}** (*{size.capitalize()} {type_}*) \n\n' \
           f'&emsp;**AC** {ac}. **Speed** {speed} ft.\n\n' \
           f'{"&emsp;**Immune:** " if condition_immunities or damage_immunities else ""}{immune}{cond_immune}\n\n' \
           f'{feature}' \
           f'&emsp;**Add {physical} to attacks** and STR/DEX/CON rolls. ' \
           f'Add {mental} to INT/WIS/CHA rolls.\n\n' \
           f'&emsp;Melee {melee_type} 5 ft.{ranged_attack} All **attacks deal 5 ({damage})**.\n\n' \
           f'&emsp;Dies upon taking damage twice{vuln} or {ac} damage in one hit.\n\n'
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
        ac='6 + prof',
        damage='d4 + 2',
        speed=20,
        physical='{prof}',
        mental='{prof - 4}',
        vulnerabilities=['radiant'],
        damage_immunities=['poison', 'necrotic'],
        condition_immunities=['charmed', 'frightened', 'poisoned']
    )
    feat = Feature(name='Summon Zombie Entourage',
                   description_template='This creature can conjure a group of 2 (1d4 + 1) zombie minions 1/day. '
                                        'Each appears in an unoccupied space within 30 ft. of this creature. '
                                        'They follow this creature\'s mental commands '
                                        'and die if this creature dies or moves more than 1 mile away. One minion may '
                                        'take a turn after a player character ends their turn. Minions can\'t take '
                                        'more than one '
                                        'turn each round. ' 
                                        f'Their statistics are: {minion}',
                   can_multiattack=False,
                   effect_damage=.75,
                   effect_hp=.75,
                   )
    sb.actions.append(feat)
    return sb
all_tags.append(Tag('zombie escort', 'can conjure a small group of zombie minions',
                    on_apply=apply, weight=15, overwritten_by={'minions'}, overwrites={'minions'}))

def apply(sb: Statblock) -> Statblock:
    minion = make_minion(
        name='Skeleton Minion',
        size='Medium',
        type_='undead',
        ac='{10 + prof}',
        damage='d4 + 2',
        ranged=30,
        ranged_type='piercing',
        speed=30,
        physical='{prof}',
        mental='{prof - 4}',
        vulnerabilities=['bludgeoning'],
        damage_immunities=['poison', 'necrotic'],
        condition_immunities=['charmed', 'frightened', 'poisoned']
    )
    feat = Feature(name='Summon Skeletal Entourage',
                   description_template='This creature can conjure a group of 2 (1d4 + 1) skeleton minions 1/day. '
                                        'Each appears in an unoccupied space within 30 ft. of this creature. '
                                        'They follow this creature\'s mental commands '
                                        'and die if this creature dies or moves more than 1 mile away. One minion may '
                                        'take a turn after a player character ends their turn. Minions can\'t take '
                                        'more than one '
                                        'turn each round. ' 
                                        f'Their statistics are: {minion}',
                   can_multiattack=False,
                   effect_damage=.5,
                   effect_hp=.5,
                   )
    sb.actions.append(feat)
    return sb
all_tags.append(Tag('skeletal escort', 'can conjure a small group of skeleton minions',
                    on_apply=apply, weight=15, overwritten_by={'minions'}, overwrites={'minions'}))

# todo skeleton horde, summons like 3d4 + 3, larger effect on damage/hp
# todo zombie horde, summons like 3d4 + 3

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Elephantine Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of an elephant (CR 4), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).*'
                                        'The mount acts independently, but obeys the rider\'s mental commands.'
                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('elephantine mount', 'rides into battle on an enormous undead creature',
                    on_apply=apply, weight=4, overwritten_by={'mount'}, overwrites={'mount'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Cervine Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of a giant elk (CR 2), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).*'
                                        'The mount acts independently, but obeys the rider\'s mental commands.'
                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('cervine mount', 'rides into battle on a giant elk-like undead creature',
                    on_apply=apply, weight=8, overwritten_by={'mount'}, overwrites={'mount'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Arachniadian Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of a giant spider (CR 1), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).*'
                                        'The mount acts independently, but obeys the rider\'s mental commands.'
                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('arachnidian mount', 'rides into battle on a giant spider-like undead creature',
                    on_apply=apply, weight=10, overwritten_by={'mount'}, overwrites={'mount'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Batty Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of a giant bat (CR 1), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).*'
                                        'The mount acts independently, but obeys the rider\'s mental commands.'
                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('batty mount', 'rides into battle on a giant bat-like undead creature',
                    on_apply=apply, weight=10, overwritten_by={'mount'}, overwrites={'mount'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Screeching Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of a giant bat (CR 1), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).*'
                                        'The mount acts independently, but obeys the rider\'s mental commands.'
                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('screeching mount', 'rides into battle on a giant bat-like undead creature',
                    on_apply=apply, weight=10, overwritten_by={'mount'}, overwrites={'mount'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Chitinous Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of a giant bat (CR 1), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).*'
                                        'The mount acts independently, but obeys the rider\'s mental commands.'

                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('chitinous mount', 'rides into battle on a giant scorpion-like undead creature',
                    on_apply=apply, weight=10, overwritten_by={'mount'}, overwrites={'mount'}))

all_tags = dict([(tag.name, tag) for tag in all_tags])

# todo add 'scepters'/weapons: grant a basic melee or ranged attack with some kind of damage like fire/necrotic/cold/poison,
# + some other, stronger spell-like ability. break under some condition if a non-kostlyavets uses them. add to loot table?