# Text Filter 服务
# Text Filter 下有几个可用的 Filter。各有自己的标准，按需使用
# Text Filter 只用于删除杂乱文本 (英文叫 "boilerplate")
# Filters 可以给文本打分。高分 - 大概率是重要的。低分 - 大概率是垃圾
# Filters 也可以衡量文本是否达标
# 可调试 Filter 严格。严格 - 只留确认是需要的。松懈 - 只删确认是垃圾的

# ！！！ 可调式代码 ！！！

from .LinkDensityTextFilter import LinkDensityTextFilter
from .NumWordsTextFilter import NumWordsTextFilter
from .HeadingTextFilter import HeadingTextFilter
from .ElementInfo import ElementInfo
from .ElementInfo import BlockType


class TextBoilerFilter:
    def __init__(self):
        self._filters_dict = {
            "word_count": NumWordsTextFilter(),
            "link_density": LinkDensityTextFilter(),
            "heading": HeadingTextFilter(),
        }
        self._element_info_table = []

    """
    Filter Rule Table
    Word count, Link density, Heading
    1, 1, 1 -> 留
    1, 1, 0 -> 留
    0, 1, 1 -> 留
    0, 1, 0 -> 删
    *, 0, * -> 删
    """
    def filter_elements(self, main_element, text_block_xpath):
        self._apply_filters(main_element, text_block_xpath)
        self._local_classify()
        self._remove_boiler()

    # 对 elements 使用 filters
    def _apply_filters(self, main_element, text_block_xpath):
        for element in main_element.xpath(text_block_xpath):
            element_info_entry = ElementInfo(element)
            # 是否字数及格
            element_info_entry.passed_word_count = self._filters_dict["word_count"].passed_filter(element)
            # 是否 link density 达标
            element_info_entry.passed_link_density = self._filters_dict["link_density"].passed_filter(element)
            # 认定是否可能是 heading
            element_info_entry.passed_heading = self._filters_dict["heading"].passed_filter(element)
            # add element info to table
            self._element_info_table.append(element_info_entry)

    # 按 filter 结果归类 elements
    def _local_classify(self):
        for entry in self._element_info_table:
            if not entry.passed_link_density:
                # 链接里的文本太多，定位垃圾
                entry.classification = BlockType.BOILER
            elif not entry.passed_word_count and not entry.passed_heading:
                # 词数太少且不可能是 heading，也是垃圾
                entry.classification = BlockType.BOILER
            elif entry.passed_word_count and not entry.passed_heading:
                # 词数多，但不是 heading 字体。是主内容
                entry.classification = BlockType.FULL_TEXT
            elif entry.passed_heading:
                # 剩下之是 heading
                entry.classification = BlockType.HEADING

    def _context_classify(self):
        pass

    # 移除垃圾
    def _remove_boiler(self):
        for entry in self._element_info_table:
            if entry.classification == BlockType.BOILER:
                entry.element.xpath(".").remove()
