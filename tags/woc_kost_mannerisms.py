from utils import common_actions
from utils import Feature
from statblock import Statblock
from statblock import Tag

all_tags = []
table_name = 'WoC: Kostlyavets Mannerisms'
table_description = \
"""todo
"""

all_tags.append(Tag('fear of sunlight', '-', weight=10))
all_tags.append(Tag('fear of garlic', '-', weight=10))
all_tags.append(Tag('fear of right-angles', '-', weight=10))

all_tags = dict([(tag.name, tag) for tag in all_tags])
