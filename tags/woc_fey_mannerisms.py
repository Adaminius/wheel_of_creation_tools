from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'WoC: Fey Mannerisms'
table_description = 'If there is one unifying quality among the fey that inhabit the Ring of Seasons, it is that ' \
                    'none of them operate with the same morality or instincts that resemble those of humanity. Their ' \
                    'minds and bodies are not so separated, and they are bound to pacts and laws ' \
                    'ultimately incomprehensible to inhabitants of the Ring of Earth.'

all_tags.append(Tag('cannot break a promise', effect_text='-', weight=40))
all_tags.append(Tag('cannot speak a lie', '-', weight=40))
all_tags.append(Tag('cannot cross a threshold', '-', weight=40))
all_tags.append(Tag('ascetic', effect_text='-', weight=3))
all_tags.append(Tag('hedonist', effect_text='-', weight=3))
all_tags.append(Tag('guardian of a worthless treasure', effect_text='-'))
all_tags.append(Tag('prankster', effect_text='-', weight=20, requires={'Summery'}))
all_tags.append(Tag('hunger for souls', effect_text='-', weight=10))
all_tags.append(Tag('appetite for mortal flesh', '-', stacks=True))
all_tags.append(Tag('thirsts for favors', effect_text='-', weight=20))
all_tags.append(Tag('just regular hunger', effect_text='-'))
all_tags.append(Tag('illogical', effect_text='-'))
all_tags.append(Tag('cold logic', effect_text='-', requires={'Wintry'}))
all_tags.append(Tag('fears that which it was created to destroy', '-', weight=5))
all_tags.append(Tag('indiscriminately homicidal', effect_text='-'))
all_tags.append(Tag('utterly inscrutable motivations', '-', weight=20))
all_tags.append(Tag('hatred for mortals', '-', weight=20))
all_tags.append(Tag('love for mortals', '-', weight=5))
all_tags.append(Tag('love for a mortal', '-', weight=2))
all_tags.append(Tag('hatred for the Courts', '-'))
all_tags.append(Tag('love for the Courts', '-'))
all_tags.append(Tag('loner', '-', overwritten_by={'social'}, overwrites={'social'}))
all_tags.append(Tag('gregarious', '-', overwritten_by={'social'}, overwrites={'social'}))

all_tags = dict([(tag.name, tag) for tag in all_tags])
