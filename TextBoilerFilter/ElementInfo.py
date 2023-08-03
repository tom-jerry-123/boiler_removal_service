# 不是 Filter
# 用来储存有关 element 的信息的

from enum import Enum


class BlockType(Enum):
    UNKNOWN = 0
    # 主要内容
    FULL_TEXT = 1
    HEADING = 2
    # 其他可能有关的
    OTHER_RELATED = 3
    # 垃圾
    BOILER = 4


class ElementInfo:
    # parameter type list (Selector, Bool, Bool, Bool)
    def __init__(self, element, passed_word_count=None, passed_link_density=None, passed_heading=None):
        self.element = element
        self.passed_word_count = passed_word_count
        self.passed_link_density = passed_link_density
        self.passed_heading = passed_heading
        self.classification = BlockType.UNKNOWN
