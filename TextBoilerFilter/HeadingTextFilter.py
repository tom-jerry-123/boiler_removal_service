# Heading Filter
# 检测文本元素里的字是否符合 heading 的字体，字数
# 达标元素可能是 Heading，但不保证是
# 非达标的几乎 100% 不是 Heading

from enum import Enum


class TextType(Enum):
    ALL = 1
    NORMAL = 2
    BOLD = 3
    ITALIC = 4
    BOLD_ITALIC = 5
    LINK = 6


class HeadingTextFilter:
    def __init__(self, strict_pass=False):
        self._strict_pass = strict_pass

    @staticmethod
    def _count_words(element, text_type=TextType.ALL):
        num_words = 0
        wanted_text_xpath = ""
        if text_type == TextType.ALL:
            wanted_text_xpath = ".//text()"
        elif text_type == TextType.BOLD:
            wanted_text_xpath = ".//text()[ancestor::b or ancestor::strong]"
        elif text_type == TextType.ITALIC:
            wanted_text_xpath = ".//text()[ancestor::i or ancestor::em]"
        elif isinstance(text_type, TextType):
            raise ValueError("Type of text requested is not supported by method.")
        else:
            raise TypeError("Input for text_type parameter not of class 'TextType'.")

        for text in element.xpath(wanted_text_xpath).getall():
            num_words += len(text.strip().split())

        return num_words

    def score(self, text_block_element):
        num_bold_words = self._count_words(element=text_block_element, text_type=TextType.BOLD)
        num_italic_words = self._count_words(element=text_block_element, text_type=TextType.ITALIC)
        total_words = self._count_words(element=text_block_element)
        # 无词 - 不是文本。词数太多 - 是主文章，不是 heading
        if total_words == 0 or total_words > 15:
            return 0
        elif num_italic_words / total_words > 0.35 or num_italic_words > 3:
            # 太多斜体 - 不是 heading
            return 0
        elif text_block_element.xpath("self::h1 | self::h2 | self::h3").get() is not None:
            # HTML 用 heading tag。
            # print("Found heading tag: \n" + text_block_element.get())
            return 1
        elif num_bold_words == total_words:
            return 0.5
        return 0

    def passed_filter(self, text_block_element):
        ele_score = self.score(text_block_element)
        if self._strict_pass:
            return ele_score > 1.0
        return ele_score > 0.0
