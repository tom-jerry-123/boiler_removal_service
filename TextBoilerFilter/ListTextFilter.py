# Filter 判断元素是否是 list

from . import Tokenizer


class ListTextFilter:
    @staticmethod
    def _is_list(element):
        return element.xpath("self::ul | self::ol").get() is not None

    def score(self, element):
        return 1 if self._is_list(element) else 0

    def pass_filter(self, element):
        return self._is_list_element(element)
