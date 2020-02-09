from utils import common_features
from utils import Feature
from statblock import Statblock
from statblock import Tag
from statblock import Loot

all_tags = []
table_name = 'WoC: Tuguai Means'
table_description = 'Coming Soon!'
img_url = ''


def modify_loot_properties(sb: Statblock, loot_name, key, value):
    for loot in sb.loot:
        if loot.name.lower().strip() == loot_name.lower().strip():
            loot.properties[key] = value

def make_destructible_feature(name: str, already_has_destructible=False):
    if already_has_destructible:
        return Feature(name=f'Destructible: {name}', description_template=f'As above, but with *{name}*.')
    return Feature(name=f'Destructible: {name}', description_template=
                   f'If a creature knows the name of the tag which grants this creature its *{name}* feature, it can '
                   f'choose to declare a strike against the part of this creature\'s anatomy which grants that '
                   f'feature before rolling. The attack is always considered to be against three-quarters cover. '
                   f'After two successful hits or one critical hit against *{name}*, this creature can no longer use '
                   f'*{name}*. Damage is dealt as normal.')

def has_any_destructible(sb: Statblock):
    for feat in sb.features:
        if feat.name.startswith('Destructible:'):
            return True
    return False

def apply(sb: Statblock) -> Statblock:
    sb.primary_type = 'construct'
    sb.secondary_type = 'tuguai'
    sb.languages.append('understands Leitian but can\'t speak (or really be reasoned with)')
    sb.knowledge_dc_mod += 3
    min_scores = {
        'STR': 12,
        'DEX': 4,
        'CON': 10,
        'INT': 6,
        'WIS': 8,
        'CHA': 6
    }
    for name, score in min_scores.items():
        sb.ability_scores[name].value = max(sb.ability_scores[name].value, min_scores[name])
    sb.features.append(common_features['Magic Resistance'])
    sb.add_damage_resistance('poison')
    sb.add_damage_resistance('poison')
    sb.add_damage_resistance('necrotic')
    sb.add_damage_resistance('necrotic')
    sb.condition_immunities.add('charmed')
    sb.condition_immunities.add('exhaustion')
    sb.condition_immunities.add('frightened')
    sb.condition_immunities.add('paralyzed')
    sb.condition_immunities.add('petrified')
    sb.condition_immunities.add('poisoned')
    sb.loot.append(Loot('jadeheart',
                        properties={'dc': lambda s: f'DC {s.base_knowledge_dc} Crafting check with jeweler\'s tools or '
                                                    f'tinker\'s tools to extract'}))
    sb.loot.append(Loot('celadon plating', properties={'dc': lambda s: f'DC {s.base_knowledge_dc} Refine check with '
                                                                       f'mason\'s tools or smith\'s tools to extract'}))
    return sb
all_tags.append(Tag('tuguai', 'Construct type; tuguai subtype; magic reistance; understands Leitian; immunity to '
                              'several conditions; immunity to necrotic and poison damage; '
                              'set minimum ability scores',
                    weight=0, on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Fire Ray (Recharge 5-6)',
                   description_template='This creature raises an appendage and unleashes a gout of flame in a 60-foot '
                                        'line that is 5 feet wide. Each creature in the line must make a '
                                        'DC {8 + CON + prof} Dexterity saving throw, taking 1 ({prof}d{size_die_size}) '
                                        'fire damage on a failed save, or half as much damage on a successful one. '
                                        'In addition, terrain under the area of the ray is ignited, dealing '
                                        'd{size_die_size} fire damage to any creature that ends its turn in the area. '
                                        'The fire '
                                        'expires when this ability recharges, when a creature uses its action to '
                                        'extinguish a 5-foot square of the flames, or when the Tuguai is killed.',
                   can_multiattack=False,
                   )
    sb.actions.append(feat)
    sb.add_damage_resistance('fire')
    modify_loot_properties(sb, 'jadeheart', 'elemental', lambda s: 'elemental')
    sb.features.append(make_destructible_feature('Fire Ray',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('fire ray',
                    'add a Fire Ray action; add resistance to fire damage',
                    on_apply=apply, overwrites={'ranged_arm'}, overwritten_by={'ranged_arm'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Lightning Ray (Recharge 5-6)',
                   description_template='This creature raises an appendage and unleashes a blast of lightning in a 60-foot '
                                        'line that is 5 feet wide. Each creature in the line must make a '
                                        'DC {8 + CON + prof} Dexterity saving throw, taking 1 ({prof}d{size_die_size}) '
                                        'lightning damage on a failed save, or half as much damage on a successful one. '
                                        'In addition, any creature that is not immune to lightning and that fails this '
                                        'saving throw can\'t take reactions until the start of this creature\'s next '
                                        'turn and drop whatever they are holding.',
                   can_multiattack=False,
                   )
    sb.actions.append(feat)
    sb.add_damage_resistance('lightning')
    modify_loot_properties(sb, 'jadeheart', 'elemental', lambda s: 'elemental')
    sb.features.append(make_destructible_feature('Lightning Ray',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('lightning ray',
                    'add a Lightning Ray action; add resistance to lightning damage',
                    on_apply=apply, overwrites={'ranged_arm'}, overwritten_by={'ranged_arm'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Ice Ray (Recharge 5-6)',
                   description_template='This creature raises an appendage and unleashes an icy blast in a 60-foot '
                                        'line that is 5 feet wide. Each creature in the line must make a '
                                        'DC {8 + CON + prof} Dexterity saving throw, taking 1 ({prof}d{size_die_size}) '
                                        'cold damage on a failed save, or half as much damage on a successful one. '
                                        'In addition, terrain under the area of the ray is frozen, becoming difficult '
                                        'terrain. '
                                        'The ice melts after 10 minutes or when the Tuguai is killed.',
                   can_multiattack=False,
                   )
    sb.actions.append(feat)
    sb.add_damage_resistance('cold')
    modify_loot_properties(sb, 'jadeheart', 'elemental', lambda s: 'elemental')
    sb.features.append(make_destructible_feature('Ice Ray',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('ice ray',
                    'add a Ice Ray action; add resistance to cold damage',
                    on_apply=apply, overwrites={'ranged_arm'}, overwritten_by={'ranged_arm'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Explosive Cannon (Recharge 5-6)',
                   description_template='*Ranged Weapon Attack:* +{prof + DEX} to hit, range 30/120 ft., one target. '
                                        '*Hit:* 7 (1d{size_die_size} + {DEX}) bludgeoning damage. Hit or miss, the '
                                        'projectile explodes. The target and each creature within 5 feet of it must '
                                        'succeed on a Dexterity saving throw or take 5 ({prof}d6) fire damage. This '
                                        'attack deals double damage to structures.',
                   can_multiattack=False,
                   )
    sb.actions.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'stout', lambda s: 'stout')
    sb.features.append(make_destructible_feature('Explosive Cannon',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('explosive cannon',
                    'add an Explosive Cannon action',
                    on_apply=apply, overwrites={'ranged_arm'}, overwritten_by={'ranged_arm'}, weight=8))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Whirring Blades',
                   description_template='*Melee Weapon Attack:* +{prof + STR} to hit, reach 5 ft., one target. '
                                        '*Hit:* 7 (1d{size_die_size} + {STR}) slashing damage. If this attack hits, '
                                        'this creature can make up to 2 additional Whirring Blades attacks '
                                        '(additional attack rolls still required) against the target. '
                                        'This creature can\'t make attacks this way again this turn.',
                   can_multiattack=True,
                   effect_damage=.5,
                   )
    sb.actions.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'intricate', lambda s: 'intricate')
    sb.features.append(make_destructible_feature('Whirring Blades',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('whirring blades',
                    'add a Whirring Blades melee attack',
                    on_apply=apply, overwrites={'melee_arm'}, overwritten_by={'melee_arm'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Psionic Blades',
                   description_template='*Melee Weapon Attack:* +{prof + STR} to hit, reach 5 ft., one target. '
                                        '*Hit:* 7 (1d{size_die_size} + {STR}) psychic damage. The target\'s '
                                        'AC for this attack is 10 + its Intelligence modifier unless it is wearing '
                                        'magical armor or armor made out of celadon.',
                   can_multiattack=True,
                   effect_damage=.25,
                   )
    sb.actions.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'psionic', lambda s: 'psionic')
    sb.features.append(make_destructible_feature('Psionic Blades',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('psionic blades',
                    'add a Psionic Blades melee attack',
                    on_apply=apply, overwrites={'melee_arm'}, overwritten_by={'melee_arm'}, weight=4))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Sledgehammer',
                   description_template='*Melee Weapon Attack:* +{prof + STR} to hit, reach 5 ft., one target. '
                                        '*Hit:* 7 (1d{size_die_size} + {STR}) bludgeoning damage. If the target is a '
                                        'creature, that creature must make a DC {STR + prof + 8} Strength '
                                        'saving throw or be knocked prone.',
                   can_multiattack=True,
                   effect_damage=.5,
                   )
    sb.actions.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'stout', lambda s: 'stout')
    sb.features.append(make_destructible_feature('Sledgehammer',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('sledgehammer',
                    'add a Sledgehammer melee attack',
                    on_apply=apply, overwrites={'melee_arm'}, overwritten_by={'melee_arm'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Barbed Claws',
                   description_template='*Melee Weapon Attack:* +{prof + STR} to hit, reach 5 ft., one target. '
                                        '*Hit:* 7 (1d{size_die_size} + {STR}) piercing damage. If the target is a '
                                        'creature, it is grappled (escape DC {STR + prof + 8}). Until the grapple '
                                        'ends, this creature can\'t use this attack on a different creature.',
                   can_multiattack=True,
                   effect_damage=.5,
                   )
    sb.actions.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'intricate', lambda s: 'intricate')
    sb.features.append(make_destructible_feature('Barbed Claws',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('barbed claws',
                    'add a Barbed Claws melee attack',
                    on_apply=apply, overwrites={'melee_arm'}, overwritten_by={'melee_arm'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Antimagic Cone',
                   description_template='This creature\'s gaze creates an area of antimagic, as in the antimagic field '
                                        'spell, in a 60-foot cone. At the start of each of its turns, this creature '
                                        'decides which way the cone faces and whether the cone is active.',
                   effect_hp=.25,
                   )
    sb.features.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'antimagical', lambda s: 'antimagical')
    sb.features.append(make_destructible_feature('Antimagic Cone',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('antimagic cone',
                    'add an Antimagic Cone feature',
                    on_apply=apply, overwrites={'eye'}, overwritten_by={'eye'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Psionic Dampening Array',
                   description_template='All non-construct, non-undead creatures within 60 feet of this creature make '
                                        'attack rolls, saving throws, and skill checks based on Intelligence, Wisdom, '
                                        'or Charisma at disadvantage. All psychic damage dealt to or by '
                                        'any creatures in the field is halved.',
                   effect_hp=.25,
                   )
    sb.features.append(feat)
    sb.features.append(make_destructible_feature('Psionic Dampening Array',
                                                 already_has_destructible=has_any_destructible(sb)))
    modify_loot_properties(sb, 'jadeheart', 'psionic', lambda s: 'psionic')
    return sb
all_tags.append(Tag('psionic dampening array',
                    'add the Psionic Dampening Array feature',
                    on_apply=apply, overwrites={'field'}, overwritten_by={'field'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Vortex Engine',
                   description_template='Until the start of its next turn, this creature generates a barrier of '
                                        'rushing wind (30 miles per hour) in a 10-foot radius around '
                                        'this creature that moves with it. All '
                                        'ranged attacks that pass through, in, or out of the wind have disadvantage. '
                                        'Creatures within the wind are deafened. The area is difficult for terrain for '
                                        'creatures other than this creature. Flames in the area are extinguished. '
                                        'Gas or vapor in the area is dispersed.',
                   effect_hp=.25,
                   )
    sb.bonus_actions.append(feat)
    sb.features.append(make_destructible_feature('Vortex Engine', already_has_destructible=has_any_destructible(sb)))
    modify_loot_properties(sb, 'jadeheart', 'elemental', lambda s: 'elemental')
    return sb
all_tags.append(Tag('vortex engine',
                    'add the Vortex Engine bonus action',
                    on_apply=apply, overwrites={'field'}, overwritten_by={'field'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Cloaking Field',
                   description_template='This creature and anything it carries becomes invisible until it attacks or '
                                        'uses a spell or spell-like ability.',
                   effect_hp=.25,
                   )
    sb.bonus_actions.append(feat)
    sb.features.append(make_destructible_feature('Cloaking Field',
                                                 already_has_destructible=has_any_destructible(sb)))
    modify_loot_properties(sb, 'jadeheart', 'shadowy', lambda s: 'shadowy')
    return sb
all_tags.append(Tag('cloaking field',
                    'turn invisible as a bonus action',
                    on_apply=apply, overwrites={'field'}, overwritten_by={'field'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Deploy Sentry Wards',
                   description_template='(2/short rest) This creature deploys d4 small runestones with AC 5 and 5 '
                                        'hitpoints '
                                        'each into unoccupied spaces this creature can see within 60 ft. '
                                        'Each runestone has truesight 15 ft., cannot see further than 15 ft., and '
                                        'has no other senses. While this creature is within 1 mile of a runestone it '
                                        'deployed, it can see through the runestone in addition to its own senses. '
                                        'The runestones cease to function if this creature uses this ability again.',
                   effect_hp=.25,
                   )
    sb.actions.append(feat)
    sb.features.append(make_destructible_feature('Sentry Wards',
                                                 already_has_destructible=has_any_destructible(sb)))
    modify_loot_properties(sb, 'jadeheart', 'psychic', lambda s: 'psychic')
    return sb
all_tags.append(Tag('sentry wards',
                    'can place d4 runestones it has truesight from',
                    on_apply=apply, overwrites={'wards'}, overwritten_by={'wards'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Deploy Explosive Wards',
                   description_template='(1/short rest) This creature deploys 2d4 tiny runestones with AC 5 and 5 '
                                        'hitpoints '
                                        'each into unoccupied spaces this creature can see within 60 ft. '
                                        'When a small or '
                                        'larger living creature ends its turn within 5 ft. of a runestone or enters a '
                                        'runestone\'s space, the runestone detonates, destroying itself. '
                                        'Each creature within 5 ft. must make a DC {8 + CON + prof} Dexterity '
                                        'saving throw, taking {prof}d6 force damage on a failed save or half '
                                        'as much on a success. Runestones may be disabled with a DC {8 + CON + prof} '
                                        'Dexterity (Sleight of Hand) check or Dexterity (thieves\' tools) check. '  
                                        'The runestones cease to function if this creature uses this ability again.',
                   effect_damage=.1,
                   )
    sb.actions.append(feat)
    sb.features.append(make_destructible_feature('Explosive Wards',
                                                 already_has_destructible=has_any_destructible(sb)))
    modify_loot_properties(sb, 'jadeheart', 'elemental', lambda s: 'elemental')
    return sb
all_tags.append(Tag('explosive wards',
                    'can place 2d4 runestones which explode when a creature comes near',
                    on_apply=apply, overwrites={'wards'}, overwritten_by={'wards'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Reinforced Plating',
                   description_template='All bludgeoning, piercing, and slashing damage dealt by non-magical weapons '
                                        'is reduced by 3.',
                   effect_hp=.25,
                   )
    sb.features.append(feat)
    sb.loot.append(Loot('celadon plating', properties={'dc': lambda s: f'DC {s.base_knowledge_dc} Refine check with '
                                                                       f'mason\'s tools or smith\'s tools to extract'}))
    return sb
all_tags.append(Tag('reinforced plating',
                    'all bludgeoning/piercing/slashing damage reduced by 3',
                    on_apply=apply, overwrites={'plating'}, overwritten_by={'plating'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    sb.add_damage_resistance('radiant')
    sb.add_damage_resistance('radiant')
    sb.add_damage_resistance('fire')
    sb.loot.append(Loot('celadon plating', properties={'dc': lambda s: f'DC {s.base_knowledge_dc} Refine check with '
                                                                       f'mason\'s tools or smith\'s tools to extract'}))
    return sb
all_tags.append(Tag('reflective coating',
                    'add immunity to radiant damage; add resistance to fire damage',
                    on_apply=apply, overwrites={'plating'}, overwritten_by={'plating'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Destruction Override',
                   description_template='As an action, when this creature has fewer than {hit_dice_count + '
                                        'hit_dice_count + hit_dice_count + hit_dice_count} hit points '
                                        'remaining, it '
                                        'can choose to '
                                        'emit a loud warning chirp immediately and explode at the start of its next turn. The '
                                        'explosion extends in a 30-foot radius, and all creatures within the blast '
                                        'must succeed on a  Dexterity saving throw or take '
                                        'fire damage equal to this creature\'s remaining hit points on a failed save, '
                                        'half as much damage on a success. This creature is destroyed. The creature has an '
                                        'override code in the Leitian language, and '
                                        'will explode at the start of its next turn upon hearing it.',
                   effect_damage=.25,
                   )
    sb.features.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'elemental', lambda s: 'elemental')
    sb.features.append(make_destructible_feature('Destruction Override',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('destruction override',
                    'explodes at low hp or with codeword',
                    on_apply=apply, overwrites={'override'}, overwritten_by={'override'}, weight=6))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Stasis Override',
                   description_template='As an action, when this creature has fewer than {CON + CON} hit points '
                                        'remaining, it '
                                        'can choose to '
                                        'emit a loud warning chirp immediately and cocoon itself at the start of its '
                                        'next turn. A crystalline shell encases itself about the creature, making it '
                                        'immune to all forms of harm and rendering it unconscious. The shell can only '
                                        'be destroyed by an *antimagic field* spell or equivalent effect. The creature '
                                        'regains hit points at a rate of one per hour. The cocoon disappears one hour '
                                        'after the creature reaches its hit point maximum. '
                                        'The creature has an '
                                        'override code in the Leitian language, and '
                                        'will trigger the stasis cocoon at the start of its next turn upon hearing it.',
                   effect_hp=.15,
                   )
    sb.features.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'antimagical', lambda s: 'antimagical')
    sb.features.append(make_destructible_feature('Stasis Override',
                                                 already_has_destructible=has_any_destructible(sb)))
    return sb
all_tags.append(Tag('stasis override',
                    'forms crystalline cocoon at low hp or with codeword',
                    on_apply=apply, overwrites={'override'}, overwritten_by={'override'}, weight=6))


all_tags = dict([(tag.name, tag) for tag in all_tags])
