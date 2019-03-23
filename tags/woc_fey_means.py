from utils import common_features
from utils import Feature
from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'WoC: Fey Means'
table_description = 'Fey in the Wheel of Creation come from the Ring of Seasons, a world just outside the one humans ' \
                    'reside in. It is ruled by four courts, one for each season, and inhabitants either receive a ' \
                    'strong benefit for their allegiance with a particular court, or suffer weakness as the price for ' \
                    'freedom. The fey themselves are inspired by various mythological creatures, such as fairies, ' \
                    'jinn, or yaksha. None are so individually powerful as to be considered god-like, and they are ' \
                    'neither so virtuous as the Emperors of Heaven nor so vile as the Void or the demons in haunting the ' \
                    'the space between the rings. Their world is in many ways similar that to the Ring of Earth, ' \
                    'though twisted and exaggerated.'


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

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 2
    beckon = Feature(name='Beckon', description_template=
                     'This creature targets one humanoid, beast, or giant it can see within 30 ft. of it and performs '
                     'a beckoning gesture. If the target can see this creature, the target must make succeed on a DC '
                     '{CHA + prof + 8} Wisdom saving throw or be charmed for 1 minute.\nWhile charmed, the target '
                     'is incapacitated. If the charmed target is more than 5 ft. away from this creature, the target '
                     'must move on its turn toward this creature by the most direct route. It doesn\'t avoid '
                     'opportunity attacks, but before moving into damaging terrain, such as lava or a pit, and whenever '
                     'it takes damage, the target can repeat the saving throw. The target can also repeat the saving '
                     't hrow at the end of each of its turns. If a creature\'s saving throw is successful, the effect '
                     'ends on it.\nA target that successfully saves is immune to Beckon for the next 24 hours.',
                     can_multiattack=True)
    sb.actions.append(beckon)
    return sb
all_tags.append(Tag('alluring', '+1 to Charisma; add the Beckon action', on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 2
    return sb
all_tags.append(Tag('hideous', '+2 to Charisma', on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['DEX'].value += 3
    sb.ability_scores['CON'].value -= 1
    return sb
all_tags.append(Tag('delicate', '+3 to Dexterity; -1 to Constitution', on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['DEX'].value += 3
    sb.ability_scores['STR'].value -= 1
    return sb
all_tags.append(Tag('spindly', '+3 to Dexterity; -1 to Strength', on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['DEX'].value += 2
    return sb
all_tags.append(Tag('graceful', '+2 to Dexterity', on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.features.append(common_features['Reckless'])
    sb.damage_resistances.discard('bludgeoning, piercing, and slashing damage from weapons not made of thokcha')
    sb.damage_immunities.add('bludgeoning, piercing, and slashing damage from weapons not made of thokcha')
    return sb
all_tags.append(Tag('otherwordly fury', 'add the Reckless feature; immunity to bludgeoning, piercing, and slashing '
                                        'weapons not made from thokcha', on_apply=apply, weight=3))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['STR'].value += 2
    sb.speed = max(5, sb.speed - 5)
    sb.fly_speed = max(0, sb.fly_speed - 5)
    sb.swim_speed = max(0, sb.swim_speed - 5)
    sb.climb_speed = max(0, sb.climb_speed - 5)
    return sb
all_tags.append(Tag('lumbering', '+2 to Strength; subtract 10 ft. from all speeds', on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.features.append(common_features['Amphibious'])
    if sb.swim_speed > 0:
        sb.swim_speed += 10
    sb.add_damage_resistance('poison')
    return sb
all_tags.append(Tag('swamp-dweller', 'can breathe both air and water; if it has a swim speed, add 10 ft. to it; '
                                     'resistance to poison damage; immunity to the poisoned condition',
                    on_apply=apply, overwrites={'dweller'}, overwritten_by={'dweller'}, weight=2))

def apply(sb: Statblock) -> Statblock:
    sb.features.append(common_features['Amphibious'])
    sb.swim_speed = max(20, sb.speed)
    return sb
all_tags.append(Tag('sea-dweller', 'can breathe both air and water; gain a swim speed of 20 ft. or equal to its '
                                   'walking speed, whichever is greater; +30 ft. darkvision',
                    on_apply=apply, overwrites={'dweller'}, overwritten_by={'dweller'}, weight=2))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['DEX'].value += 1
    base_stealth = sb.ability_scores['DEX'] + sb.proficiency
    if sb.skills.get('Stealth', 0) >= base_stealth:
        sb.skills['Stealth'] = base_stealth + sb.proficiency
    else:
        sb.skills['Stealth'] = base_stealth
    return sb
all_tags.append(Tag('forest-dweller', '+1 to Dexterity; proficiency in the Stealth skill or expertise if it already '
                                      'has proficiency',
                    on_apply=apply, overwrites={'dweller'}, overwritten_by={'dweller'}, weight=2))

def apply(sb: Statblock) -> Statblock:
    sb.climb_speed = max(20, sb.speed)
    sb.features.append(common_features['Ambusher'])
    return sb
all_tags.append(Tag('jungle-dweller', 'add the Ambusher feature; gain a climb speed of 20 ft. or equal to its '
                                      'walking speed, whichever is greater',
                    on_apply=apply, overwrites={'dweller', 'Brumal'},
                    overwritten_by={'dweller', 'jungle-dweller'}, weight=2))

def apply(sb: Statblock) -> Statblock:
    sb.climb_speed = max(20, sb.speed)
    sb.features.append(common_features['Nimble Escape'])
    sb.features.append(common_features['Sunlight Sensitivity'])
    return sb
all_tags.append(Tag('cave-dweller', 'add the Nimble Escape feature; add the Sunlight Sensitivity feature; '
                                    '+60 ft. darkvision',
                    on_apply=apply, overwrites={'dweller'}, overwritten_by={'dweller'}, weight=2))

def apply(sb: Statblock) -> Statblock:
    sb.fly_speed = max(20, sb.speed)
    sb.ability_scores['CON'].value -= 1
    sb.ability_scores['DEX'].value += 1
    sb.ability_scores['CHA'].value += 1
    return sb
all_tags.append(Tag('gossamer wings',
                    'add a fly speed equal to walking speed; -1 to Constitution; +1 to Dexterity; +1 to Charisma',
                    on_apply=apply, overwrites={'wings'}, overwritten_by={'wings'}, weight=3))

def apply(sb: Statblock) -> Statblock:
    sb.fly_speed = max(20, sb.speed)
    sb.ability_scores['STR'].value -= 1
    sb.ability_scores['CHA'].value += 1
    sb.ability_scores['WIS'].value += 1
    return sb
all_tags.append(Tag('crow wings',
                    'add a fly speed equal to walking speed; -1 to Strength; +1 to Charisma; +1 to Wisdom',
                    on_apply=apply, overwrites={'wings'}, overwritten_by={'wings'}, weight=3))

def apply(sb: Statblock) -> Statblock:
    sb.speed = min(10, sb.speed - 5)
    sb.fly_speed = max(20, 2 * sb.speed)
    sb.ability_scores['CHA'].value += 2
    return sb
all_tags.append(Tag('bat wings',
                    'subtract 5 ft. from walking speed; add a fly speed equal to twice walking speed; +2 to Charisma',
                    on_apply=apply, overwrites={'wings'}, overwritten_by={'wings'}, weight=3))

def apply(sb: Statblock) -> Statblock:
    sb.features.append(common_features['Pack Tactics'])
    return sb
all_tags.append(Tag('eusocial pheromones',
                    'add the Pack Tactics feature',
                    on_apply=apply, weight=2))

def apply(sb: Statblock) -> Statblock:
    sb.features.append(common_features['Petrifying Gaze'])
    sb.darkvision += 30
    return sb
all_tags.append(Tag('crystalline eyes',
                    'add the Petrifying Gaze feature; add 30 ft. Darkvision',
                    on_apply=apply, overwrites={'eyes'}, overwritten_by={'eyes'}, weight=3))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 2
    sb.ability_scores['WIS'].value -= 2
    sb.skills['Insight'] = sb.proficiency + sb.ability_scores['WIS']
    return sb
all_tags.append(Tag('goat-like eyes',
                    '-2 to Charisma; +2 to Wisdom; add the Insight skill',
                    on_apply=apply, overwrites={'eyes'}, overwritten_by={'eyes'}, weight=5))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 2
    sb.darkvision += 30
    sb.features.append(common_features['Sunlight Sensitivity'])
    sb.skills['Perception'] = sb.proficiency + sb.ability_scores['WIS']
    return sb
all_tags.append(Tag('feline eyes',
                    '+2 to Charisma; add 30 ft. to Darkvision; add the Perception skill; '
                    'add the Sunlight Sensitivity feature',
                    on_apply=apply, overwrites={'eyes'}, overwritten_by={'eyes'}, weight=8))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 2
    sb.ability_scores['INT'].value += 2
    sb.ability_scores['WIS'].value += 2
    sb.skills['Deception'] = sb.proficiency + sb.ability_scores['CHA']
    return sb
all_tags.append(Tag('human-like eyes',
                    '+2 to Charisma; +2 to Intelligence; +2 to Wisdom; add the Deception skill',
                    on_apply=apply, overwrites={'eyes'}, overwritten_by={'eyes'}, weight=3))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['STR'].value += 3
    sb.size += 1
    return sb
all_tags.append(Tag('hulking',
                    'increase size by one step; +3 to Constitution',
                    on_apply=apply, overwrites={'small'}, overwritten_by={'big'}, weight=5))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['STR'].value += 3
    sb.size += 1
    return sb
all_tags.append(Tag('towering',
                    'increase size by one step; +3 to Strength',
                    on_apply=apply, overwrites={'small'}, overwritten_by={'big'}, weight=5))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['STR'].value += 3
    sb.size -= 1
    return sb
all_tags.append(Tag('petite',
                    'decrease size by one step; +3 to Dexterity',
                    on_apply=apply, overwrites={'big'}, overwritten_by={'small'}, weight=5))

def apply(sb: Statblock) -> Statblock:
    if sb.armor_class_type.lower().strip() == 'natural armor':
        sb.base_natural_armor += 2
    else:
        sb.ability_scores['DEX'].value += 3
    sb.size -= 1
    return sb
all_tags.append(Tag('diminutive',
                    'decrease size by one step; +2 to AC if has natural armor, +3 to Dexterity otherwise',
                    on_apply=apply, overwrites={'big'}, overwritten_by={'small'}, weight=5))

def apply(sb: Statblock) -> Statblock:
    claws = Feature(name='Claws',
                    description_template='*Melee Weapon Attack:* +{prof + STR} to hit, reach 5 ft., one target. '
                                         '*Hit:* 7 (2d{size_die_size - 2} + {STR}) slashing damage.',
                    can_multiattack=True,

                    )
    sb.actions.append(claws)
    return sb
all_tags.append(Tag('lacerating claws',
                    'add a Claw melee attack',
                    on_apply=apply, overwrites={'claws'}, overwritten_by={'claws'}, weight=8))

def apply(sb: Statblock) -> Statblock:
    claws = Feature(name='Poison Claws',
                    description_template='*Melee Weapon Attack:* +{prof + DEX} to hit, reach 5 ft., one target. '
                                         '*Hit:* 7 (1d{size_die_size} + {CHA}) poison damage.',
                    can_multiattack=True
                    )
    sb.actions.append(claws)
    return sb
all_tags.append(Tag('poison claws',
                    'add a Poison Claws melee attack',
                    on_apply=apply, overwrites={'claws'}, overwritten_by={'claws'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    attack = Feature(name='Paralyzing Bite',
                     description_template='*Melee Weapon Attack:* +{prof + DEX} to hit, reach 5 ft., one target. '
                                          '*Hit:* 7 ({prof - 1}d6 + {DEX}) piercing damage. The '
                                          'target must succeed a DC {8 + prof + CHA} Constitution saving throw or '
                                          'become poisoned for one minute. If its saving throw result is 5 or lower, '
                                          'the poisoned target falls unconscious for the same duration, or until it '
                                          'takes damage or another creatures uses its acton to shake it awake.',
                     can_multiattack=False
                     )
    sb.actions.append(attack)
    return sb
all_tags.append(Tag('paralyzing fangs',
                    'add a Paralyzing Bite melee attack',
                    on_apply=apply, overwrites={'fangs'}, overwritten_by={'fangs'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    attack = Feature(name='Venomous Bite',
                     description_template='*Melee Weapon Attack:* +{prof + DEX} to hit, reach 5 ft., one target. '
                                          '*Hit:* 7 ({size_mod}d4 + {CHA}) poison damage and 7 ({size_mod}d4 + '
                                          '{DEX}) piercing damage.',
                     can_multiattack=True
                     )
    sb.actions.append(attack)
    return sb
all_tags.append(Tag('venomous fangs',
                    'add a Venomous Bite melee attack',
                    on_apply=apply, overwrites={'fangs'}, overwritten_by={'fangs'}, weight=12))

def apply(sb: Statblock) -> Statblock:
    attack = Feature(name='Spit Acid',
                     description_template='*Ranged Weapon Attack:* +{prof + DEX} to hit, range 30/120 ft., one target. '
                                          '*Hit:* 7 ({prof - 1}d8 + {DEX}) acid damage.',
                     can_multiattack=False
                     )
    sb.actions.append(attack)
    return sb
all_tags.append(Tag('acidic spittle',
                    'add a Spit Acid ranged attack',
                    on_apply=apply, overwrites={'spit'}, overwritten_by={'spit'}, weight=5))

def apply(sb: Statblock) -> Statblock:
    attack = Feature(name='Spit Frost',
                     description_template='*Ranged Weapon Attack:* +{prof + DEX} to hit, range 30/120 ft., one target. '
                                          '*Hit:* 7 ({prof - 1}d6 + {DEX}) cold damage. On a hit, the target\'s speed'
                                          'is halved until the start of this creature\'s next turn.',
                     can_multiattack=False
                     )
    sb.actions.append(attack)
    return sb
all_tags.append(Tag('freezing spittle',
                    'add a Spit Frost ranged attack',
                    on_apply=apply, overwrites={'spit'}, overwritten_by={'spit'}, weight=15, requires={'Brumal'}))

def apply(sb: Statblock) -> Statblock:
    attack = Feature(name='Spit Fire',
                     description_template='*Ranged Weapon Attack:* +{prof + DEX} to hit, range 30/120 ft., one target. '
                                          '*Hit:* 7 ({prof - 1}d10 + {DEX}) fire damage. The GM should refer the '
                                          'target to the following webpage: '
                                          'https://en.wikipedia.org/wiki/List_of_burn_centers_in_the_Wheel_of_Creation',
                     can_multiattack=False
                     )
    sb.actions.append(attack)
    return sb
all_tags.append(Tag('scorching spittle',
                    'add a Spit Fire ranged attack',
                    on_apply=apply, overwrites={'spit'}, overwritten_by={'spit'}, weight=15, requires={'Aestival'}))

def apply(sb: Statblock) -> Statblock:
    attack = Feature(name='Putrid Spit',
                     description_template='*Ranged Weapon Attack:* +{prof + DEX} to hit, range 30/120 ft., one target. '
                                          '*Hit:* 7 ({prof - 1}d6 + {DEX}) necrotic damage, and the target can\'t '
                                          'regain hit points until the start of your next turn.',
                     can_multiattack=False
                     )
    sb.actions.append(attack)
    sb.add_damage_resistance('necrotic')
    sb.add_damage_resistance('necrotic')
    return sb
all_tags.append(Tag('putrid spittle',
                    'add a Putrid Spit ranged attack; add immunity to necrotic damage',
                    on_apply=apply, overwrites={'spit'}, overwritten_by={'spit'}, weight=15, requires={'Autumnal'}))

def apply(sb: Statblock) -> Statblock:
    attack = Feature(name='Toxic Spit',
                     description_template='*Ranged Weapon Attack:* +{prof + DEX} to hit, range 30/120 ft., one target. '
                                          '*Hit:* 7 ({prof - 1}d6 + {DEX}) poison damage, and the target must make a '
                                          'DC {8 + CHA + prof} Constitution saving throw or become poisoned for 1 '
                                          'minute. It can repeat this saving throw at the end of each its turns.',
                     can_multiattack=False
                     )
    sb.actions.append(attack)
    sb.add_damage_resistance('poison')
    sb.add_damage_resistance('poison')
    sb.condition_immunities.add('poisoned')
    return sb
all_tags.append(Tag('toxic spittle',
                    'add a Toxic Spit ranged attack; add immunity to poison damage and the poisoned condition',
                    on_apply=apply, overwrites={'spit'}, overwritten_by={'spit'}, weight=15, requires={'Vernal'}))

def apply(sb: Statblock) -> Statblock:
    feature = Feature(name='Prehensile Tail',
                      description_template='This creature can use its tail like an additional hand, allowing it to '
                                           'pick up and manipulate objects in simple ways.')
    sb.climb_speed = max(20, sb.speed, sb.climb_speed)
    sb.features.append(feature)
    sb.ability_scores['DEX'].value += 1
    return sb
all_tags.append(Tag('prehensile tail',
                    'add the Prehensile Tail feature; add a climb speed equal to walking speed; +1 to Dexterity',
                    on_apply=apply, overwrites={'tail'}, overwritten_by={'tail'}, weight=4))

def apply(sb: Statblock) -> Statblock:
    feature = Feature(name='Sweeping Tail',
                      description_template='*Melee Weapon Attack:* +{prof + STR} to hit, reach 10 ft., all '
                                           'targets within reach. '
                                           '*Hit:* 7 (1d{size_die_size} + {STR}) bludgeoning '
                                           'damage. On a hit, the target must also make a DC {8 + prof + STR} saving '
                                           'throw or be knocked prone.',
                      can_multiattack=False,
                      effect_damage=.25)
    sb.actions.append(feature)
    return sb
all_tags.append(Tag('sweeping tail',
                    'add a Tail Sweep melee attack which hits all nearby targets',
                    on_apply=apply, overwrites={'tail'}, overwritten_by={'tail'}, weight=10))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 1
    if sb.armor_class_type.lower().strip() == 'natural armor':
        sb.base_natural_armor += 2
    else:
        sb.ability_scores['DEX'].value += 3
    return sb
all_tags.append(Tag('twitching tail',
                    '+1 to Charisma; +2 to AC if has natural armor, +3 to Dexterity otherwise',
                    on_apply=apply, overwrites={'tail'}, overwritten_by={'tail'}, weight=10))


def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 1
    feature = Feature(name='Foul Omens',
                      description_template='This creature can\'t be surprised, and it always knows if there are '
                                           'any creatures with hostile intentions towards it within 1 mile, but it'
                                           'can\'t determine their exact number or location.')
    sb.features.append(feature)

    return sb
all_tags.append(Tag('tails without number',
                    '+1 to Charisma; add the Foul Omens feature',
                    on_apply=apply, overwrites={'tail'}, overwritten_by={'tail'}, weight=3))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['STR'].value += 1
    feature = Feature(name='Gore', description_template=
                      '*Melee Weapon Attack:* +{prof + STR} to hit, reach 5 ft., one target. '
                      '*Hit:* 7 ({size_mod}d8 + {STR}) piercing damage.',
                      can_multiattack=True)
    sb.actions.append(feature)
    sb.features.append(common_features['Charge'])
    return sb
all_tags.append(Tag('goring horns',
                    'add the Charge feature; add the Gore attack; +1 to Strength',
                    on_apply=apply, overwrites={'horn'}, overwritten_by={'horn'}, weight=10))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CON'].value += 1
    sb.speed += 10
    sb.features.append(common_features['Charge'])
    return sb
all_tags.append(Tag('twisting antlers',
                    'add 10 ft. to walking speed; add the Charge feature; +1 to Constitution',
                    on_apply=apply, overwrites={'horn'}, overwritten_by={'horn'}, weight=10))

def apply(sb: Statblock) -> Statblock:
    if sb.armor_class_type.lower().strip() == 'natural armor':
        sb.base_natural_armor += 2
    else:
        sb.ability_scores['STR'].value += 3
    sb.features.append(common_features['Charge'])
    return sb
all_tags.append(Tag('ramming horns',
                    'add the Charge feature; +2 to AC if has natural armor, +3 to Strength otherwise',
                    on_apply=apply, overwrites={'horn'}, overwritten_by={'horn'}, weight=10))

def apply(sb: Statblock) -> Statblock:
    if sb.ability_scores['INT'].value > 7:
        feature = Feature('Illusory Appearance',
                          'The creature uses its magic to take on the appearance of a humanoid, animal, or '
                          'plant of similar '
                          'size. This effect can be ended as a bonus action or ends automatically if the creature '
                          'dies. '
                          'The false appearance fails to hold up to physical inspection--if the creature actually has '
                          'scales but appears to have soft fur, someone touching it could feel the roughness of the '
                          'scales. Otherwise, a creature must take an action to visually inspect the illusion and '
                          'succeed on a DC {8 + prof + CHA} Intelligence (Investigation) check to discern that '
                          'the creature is disguised.')
    else:
        feature = Feature('Illusory Appearance',
                          'The creature uses its magic to take on the appearance of an animal or plant of '
                          'similar '
                          'size. This effect can be ended as a bonus action or ends automatically if the creature '
                          'dies. '
                          'The false appearance fails to hold up to physical inspection--if the creature actually has '
                          'scales but appears to have soft fur, someone touching it could feel the roughness of the '
                          'scales. Otherwise, a creature must take an action to visually inspect the illusion and '
                          'succeed on a DC {8 + prof + CHA} Intelligence (Investigation) check to discern that '
                          'the creature is disguised.')
    sb.actions.append(feature)
    return sb
all_tags.append(Tag('deceptive glamour',
                    'add the Illusory Appearance action--if Intelligence > 7 can be humanoid, otherwise as '
                    'animals/plants',
                    on_apply=apply, weight=13))

def apply(sb: Statblock) -> Statblock:
    attack = Feature(name='Icy Breath (Recharge 5-6)',
                     # todo: if we implement a better op parser, could scale the cone from 15 to 60 ft.
                     description_template='The creature exhales a freezing gust of wind in a 30 ft. cone. Each '
                                          'creature in that area must make a DC {8 + prof + CHA} Constitution '
                                          'saving throw. On a failed saving throw, the creature is pushed back 15 ft. '
                                          'and takes 5 ({prof + prof - 1}d6) cold damage. On a success, it isn\'t pushed '
                                          'and takes half as much damage.',
                     can_multiattack=False
                     )
    sb.actions.append(attack)
    return sb
all_tags.append(Tag('icy breath',
                    'add an Icy Breath action',
                    on_apply=apply, overwrites={'breath'}, overwritten_by={'breath'}, weight=10, requires={'Brumal'}))

def apply(sb: Statblock) -> Statblock:
    sb.add_damage_resistance('cold')
    sb.add_damage_resistance('cold')
    sb.add_damage_vulnerability('fire')
    if sb.armor_class_type.lower().strip() == 'natural armor':
        sb.base_natural_armor += 2
    else:
        sb.ability_scores['CON'].value += 3
    return sb
all_tags.append(Tag('frozen hide',
                    'add cold immunity; add fire vulnerability; +2 to AC if has natural armor, '
                    '+3 to Constitution otherwise',
                    on_apply=apply, overwrites={'hide'}, overwritten_by={'hide'}, weight=10, requires={'Brumal'}))

def apply(sb: Statblock) -> Statblock:
    sb.add_damage_resistance('fire')
    sb.add_damage_resistance('fire')
    sb.add_damage_vulnerability('cold')
    sb.features.append(Feature('Scorching Hide', 'When a creature makes a melee weapon attack against this creature,'
                                                 'they take {hit_dice_count} fire damage.'))
    return sb
all_tags.append(Tag('scorching hide',
                    'add fire immunity; add cold vulnerability; deals fire damage to attackers',
                    on_apply=apply, overwrites={'hide'}, overwritten_by={'hide'}, weight=10, requires={'Aestival'}))

# if we're using so much charisma, need more charisma abilities like magic attacks
# spritely
# gouging tusks
# scything tusks
# reptilian eyes
# reckless
# charge
# fangs (removed bite from predator SB so need something to fill in)
# claws
# hide/armor/skin/fur
# parry
# detect magic
# invisibility (see Sprite)
# heart sight (see Sprite)
# hooves/feet
# snout/face
# tunneling claws
# tree stride
# mimic voices
# voice weapon
# Change Shape (better Illusory appearance, see dragons)
# winter
#   icy breath
#   paralyzing breath
#   snow camouflage
#   ice walk
# summer
#   fiery breath
#   blinding radiance
#   moisture drain
#   rocky hide
#   charred hide
# autumn
#   corrosive breath
#   withering spores
#   moldy hide
# spring
#   poisonous breath
#   tantalizing spores
#   paralyzing spores
#   bark-like hide

############################
#    ~~~ Alignments ~~~    #
############################
def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Winter'
    sb.add_damage_resistance('cold')
    sb.add_damage_resistance('psychic')
    if sb.primary_type == 'fey':
        sb.add_damage_resistance('psychic')
    sb.features.append(common_features['Bound to the Courts'])
    sb.features.append(common_features['Courtship'])
    return sb
all_tags.append(Tag('Brumal', 'Winter alignment; cold and psychic resistance; advantage on saving throws against being '
                              'charmed or put to sleep',
                    on_apply=apply,
                    overwrites={'alignment', 'jungle-dweller'}, overwritten_by={'alignment', 'Brumal'},
                    weight=18
                    ))

def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Spring'
    sb.add_damage_resistance('poison')
    sb.add_damage_resistance('psychic')
    if sb.primary_type == 'fey':
        sb.add_damage_resistance('psychic')
    sb.features.append(common_features['Bound to the Courts'])
    sb.features.append(common_features['Courtship'])
    return sb
all_tags.append(Tag('Vernal', 'Spring alignment; poison and psychic resistance; advantage on saving throws against being '
                               'charmed or put to sleep',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'},
                    weight=18
                    ))

def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Summer'
    sb.damage_resistances.add('fire')
    sb.add_damage_resistance('psychic')
    if sb.primary_type == 'fey':
        sb.add_damage_resistance('psychic')
    sb.features.append(common_features['Bound to the Courts'])
    sb.features.append(common_features['Courtship'])
    return sb
all_tags.append(Tag('Aestival', 'Summer alignment; fire and psychic resistance; advantage on saving throws against being '
                               'charmed or put to sleep',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'},
                    weight=18
                    ))

def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Autumn'
    sb.add_damage_resistance('necrotic')
    sb.add_damage_resistance('psychic')
    if sb.primary_type == 'fey':
        sb.add_damage_resistance('psychic')
    sb.features.append(common_features['Bound to the Courts'])
    sb.features.append(common_features['Courtship'])
    return sb
all_tags.append(Tag('Autumnal', 'Autumn alignment; necrotic and psychic resistance; advantage on saving throws against being '
                               'charmed or put to sleep',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'},
                    weight=18
                    ))


all_tags = dict([(tag.name, tag) for tag in all_tags])
