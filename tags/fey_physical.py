from utils import common_actions
from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'Fey Physical'

def apply(sb: Statblock) -> Statblock:
    sb.primary_type = 'fey'
    sb.damage_immunities.add('immunity to bludgeoning, piercing, and slashing damage from weapons not made of thokcha')
    sb.damage_vulnerabilities.add('psychic')
    sb.languages.append('Sylvan')
    return sb
all_tags.append(Tag('fey', 'Fey type; immunity to bludgeoning, piercing, and slashing damage from weapons not made of thokcha; vulnerability to psychic damage; speaks Sylvan', weight=0, on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 2
    return sb
all_tags.append(Tag('beautiful', 'add +2 to Charisma', on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['CHA'].value += 2
    return sb
all_tags.append(Tag('hideous', 'add +2 to Charisma', on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.ability_scores['STR'].value += 2
    sb.speed = max(0, sb.speed - 5)
    sb.fly_speed = max(0, sb.fly_speed - 5)
    sb.swim_speed = max(0, sb.swim_speed - 5)
    sb.climb_speed = max(0, sb.climb_speed - 5)
    return sb
all_tags.append(Tag('lumbering', 'add +2 to Strength; subtract 5 ft. from all speeds', on_apply=apply))

def apply(sb: Statblock) -> Statblock:
    sb.abilities.append(common_actions['Amphibious'])
    return sb
all_tags.append(Tag('swamp-dweller', 'can breathe both air and water'))

############################
#    ~~~ Alignments ~~~    #
############################
def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Winter'
    sb.damage_resistances.add('cold')
    sb.damage_resistances.add('psychic')
    sb.damage_vulnerabilities.discard('psychic')
    return sb
all_tags.append(Tag('Wintry', 'Winter alignment; cold and psychic resistance',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'}
                    ))

def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Spring'
    sb.damage_resistances.add('poison')
    sb.damage_resistances.add('psychic')
    sb.damage_vulnerabilities.discard('psychic')
    return sb
all_tags.append(Tag('Springy', 'Spring alignment; poison and psychic resistance',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'}
                    ))

def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Summer'
    sb.damage_resistances.add('fire')
    sb.damage_resistances.add('psychic')
    sb.damage_vulnerabilities.discard('psychic')
    return sb
all_tags.append(Tag('Summery', 'Summer alignment; fire and psychic resistance',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'}
                    ))

def apply(sb: Statblock) -> Statblock:
    sb.alignment = 'Autumn'
    sb.damage_resistances.add('necrotic')
    sb.damage_resistances.add('psychic')
    sb.damage_vulnerabilities.discard('psychic')
    return sb
all_tags.append(Tag('Autumnal', 'Autumn alignment; necrotic and psychic resistance',
                    on_apply=apply,
                    overwrites={'alignment'}, overwritten_by={'alignment'}
                    ))

all_tags = dict([(tag.name, tag) for tag in all_tags])
