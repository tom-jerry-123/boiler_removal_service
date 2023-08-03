
import markdownify as md
import scrapy
from TextBoilerFilter import TextBoilerFilter
from MainContentFilter import MainContentSelector


class FilterSpider(scrapy.Spider):
    name = 'filter_spider'
    start_urls = [
        # "https://docs.kaleido.io/kaleido-services/digital-assets/token-explorer/",
        # "https://docs.kaleido.io/kaleido-services/document-store/architecture/",
        # "https://www.cointime.com/news/zippychain-23786",
        "https://www.cointime.com/flash-news/bitcoin-miner-reserve-increasing-despite-stagnant-prices-below-95298",
        "https://coinmarketcap.com/community/articles/64a82ac1a6ec74147bcb7208/",
    ]
    urls_parsed = set()
    layout_xpath_list = ["//body"]
    # xpath of text blocks
    text_block_xpath = "//*[self::p or self::h1 or self::h2 or self::h3 or self::li " \
                       "or self::div[not(descendant::p or descendant::div)]][descendant::text()]"
    # xpath of relevant text nodes
    text_xpath = "//text()[(ancestor::p or ancestor::h1 or ancestor::h2 or ancestor::h3 " \
                 "or ancestor::code or ancestor::li) " \
                 "and not(ancestor::header or ancestor::nav or ancestor::footer)]"
    strongly_protected_xpath = "//code"
    outfile_name = "ScrapedData/output-{}.md"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, headers={'User-Agent': 'Mozilla/5.0'})

    def parse(self, response):
        # print(response.text)
        response.xpath("//iframe | //header | //footer | //nav").remove()
        # use text density analysis to find main content
        # main_content_info = self.main_content_selector(response)
        # layout = main_content_info['main_element']
        layout = response.xpath(self.layout_xpath_list[0])

        # log whether algorithm successful
        # self.log_message(main_content_info, response.url)
        text_filter = TextBoilerFilter()
        text_filter.filter_elements(layout, self.text_block_xpath)

        main_content_filter = MainContentSelector(text_xpath=self.text_xpath)
        main_content_info = main_content_filter.main_content_selector(response)
        layout = main_content_info["main_element"]

        main_content_filter.log_main_info(main_content_info, response.url, "output-{}.md".format(len(self.urls_parsed)+1))

        layout.xpath("//figcaption | //button | //script | //style").remove()
        layout.xpath("//*[not(descendant::text())]").remove()

        self.urls_parsed.add(response.url)
        self.output_website(layout)

    def output_website(self, layout):
        content = md.markdownify(
            layout.get(),
            strip=["a"],
            autolinks=True,
            default_title=True,
            heading_style=md.ATX,
            strong_em_symbol=md.UNDERSCORE,
            newline_style=md.BACKSLASH,
        )

        with open(self.outfile_name.format(len(self.urls_parsed)), "w", encoding='utf8') as f:
            f.write(content)
