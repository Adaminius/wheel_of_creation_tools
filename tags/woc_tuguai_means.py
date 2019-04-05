from utils import common_features
from utils import Feature
from statblock import Statblock
from statblock import Tag
from statblock import Loot

all_tags = []
table_name = 'WoC: Tuguai Means'
table_description = 'Coming Soon!'


def modify_loot_properties(sb: Statblock, loot_name, key, value):
    for loot in sb.loot:
        if loot.name.lower().strip() == loot_name.lower().strip():
            loot.properties[key] = value


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
                                        'DC {8 + CON + prof} Dexterity saving throw, taking {prof}d{size_die_size} '
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
    return sb
all_tags.append(Tag('fire ray',
                    'add a Fire Ray action; add resistance to fire damage',
                    on_apply=apply, overwrites={'ranged_arm'}, overwritten_by={'ranged_arm'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Ice Ray (Recharge 5-6)',
                   description_template='This creature raises an appendage and unleashes an icy blast in a 60-foot '
                                        'line that is 5 feet wide. Each creature in the line must make a '
                                        'DC {8 + CON + prof} Dexterity saving throw, taking {prof}d{size_die_size} '
                                        'cold damage on a failed save, or half as much damage on a successful one. '
                                        'In addition, terrain under the area of the ray is frozen, becoming difficult '
                                        'terrain. '
                                        'The ice melts after 10 minutes or when the Tuguai is killed.',
                   can_multiattack=False,
                   )
    sb.actions.append(feat)
    sb.add_damage_resistance('cold')
    modify_loot_properties(sb, 'jadeheart', 'elemental', lambda s: 'elemental')
    return sb
all_tags.append(Tag('ice ray',
                    'add a Ice Ray action; add resistance to cold damage',
                    on_apply=apply, overwrites={'ranged_arm'}, overwritten_by={'ranged_arm'}, weight=12))


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
    return sb
all_tags.append(Tag('whirring blades',
                    'add a Whirring Blades melee_attack',
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
    return sb
all_tags.append(Tag('antimagic cone',
                    'add an Antimagic Cone feature',
                    on_apply=apply, overwrites={'eye'}, overwritten_by={'eye'}, weight=12))


def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Psionic Dampening Array',
                   description_template='All non-construct, non-undead creatures within 60 feet of this creature make '
                                        'attack rolls, saving throws, and skill checks based on Intelligence, Wisdom, '
                                        'or Charisma are made at disadvantage. All psychic damage dealt to or by '
                                        'any creatures in the field is halved.',
                   effect_hp=.25,
                   )
    sb.features.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'psionic', lambda s: 'psionic')
    return sb
all_tags.append(Tag('psionic dampening array',
                    'add the Psionic Dampening Array feature',
                    on_apply=apply, overwrites={'field'}, overwritten_by={'field'}, weight=12))


def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Cloaking Field',
                   description_template='This creature and anything it carries becomes invisible until it attacks or '
                                        'uses a spell.',
                   effect_hp=.25,
                   )
    sb.bonus_actions.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'shadowy', lambda s: 'shadowy')
    return sb
all_tags.append(Tag('cloaking field',
                    'add the Cloak bonus action',
                    on_apply=apply, overwrites={'field'}, overwritten_by={'field'}, weight=12))


def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Reinforced Plating',
                   description_template='All bludgeoning, piercing, and slashing damage dealt by non-magical weapons '
                                        'is reduced by 3.',
                   effect_hp=.25,
                   )
    sb.features.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'reinforced', lambda s: 'reinforced')
    return sb
all_tags.append(Tag('reinforced plating',
                    'all bludgeoning/piercing/slashing damage reduced by 3',
                    on_apply=apply, overwrites={'plating'}, overwritten_by={'plating'}, weight=12))


def apply(sb: Statblock) -> Statblock:
    feat = Feature(name='Destruction Override',
                   description_template='As an action, when this creature has fewer than {CON + CON} hit points '
                                        'remaining, it '
                                        'can choose to '
                                        'emit a loud warning chirp and explode at the start of its next turn. The '
                                        'explosion extends in a 30-foot radius, and all creatures within the blast '
                                        'must succeed on a DC {CON + prof + 8} Dexterity saving throw or take '
                                        'fire damage equal to this creature\'s remaining hit points on a failed save, '
                                        'half as much damage on a success. This creature and its jadeheart are '
                                        'destroyed. The creature has an override code in the Leitian language, and '
                                        'will explode at the start of its next turn upon hearing it.',
                   effect_damage=.25,
                   effect_hp=.25,
                   )
    sb.features.append(feat)
    modify_loot_properties(sb, 'jadeheart', 'elemental', lambda s: 'elemental')
    return sb
all_tags.append(Tag('destruction override',
                    'explodes at low hp or with codeword',
                    on_apply=apply, overwrites={'override'}, overwritten_by={'override'}, weight=6))


all_tags = dict([(tag.name, tag) for tag in all_tags])
