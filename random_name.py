import random
from statblock import Statblock


generic_titles = [
    ' the Invincible',
    ' the Invisible',
    ' the Unseen',
    ' the Whacked',
    ' the Wacky',
    ' the Forlorn',
    ' the Undefeated',
    ', Victor from the Blue Team',
    ' the Wanderer',
    ' the Shiny',
    ' the Crass',
    ' the Gatherer',
    ' the Ironclad',
    ' the Well-Read',
    ' the Dishonored',
    ' the Fabled',
    ' the Strange',
    ' the Dogmatic',
    ' the Undertold',
    ', Bearer of Banners',
    ' the Undying',
    ' the Inexplicable',
    ' the Just Plain Mad',
    ' the Inescapable',
    ' the Burdened',
    ' the Inexorable',
    ' the Bloodthirsty',
    ' the Lonely',
]


def get_other_name(sb: Statblock):
    first = [
        'Lumpkin',
        'Koebel',
        'Harper',
        'Colville',
        'Crane',
        'Crawford',
        'Crawford',
        'Baker',
        'Mearls',
        'Kimbee',
        'Sonka',
        'Rhaegos',
        'Naecar',
        'Xirath',
        'Baelas',
        'Rulfgar',
        'Mitch',
    ]
    if 'warrior' in sb.name.lower():
        return [random.choice(first) + random.choice(generic_titles)]
    return [f'{random.choice(first)}\'s Monster']


def get_fey_name(sb: Statblock):
    if 'fey' not in sb.primary_type.lower():
        return []
    prav = [
        'Rusalka',
        'Vodianoi',
        'Leshy',
        'Likho',
        'Kikimora',
        'Mavka',
    ]
    names = [random.choice(choices) for choices in [prav]]
    return [random.choice(names)]


generators = [
    get_fey_name,
]


def get_random_name(sb: Statblock):
    names = []
    for generator in generators:
        names.extend(generator(sb))
    if not names:
        return get_other_name(sb)[0]
    return random.choice(names)


if __name__ == '__main__':
    sb = Statblock.from_markdown(filename='statblocks/warrior.md')
    print(get_random_name(sb))
    sb = Statblock.from_markdown(filename='statblocks/predator.md')
    print(get_random_name(sb))
    sb = Statblock.from_markdown(filename='statblocks/predator.md')
    import tags.woc_fey_means
    sb = tags.woc_fey_means.all_tags['fey'].apply(sb)
    print(get_random_name(sb))

