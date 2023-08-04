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
from .ListTextFilter import ListTextFilter
from .ElementInfo import ElementInfo
from .ElementInfo import BlockType


class TextBoilerFilter:
    def __init__(self, text_block_xpath="//text()"):
        self._text_block_xpath = text_block_xpath
        self._filters_dict = {
            "word_count": NumWordsTextFilter(),
            "link_density": LinkDensityTextFilter(),
            "heading": HeadingTextFilter(),
            "list": ListTextFilter(),
        }
        self._element_info_table = []

    """
    Filter Rule Table
    """
    def filter_elements(self, main_element):
        self._apply_filters(main_element)
        self._local_classify()
        self._context_classify()
        self._remove_boiler()

    # 对 elements 使用 filters
    def _apply_filters(self, main_element):
        for element in main_element.xpath(self._text_block_xpath):
            element_info_entry = ElementInfo(element)
            # 是否字数及格
            element_info_entry.passed_word_count = self._filters_dict["word_count"].passed_filter(element)
            # 是否 link density 达标
            element_info_entry.passed_link_density = self._filters_dict["link_density"].passed_filter(element)
            # 认定是否可能是 heading
            element_info_entry.passed_heading = self._filters_dict["heading"].passed_filter(element)
            # 认定是 list element
            element_info_entry.passed_list = self._filters_dict["list"].pass_filter(element)
            # add element info to table
            self._element_info_table.append(element_info_entry)

    # 更改这个函数来调试分类规则
    # 按 filter 结果归类 elements
    def _local_classify(self):
        for entry in self._element_info_table:
            if not entry.passed_link_density:
                # 链接里的文本太多，定位垃圾
                entry.classification = BlockType.BOILER
            elif entry.passed_word_count and not entry.passed_heading:
                # 词数多，但不是 heading 字体。是主内容
                entry.classification = BlockType.FULL_TEXT
            else:
                entry.classification = BlockType.PENDING

    # 更改这个函数来调整分类规则
    def _context_classify(self):
        for i in range(len(self._element_info_table)):
            entry = self._element_info_table[i]
            # 已经被分类的。跳过
            if entry.classification != BlockType.UNCLASSIFIED and entry.classification != BlockType.PENDING:
                continue
            # 用附近元素判定认为可能是 heading 的是否真是 heading
            elif entry.passed_heading:
                if i + 1 >= len(self._element_info_table):
                    # 在文章底。肯定不是 heading。分为垃圾。
                    entry.classification = BlockType.BOILER
                else:
                    next_entry = self._element_info_table[i+1]
                    if next_entry.classification == BlockType.FULL_TEXT:
                        # 是真的 heading。
                        entry.classification = BlockType.HEADING
                    else:
                        # 后面不是主内容，大概率是垃圾
                        entry.classification = BlockType.BOILER
            # 很短的文本，但不是 link。用附近元素判断它是什么
            elif not entry.passed_word_count and not entry.passed_heading:
                if not entry.passed_list:
                    # 普通文本不该这么短，认定是垃圾
                    entry.classification = BlockType.BOILER
                else:
                    # 如果 list 到这里，说明它既没归为 Full text，也没归为垃圾。说明 list 很短但链接不多。
                    if i < 2:
                        entry.classification = BlockType.BOILER
                    elif self._element_info_table[i-1].classification == BlockType.FULL_TEXT:
                        entry.classification = BlockType.OTHER_RELATED
                    else:
                        entry.classification = BlockType.BOILER

    # 移除垃圾
    def _remove_boiler(self):
        for entry in self._element_info_table:
            if entry.classification == BlockType.BOILER:
                entry.element.xpath(".").remove()
