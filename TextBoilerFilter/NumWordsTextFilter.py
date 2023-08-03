# Num Words Text Filter
# Local ‘微观’ Filter
# 靠元素词数来判定相关性


class NumWordsTextFilter:
    # Fix method to take care of chinese characters as well
    @staticmethod
    def _count_words(element):
        num_words = 0
        for text in element.xpath(".//text()").getall():
            num_words += len(text.strip().split())
        return num_words

    # Assign a score. 1 = keep, 0 = remove
    def score(self, element):
        num_words = self._count_words(element)
        return 1 if num_words > 6 else 0

    # Boolean assessment metric. Pass or fail
    def passed_filter(self, element):
        return self.score(element) >= 1
