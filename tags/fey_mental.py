from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'Fey Mental'

all_tags.append(Tag('inscrutable motivations', '-'))
all_tags.append(Tag('appetite for mortal flesh', '-', stacks=True))
all_tags.append(Tag('loner', '-', overwritten_by={'social'}, overwrites={'social'}))
all_tags.append(Tag('predator', '-'))
all_tags.append(Tag('territorial', '-'))
all_tags.append(Tag('gregarious', '-', overwritten_by={'social'}, overwrites={'social'}))


all_tags = dict([(tag.name, tag) for tag in all_tags])
