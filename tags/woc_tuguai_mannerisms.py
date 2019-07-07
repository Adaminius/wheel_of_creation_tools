from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'WoC: Tuguai Mannerisms'
table_description = 'Coming soon!'
img_url = ''

all_tags.append(Tag('cannot break a promise', effect_text='-', weight=20))


all_tags = dict([(tag.name, tag) for tag in all_tags])
