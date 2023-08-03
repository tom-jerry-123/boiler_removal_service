# Link Density Text Filter

from . import Tokenizer


class LinkDensityTextFilter:
    @staticmethod
    def _get_link_density(element):
        num_words = 0
        num_words_in_link = 0
        for text in element.xpath(".//text()").getall():
            num_words += len(Tokenizer.trim_and_tokenize(text))
        for text in element.xpath(".//text()[ancestor::a]").getall():
            num_words_in_link += len(Tokenizer.trim_and_tokenize(text))
        if num_words == 0:
            return 2
        return num_words_in_link / num_words

    # Assign a score for this metric
    def score(self, element):
        return self._get_link_density(element)

    # determines whether element passes this filter
    def passed_filter(self, element):
        return self._get_link_density(element) < 0.35
