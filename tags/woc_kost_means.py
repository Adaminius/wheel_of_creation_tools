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

escorts = {'zombie escort', 'skeletal escort', 'mummified escort', 'ghostly escort',
           'vampiric escort', 'ghoulish escort'}
hordes = {'zombie horde', 'skeletal horde', 'mummified horde', 'ghostly horde',
          'ghoulish horde'}
escorts_and_hordes = escorts.union(hordes)

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
    sb.features.append(common_features['Undead Fortitude'])
    sb.ability_scores['STR'].value += 2
    sb.ability_scores['CON'].value += 4
    return sb
all_tags.append(Tag('meaty', 'gain the Undead Fortitude feature; +4 Constitution; +2 Strength', on_apply=apply,
                    weight=40, overwritten_by={'undead form'}, overwrites={'undead form'}))

def apply(sb: Statblock) -> Statblock:
    sb.add_damage_resistance('piercing and slashing')
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
        ac='{7 + prof}',
        damage='d4 + {prof}',
        speed=20,
        physical='{prof}',
        mental='{prof - 4}',
        vulnerabilities=['radiant'],
        damage_immunities=['poison', 'necrotic'],
        condition_immunities=['charmed', 'frightened', 'poisoned']
    )
    feat = Feature(name='Summon Zombie Entourage',
                   description_template='This creature can conjure a group of 4 zombie minions 1/day. '
                                        'Each appears in an unoccupied space within 30 ft. of this creature. '
                                        'They follow this creature\'s mental commands '
                                        'and die if this creature dies, this creature moves more than 1 mile away, '
                                        'or at dawn of the next day. One minion may '
                                        'take a turn after a player character ends their turn. Minions can\'t take '
                                        'more than one '
                                        'turn each round. ' 
                                        f'Their statistics are: {minion}',
                   can_multiattack=False,
                   effect_damage=.5,
                   effect_hp=.3,
                   )
    sb.actions.append(feat)
    return sb
all_tags.append(Tag('zombie escort', 'can conjure a small group of zombie minions',
                    on_apply=apply, weight=15, overwritten_by={'minions'}, overwrites={'minions'}))

def apply(sb: Statblock) -> Statblock:
    minion = make_minion(
        name='Zombie Minion',
        type_='undead',
        ac='{7 + prof}',
        damage='d4 + {prof}',
        speed=20,
        physical='{prof}',
        mental='{prof - 4}',
        vulnerabilities=['radiant'],
        damage_immunities=['poison', 'necrotic'],
        condition_immunities=['charmed', 'frightened', 'poisoned']
    )
    feat = Feature(name='Summon Zombie Horde',
                   description_template='This creature can conjure a group of 2 (1d4 + 8) zombie minions 1/day. '
                                        'Each appears in an unoccupied space within 60 ft. of this creature. '
                                        'They follow this creature\'s mental commands '
                                        'and die if this creature dies, this creature moves more than 1 mile away, '
                                        'or at dawn of the next day. One minion may '
                                        'take a turn after a player character ends their turn. Minions can\'t take '
                                        'more than one '
                                        'turn each round. ' 
                                        f'Their statistics are: {minion}',
                   can_multiattack=False,
                   effect_damage=.75,
                   effect_hp=.4,
                   )
    sb.actions.append(feat)
    return sb
all_tags.append(Tag('zombie horde', 'can conjure a large group of zombie minions',
                    on_apply=apply, weight=10, overwritten_by={'minions'}, overwrites={'minions'}))

def apply(sb: Statblock) -> Statblock:
    minion = make_minion(
        name='Skeleton Minion',
        size='Medium',
        type_='undead',
        ac='{9 + prof}',
        damage='d4 + {prof}',
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
                   description_template='This creature can conjure a group of 4 skeleton minions 1/day. '
                                        'Each appears in an unoccupied space within 30 ft. of this creature. '
                                        'They follow this creature\'s mental commands '
                                        'and die if this creature dies, this creature moves more than 1 mile away, '
                                        'or at dawn of the next day. One minion may '
                                        'take a turn after a player character ends their turn. Minions can\'t take '
                                        'more than one '
                                        'turn each round. ' 
                                        f'Their statistics are: {minion}',
                   can_multiattack=False,
                   effect_damage=.5,
                   effect_hp=.3,
                   )
    sb.actions.append(feat)
    return sb
all_tags.append(Tag('skeletal escort', 'can conjure a small group of skeleton minions',
                    on_apply=apply, weight=15, overwritten_by={'minions'}, overwrites={'minions'}))

def apply(sb: Statblock) -> Statblock:
    minion = make_minion(
        name='Skeleton Minion',
        size='Medium',
        type_='undead',
        ac='{9 + prof}',
        damage='d4 + {prof}',
        ranged=30,
        ranged_type='piercing',
        speed=30,
        physical='{prof}',
        mental='{prof - 4}',
        vulnerabilities=['bludgeoning'],
        damage_immunities=['poison', 'necrotic'],
        condition_immunities=['charmed', 'frightened', 'poisoned']
    )
    feat = Feature(name='Summon Skeletal Horde',
                   description_template='This creature can conjure a group of 2 (1d4 + 8) skeleton minions 1/day. '
                                        'Each appears in an unoccupied space within 30 ft. of this creature. '
                                        'They follow this creature\'s mental commands '
                                        'and die if this creature dies, this creature moves more than 1 mile away, '
                                        'or at dawn of the next day. One minion may '
                                        'take a turn after a player character ends their turn. Minions can\'t take '
                                        'more than one '
                                        'turn each round. ' 
                                        f'Their statistics are: {minion}',
                   can_multiattack=False,
                   effect_damage=.75,
                   effect_hp=.4,
                   )
    sb.actions.append(feat)
    return sb
all_tags.append(Tag('skeletal horde', 'can conjure a large group of skeleton minions',
                    on_apply=apply, weight=10, overwritten_by={'minions'}, overwrites={'minions'}))

def apply(sb: Statblock) -> Statblock:
    minion = make_minion(
        name='Ghost Minion',
        size='Medium',
        type_='undead',
        ac='{12 + prof}',
        damage='d4 + {prof}',
        ranged=30,
        ranged_type='cold',
        speed=40,
        physical='{prof - 2}',
        mental='{prof}',
        vulnerabilities=['psychic'],
        damage_immunities=['poison', 'necrotic', 'cold'],
        condition_immunities=['poisoned', 'grappled', 'prone']
    )
    feat = Feature(name='Summon Ghostly Entourage',
                   description_template='This creature can conjure a group of 4 ghost minions 1/day. '
                                        'Each appears in an unoccupied space within 30 ft. of this creature. '
                                        'They follow this creature\'s mental commands '
                                        'and die if this creature dies, this creature moves more than 1 mile away, '
                                        'or at dawn of the next day. One minion may '
                                        'take a turn after a player character ends their turn. Minions can\'t take '
                                        'more than one '
                                        'turn each round. ' 
                                        f'Their statistics are: {minion}',
                   can_multiattack=False,
                   effect_damage=.5,
                   effect_hp=.3,
                   )
    sb.actions.append(feat)
    return sb
all_tags.append(Tag('ghostly escort', 'can conjure a small group of ghost minions',
                    on_apply=apply, weight=15, overwritten_by={'minions'}, overwrites={'minions'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Elephantine Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of an elephant (CR 4), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).* '
                                        'The mount acts independently, but obeys the rider\'s mental commands.'
                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('elephantine mount', 'rides into battle on an elephant-like undead creature',
                    on_apply=apply, weight=4, overwritten_by={'mount'}, overwrites={'mount'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Cervine Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of a giant elk (CR 2), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).* '
                                        'The mount acts independently, but obeys the rider\'s mental commands.'
                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('cervine mount', 'rides into battle on a giant elk-like undead creature',
                    on_apply=apply, weight=8, overwritten_by={'mount'}, overwrites={'mount'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Arachnidian Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of a giant spider (CR 1), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).* '
                                        'The mount acts independently, but obeys the rider\'s mental commands.'
                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('arachnidian mount', 'rides into battle on a giant spider-like undead creature',
                    on_apply=apply, weight=8, overwritten_by={'mount'}, overwrites={'mount'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Screeching Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of a giant bat (CR 1), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).* '
                                        'The mount acts independently, but obeys the rider\'s mental commands.'
                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('screeching mount', 'rides into battle on a giant bat-like undead creature',
                    on_apply=apply, weight=8, overwritten_by={'mount'}, overwrites={'mount'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Chitinous Mount',
                   description_template='Rides into battle astride a creature of sewn flesh and bone. '
                                        'This mount has the statistics of a giant scorpion (CR 1), except that it is undead '
                                        'and immune to necrotic and poison damage and the frightened, charmed, '
                                        'and poisoned conditions *(Note: the mount\'s CR is **not** included in the '
                                        'calculation for this creature\'s CR).* '
                                        'The mount acts independently, but obeys the rider\'s mental commands.'

                   )
    sb.features.append(feat)
    return sb
all_tags.append(Tag('chitinous mount', 'rides into battle on a giant scorpion-like undead creature',
                    on_apply=apply, weight=8, overwritten_by={'mount'}, overwrites={'mount'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Staff of Flames',
                   description_template='*Melee Weapon Attack:* +{prof + INT} to hit, reach 5 ft., one target. '
                                        '*Hit:* 7 ({max(prof - 1, 1)}d{size_die_size} + {INT}) fire damage. ',
                   can_multiattack=True,
                   )
    sb.actions.append(feat)
    feat = Feature(name='Fiery Bolt',
                   description_template='*Ranged Weapon Attack:* +{prof + INT} to hit, range 30/60 ft., one target. '
                                        '*Hit:* 7 ({max(prof - 1, 1)}d{size_die_size} + {INT}) fire damage. ',
                   can_multiattack=True,
                   )
    sb.actions.append(feat)
    feat = Feature(name='Flaming Sphere',
                   description_template='While a kostlyavets wields a staff of flames, it may cast *flaming sphere* at '
                                        'will at {max(prof, 2)}th level, requiring no material components.')
    sb.actions.append(feat)
    sb.loot.append(Loot('staff of flames',
                        properties={'wieldable': lambda s:
                                    f'If wielded by a creature other than a kostlyavets, acts as a quarterstaff '
                                    f'that deals {max(s.proficiency - 1, 1)}d6 fire damage instead of its '
                                    f'regular damage and turns to ash '
                                    f'at the end of the first combat it hits an enemy in.'
                                    }))
    return sb
all_tags.append(Tag('staff of shadows',
                    'add necrotic attacks; cast darkness at will',
                    on_apply=apply, overwrites={'kost_weapon'}, overwritten_by={'kost_weapon'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Staff of Silence',
                   description_template='*Melee Weapon Attack:* +{prof + INT} to hit, reach 5 ft., one target. '
                                        '*Hit:* 7 ({max(prof - 1, 1)}d{size_die_size} + {INT}) necrotic damage. ',
                   can_multiattack=True,
                   )
    sb.actions.append(feat)
    feat = Feature(name='Shadow Bolt',
                   description_template='*Ranged Weapon Attack:* +{prof + INT} to hit, range 30/60 ft., one target. '
                                        '*Hit:* 7 ({max(prof - 1, 1)}d{size_die_size} + {INT}) necrotic damage. ',
                   can_multiattack=True,
                   )
    sb.actions.append(feat)
    feat = Feature(name='Silence',
                   description_template='While a kostlyavets wields a staff of shadows, it may cast *silence* at '
                                        'will, requiring no material components.')
    sb.actions.append(feat)
    sb.loot.append(Loot('staff of shadows',
                        properties={'wieldable': lambda s:
                                    f'If wielded by a creature other than a kostlyavets, acts as a quarterstaff '
                                    f'that deals {max(s.proficiency - 1, 1)}d6 necrotic damage instead of its '
                                    f'regular damage and turns to ash '
                                    f'at the end of the first combat it hits an enemy in.'
                                    }))
    return sb
all_tags.append(Tag('staff of silence',
                    'add necrotic attacks; cast silence at will',
                    on_apply=apply, overwrites={'kost_weapon'}, overwritten_by={'kost_weapon'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Ethereal Blade',
                   description_template='*Melee Weapon Attack:* +{prof + INT} to hit, reach 5 ft., one target. '
                                        '*Hit:* 7 ({max(prof - 1, 1)}d{size_die_size} + {INT}) cold damage. ',
                   can_multiattack=True,
                   )
    sb.actions.append(feat)
    feat = Feature(name='Icy Touch',
                   description_template='*Ranged Weapon Attack:* +{prof + INT} to hit, range 30/60 ft., one target. '
                                        '*Hit:* 7 ({max(prof - 1, 1)}d{size_die_size} + {INT}) cold damage. ',
                   can_multiattack=True,
                   )
    sb.actions.append(feat)
    feat = Feature(name='Misty Step',
                   description_template='While a kostlyavets wields an ethereal blade, it may cast *misty step* '
                                        'at will, requiring no material components.',
                   effect_hp=.1
                   )
    sb.bonus_actions.append(feat)
    sb.loot.append(Loot('ethereal blade',
                        properties={'wieldable': lambda s:
                                    f'If wielded by a creature other than a kostlyavets, acts as a longsword '
                                    f'that deals {max(s.proficiency - 1, 1)}d8 cold damage instead of its '
                                    f'regular damage and turns to ash '
                                    f'at the end of the first combat it hits an enemy in.'
                                    }))
    return sb
all_tags.append(Tag('ethereal blade',
                    'add cold attacks; cast misty step at will',
                    on_apply=apply, overwrites={'kost_weapon'}, overwritten_by={'kost_weapon'}, weight=12,
                    requires={'ghostly'}))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Burning Blade',
                   description_template='*Melee Weapon Attack:* +{prof + INT} to hit, reach 5 ft., one target. '
                                        '*Hit:* 7 ({max(prof - 1, 1)}d{size_die_size} + {INT}) fire damage. ',
                   can_multiattack=True,
                   )
    sb.actions.append(feat)
    feat = Feature(name='Fiery Bolt',
                   description_template='*Ranged Weapon Attack:* +{prof + INT} to hit, range 30/60 ft., one target. '
                                        '*Hit:* 7 ({max(prof - 1, 1)}d{size_die_size} + {INT}) fire damage. ',
                   can_multiattack=True,
                   )
    sb.actions.append(feat)
    feat = Feature(name='Flaming Sphere',
                   description_template='While a kostlyavets wields a burning blade, it may cast *flaming sphere*'
                                        ' at {max(2, prof)}th level'
                                        'at will, requiring no material components.',
                   effect_damage=.25
                   )
    sb.actions.append(feat)
    sb.loot.append(Loot('burning blade',
                        properties={'wieldable': lambda s:
                                    f'If wielded by a creature other than a kostlyavets, acts as a longsword '
                                    f'that deals {max(s.proficiency - 1, 1)}d8 fire damage instead of its '
                                    f'regular damage and turns to ash '
                                    f'at the end of the first combat it hits an enemy in.'
                                    }))
    return sb
all_tags.append(Tag('burning blade',
                    'add fire attacks; cast burning blade at will',
                    on_apply=apply, overwrites={'kost_weapon'}, overwritten_by={'kost_weapon'}, weight=12,))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Vampiric Sacrifice',
                   description_template='When a minion under this creature\'s control within 60 ft. would take damage, '
                                        'this creature may sacrifice it to '
                                        'gain 5 ({max(prof - 1, 1)}d8 + {max(prof - 1, 1)}) temporary hitpoints. '
                                        'These temporary hitpoints '
                                        'are lost at dawn.',
                   )
    sb.reactions.append(feat)
    return sb
all_tags.append(Tag('vampiric rune',
                    'sacrifice a minion to gain temp hp',
                    on_apply=apply, overwrites={'rune'}, overwritten_by={'rune'}, weight=12,
                    requires=escorts_and_hordes))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Abjuring Sacrifice',
                   description_template='This creature may sacrifice a minion under its control within 60 ft. to '
                                        'cast *counterspell* at {max(prof, 3)}th level.',
                   )
    sb.reactions.append(feat)
    return sb
all_tags.append(Tag('abjuring rune',
                    'sacrifice a minion to cast counterspell',
                    on_apply=apply, overwrites={'rune'}, overwritten_by={'rune'}, weight=12,
                    requires=escorts_and_hordes))


all_tags = dict([(tag.name, tag) for tag in all_tags])


# todo add 'scepters'/weapons: grant a basic melee or ranged attack with some kind of damage like fire/necrotic/cold/poison,
# + some other, stronger spell-like ability. break under some condition if a non-kostlyavets uses them.
# spell should generally alter the battlefield in some way; at will/multiple use

# to add:
# web
# warding wind?

# todo fly speed for ghostly?
# todo mummy minions

# todo add trinkets: single/limited use spell
# counterspell?

# todo add ritual knives (or something like that): sacrifice minions for effects
# todo scaling REALLy needs work
# todo scaling REALLY needs work
# todo scaling REALLY needs work
# todo scaling REALLY needs work
# todo scaling really needs work
# todo scaling really needs work
# todo scaling really needs work
# todo scaling really needs work
# todo scaling really needs work
