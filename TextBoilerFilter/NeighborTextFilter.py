# Filters text elements based on features of neighboring elements
# only affects "indeterminate cases" i.e. passing exactly one of link density and word count filters
# Does not appear useful

"""
Rule book
Word count, Link density
1, 1 = text neighbor
0, 1 =
*, 0 = boilerplate neighbor
"""


class NeighborTextFilter:
    def score_all_elements(self, main_element):
        pass

    def score(self, element):
        pass

    def pass_filter(self, element):
        pass
