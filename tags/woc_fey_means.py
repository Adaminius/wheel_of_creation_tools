from utils import common_actions
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
                    'neither so virtuous as the Emperors of Heaven nor so vile as the demons inhabiting the Void and ' \
                    'the Grease Between the Rings. Their world is in many ways similar that to the Ring of Earth, ' \
                    'though twisted and exaggerated.'


def apply(sb: Statblock) -> Statblock:
    sb.primary_type = 'fey'
    sb.add_damage_resistance('bludgeoning, piercing, and slashing damage from weapons not made of thokcha')
    sb.add_damage_vulnerability('psychic')
    sb.languages.append('Sylvan')
    return sb
all_tags.append(Tag('fey', 'Fey type; resistance to bludgeoning, piercing, and slashing damage from weapons not made '
                           'of thokcha; vulnerability to psychic damage; speaks Sylvan',
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
                    'throw at the end of each of its turns. If a creature\'s saving throw is successful, the effect '
                    'ends on it.\nA target that successfully saves is immune to Beckon for the next 24 hours.')
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
    sb.ability_scores['STR'].value += 2
    sb.damage_resistances.discard('bludgeoning, piercing, and slashing damage from weapons not made of thokcha')
    sb.damage_immunities.add('bludgeoning, piercing, and slashing damage from weapons not made of thokcha')
    return sb
all_tags.append(Tag('otherwordly fury', '+2 to Strength; immunity to bludgeoning, piercing, and slashing weapons not '
                                        'made from thokcha', on_apply=apply, weight=3))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['STR'].value += 2
    sb.speed = max(5, sb.speed - 5)
    sb.fly_speed = max(0, sb.fly_speed - 5)
    sb.swim_speed = max(0, sb.swim_speed - 5)
    sb.climb_speed = max(0, sb.climb_speed - 5)
    return sb
all_tags.append(Tag('lumbering', '+2 to Strength; subtract 10 ft. from all speeds', on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.features.append(common_actions['Amphibious'])
    if sb.swim_speed > 0:
        sb.swim_speed += 10
    sb.add_damage_resistance('poison')
    return sb
all_tags.append(Tag('swamp-dweller', 'can breathe both air and water; if it has a swim speed, add 10 ft. to it; '
                                     'resistance to poison damage; immunity to the poisoned condition',
                    on_apply=apply, overwrites={'dweller'}, overwritten_by={'dweller'}, weight=2))

def apply(sb: Statblock) -> Statblock:
    sb.features.append(common_actions['Amphibious'])
    sb.swim_speed = max(20, sb.speed)
    return sb
all_tags.append(Tag('sea-dweller', 'can breathe both air and water; gain a swim speed of 20 ft. or equal to its '
                                   'walking speed, whichever is greater; +30 ft. darkvision',
                    on_apply=apply, overwrites={'dweller'}, overwritten_by={'dweller'}, weight=2))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['DEX'].value += 1
    sb.skills['Stealth'] = min(2 * sb.proficiency + sb.ability_scores['DEX'].modifier,
                               sb.skills.get('Stealth', 0) + sb.proficiency + sb.ability_scores['DEX'])
    return sb
all_tags.append(Tag('forest-dweller', '+1 to Dexterity; proficiency in the Stealth skill or expertise if it already '
                                      'has proficiency',
                    on_apply=apply, overwrites={'dweller'}, overwritten_by={'dweller'}, weight=2))

def apply(sb: Statblock) -> Statblock:
    sb.climb_speed = max(20, sb.speed)
    sb.features.append(common_actions['Ambusher'])
    return sb
all_tags.append(Tag('jungle-dweller', 'add the Ambusher feature; gain a climb speed of 20 ft. or equal to its '
                                      'walking speed, whichever is greater',
                    on_apply=apply, overwrites={'dweller'}, overwritten_by={'dweller'}, weight=2))

def apply(sb: Statblock) -> Statblock:
    sb.climb_speed = max(20, sb.speed)
    sb.features.append(common_actions['Nimble Escape'])
    sb.features.append(common_actions['Sunlight Sensitivity'])
    return sb
all_tags.append(Tag('cave-dweller', 'add the Nimble Escape feature; add the Sunlight Sensitivity feature; '
                                    '+60 ft. darkvision',
                    on_apply=apply, overwrites={'dweller'}, overwritten_by={'dweller'}, weight=2))

# goat-like eyes
# feline eyes
# human-like face
# gossamer wings
# feathery wings
# bat wings
# lacerating claws

############################
#    ~~~ Alignments ~~~    #
############################
def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Winter'
    sb.add_damage_resistance('cold')
    sb.add_damage_resistance('psychic')
    if sb.primary_type == 'fey':
        sb.add_damage_resistance('psychic')
    sb.features.append(common_actions['Bound to the Courts'])
    return sb
all_tags.append(Tag('Wintry', 'Winter alignment; cold and psychic resistance; advantage on saving throws against being '
                              'charmed or put to sleep',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'}
                    ))

def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Spring'
    sb.add_damage_resistance('poison')
    sb.add_damage_resistance('psychic')
    if sb.primary_type == 'fey':
        sb.add_damage_resistance('psychic')
    sb.features.append(common_actions['Bound to the Courts'])
    return sb
all_tags.append(Tag('Vernal', 'Spring alignment; poison and psychic resistance; advantage on saving throws against being '
                               'charmed or put to sleep',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'}
                    ))

def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Summer'
    sb.damage_resistances.add('fire')
    sb.add_damage_resistance('psychic')
    if sb.primary_type == 'fey':
        sb.add_damage_resistance('psychic')
    sb.features.append(common_actions['Bound to the Courts'])
    return sb
all_tags.append(Tag('Summery', 'Summer alignment; fire and psychic resistance; advantage on saving throws against being '
                               'charmed or put to sleep',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'}
                    ))

def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Autumn'
    sb.add_damage_resistance('necrotic')
    sb.add_damage_resistance('psychic')
    if sb.primary_type == 'fey':
        sb.add_damage_resistance('psychic')
    sb.features.append(common_actions['Bound to the Courts'])
    return sb
all_tags.append(Tag('Autumnal', 'Autumn alignment; necrotic and psychic resistance; advantage on saving throws against being '
                               'charmed or put to sleep',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'}
                    ))

all_tags = dict([(tag.name, tag) for tag in all_tags])
