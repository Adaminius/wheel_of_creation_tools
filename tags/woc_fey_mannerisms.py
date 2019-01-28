from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'WoC: Fey Mannerisms'

all_tags.append(Tag('wants favors', effect_text='-', weight=20))
all_tags.append(Tag('can\'t break a promise', effect_text='-', weight=40))
all_tags.append(Tag('ascetic', effect_text='-', weight=3))
all_tags.append(Tag('wants souls', effect_text='-', weight=10))
all_tags.append(Tag('guardian', effect_text='-', weight=5))
all_tags.append(Tag('prankster', effect_text='-', weight=20, requires={'Summery'}))
all_tags.append(Tag('illogical', effect_text='-'))
all_tags.append(Tag('cold logic', effect_text='-', requires={'Wintry'}))
all_tags.append(Tag('indiscriminately homicidal', effect_text='-'))
all_tags.append(Tag('inscrutable motivations', '-', weight=20))
all_tags.append(Tag('appetite for mortal flesh', '-', stacks=True))
all_tags.append(Tag('loner', '-', overwritten_by={'social'}, overwrites={'social'}))
all_tags.append(Tag('gregarious', '-', overwritten_by={'social'}, overwrites={'social'}))

all_tags = dict([(tag.name, tag) for tag in all_tags])
