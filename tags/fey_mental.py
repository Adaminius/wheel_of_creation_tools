from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'Fey Mental'

all_tags.append(Tag('inscrutable motivations', '-'))
all_tags.append(Tag('appetite for mortal flesh', '-'))
all_tags.append(Tag('loner', '-'))
all_tags.append(Tag('predator', '-'))
all_tags.append(Tag('territorial', '-'))
all_tags.append(Tag('gregarious', '-', overwritten_by={'loner'}, overwrites={'loner'}))


all_tags = dict([(tag.name, tag) for tag in all_tags])
