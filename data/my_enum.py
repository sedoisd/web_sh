import enum


class TopicParentType(enum.Enum):
    group = 'group'
    category = 'category'
    forum = 'forum'


class ForumParentType(enum.Enum):
    group = 'group'
    category = 'category'


class CategoryParentType(enum.StrEnum):
    group = 'group'
