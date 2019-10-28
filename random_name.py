import random
import numpy as np
import re
from collections import defaultdict
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

special_consonant_mapping = {text: i for text, i in
  zip(['shch', 'sch', 'sh', 'ch', 'kh', 'ts', 'dzh', 'zh', 'ph', 'lh'],
      r'01234569789!@#$%^&*()+_.,/\?')
}
reverse_special_consonant_mapping = {v: k for k, v in special_consonant_mapping.items()}


def encode_consonants(word):
    """This is a really dumb way to deal with the problem of multiple letter consonants, 
    but it was the first thing that I thought of."""
    for k, v in special_consonant_mapping.items():
        word = word.replace(k, v)
    return word


def decode_consonants(word):
    for k, v in reverse_special_consonant_mapping.items():
        word = word.replace(k, v)
    return word


def is_vowel(letter: str):
    if letter in {'a', 'e', 'i', 'o', 'u', 'y'}:
        return True


def is_consonant(letter: str):
    if letter == 'y':
        return True
    return not is_vowel(letter)


def word_to_phonemes(word: str, max_length=5):
    word = list(encode_consonants(word.lower()))
    
    phonemes = []
    current_phoneme = ''
    found_vowel = False
    while len(word) > 2:
        letter = word.pop(0)
        current_phoneme += letter
        if (is_consonant(letter) and found_vowel) or len(current_phoneme) >= max_length:
            phonemes.append(current_phoneme)
            current_phoneme = ''
            found_vowel = False
        if is_vowel(letter):
            found_vowel = True
    if len(current_phoneme) < 2:
        phonemes.append(current_phoneme + ''.join(word))
    else:
        phonemes.append(current_phoneme)
        phonemes.append(''.join(word))

    return [decode_consonants(p) for p in phonemes]


def build_markov(text: str):
    """Breaks text up into words by whitespace, then breaks those words up into phonemes.
    Uses these phonemes to create a markov chain which can be used to create words
    similar to those in the text."""
    text = text\
        .replace(',', ' ')\
        .replace('.', ' ')\
        .replace(';', '') \
        .replace(':', '') \
        .replace('?', '') \
        .replace('!', '') \
        .replace('"', '')
        # .replace('-', '')\
        # .replace('\'', '') \
    words = set([word.lower() for word in re.split(r'\W+', text) if len(word) > 2])
    phoneme_groups = [word_to_phonemes(word) for word in words]

    markov_counts = defaultdict(lambda: defaultdict(int))
    top_level = []
    for phoneme_group in phoneme_groups:
        top_level.append(phoneme_group[0])
        last_phoneme = phoneme_group[0].lower()
        for phoneme in phoneme_group[1:]:
            phoneme = phoneme.lower()
            markov_counts[last_phoneme][phoneme] += 1
            last_phoneme = phoneme

    markov_chain = {'': (top_level, np.ones(len(top_level)) / len(top_level))}
    for phoneme, counts in markov_counts.items():
        keys = []
        values = []
        for key, value in counts.items():
            keys.append(key)
            values.append(value)
        markov_chain[phoneme] = (keys, np.array(values) / sum(values))

    return markov_chain


def walk_markov(markov_chain, steps, last_phoneme=None):
    if steps <= 0:
        return []
    if last_phoneme is None:
        last_phoneme = random.choice(list(markov_chain.keys()))
        return [last_phoneme] + walk_markov(markov_chain, steps - 1, last_phoneme)
    choices, probabilities = markov_chain[last_phoneme]
    if not choices:
        return [last_phoneme] + walk_markov(markov_chain, steps - 1, random.choice(list(markov_chain.keys())))
    choice = np.random.choice(choices, p=probabilities)
    if choice == last_phoneme:
        return [last_phoneme] + walk_markov(markov_chain, steps - 1, random.choice(list(markov_chain.keys())))
    return [choice] + walk_markov(markov_chain, steps - 1, last_phoneme)


def make_markov_word(markov_chain, max_phonemes=4, min_phonemes=2, max_length=11, min_length=3):
    word = ''
    while len(word) < min_length or len(word) > max_length:
        number_phonemes = random.randint(min_phonemes, max_phonemes + 1)
        word = ''.join(walk_markov(markov_chain, number_phonemes, ''))
    return word


def file_to_markov_ready_text(filename):
    # todo accept multiple file names e.g. so we can have prav_fey + prav_brumal
    with open(filename) as file_handle:
        lines = file_handle.read().splitlines()
    lines = [line for line in lines if not line.startswith('#')]
    return ' '.join(lines)

markov_chains = {
    'prav_fey': build_markov(re.sub(r'[^A-Za-z\s]+', '', file_to_markov_ready_text('name_lists/prav_fey.txt')))
}


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

    names = [
        make_markov_word(markov_chains['prav_fey'], max_phonemes=4, min_phonemes=2, max_length=12, min_length=4)
    ]
    return [random.choice(names)]


generators = [
    get_fey_name,
]


def get_random_name(sb: Statblock):
    """Get a random name from the list of functions in `generators`. These functions should only return names if the
    stat block meets some criteria, e.g. it must be the fey type to get a fey name. If there are no eligible names,
    uses `get_other_name()`."""
    # todo filter swear words
    names = []
    for generator in generators:
        names.extend(generator(sb))
    if not names:
        return get_other_name(sb)[0]
    return random.choice(names)


if __name__ == '__main__':
    from pprint import pprint as pp
    pp(markov_chains)
    names = []
    for _ in range(10):
        # sb = Statblock.from_markdown(filename='statblocks/warrior.md')
        # print(get_random_name(sb))
        # sb = Statblock.from_markdown(filename='statblocks/predator.md')
        # print(get_random_name(sb))
        sb = Statblock.from_markdown(filename='statblocks/predator.md')
        import tags.woc_fey_means
        sb = tags.woc_fey_means.all_tags['fey'].apply(sb)
        names.append(get_random_name(sb))
    print(''.join(['{:<13}'.format(name) for name in names]))

