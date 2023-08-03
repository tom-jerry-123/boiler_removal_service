# Selects the main content of a web page given a response object
# Returns a dict encapsulating main_element selector and its info
# "main_element": main_content_element (selector object for main content)
# "text_density": text_density of main content
# "text_length": length of text in main content element
# "percent_total": percent of total text captured

class MainContentSelector:
    # method below selects the main content element
    def __init__(self, layout_xpath="//body", text_xpath="//text()"):
        self.layout_xpath = layout_xpath
        self.text_xpath = text_xpath

    # Main Content Selector
    def main_content_selector(self, response):
        main_content_element = None
        max_density = 0.0
        main_text_length = 0

        # Compute total text length
        total_text_length = 0
        for text in response.xpath(self.layout_xpath + self.text_xpath).getall():
            total_text_length += len(text.strip())

        # Text density by percentage of element code that is text
        for element in response.xpath(self.layout_xpath + "//*"):
            text_density = self.compute_text_density(element)
            text_length = text_density * len(str(element.get()))

            # print(text_density, text_length/total_text_length)
            # Check if we have element with better text density
            if text_density > max_density and 0.5 < text_length / total_text_length:
                main_content_element = element
                max_density = text_density
                main_text_length = text_length

        main_content_info = {
            "main_element": main_content_element,
            "text_density": max_density,
            "text_length": main_text_length,
            "percent_total": main_text_length / total_text_length
        }

        # Return main content element and its stats after text density analysis finishes
        return main_content_info

    """""""""""
    Helper methods
    """""""""""
    # compute text density of an element
    def compute_text_density(self, element):
        text_length = 0
        text_list = element.xpath("." + self.text_xpath).getall()
        for text in text_list:
            text_length += len(text.strip())
        element_length = len(str(element.get()))
        # Calculate text density
        text_density = text_length / element_length
        return text_density

    # logs info about main content
    def log_main_info(self, main_content_info, url, outfile="Not known"):
        # Log failure message if program did not find main_content
        if main_content_info["main_element"] is None:
            print("\n\n############################################\n\n"
                  "!!! Program failed, exiting parser !!!"
                  "\n\n############################################\n\n")
            with open("ScrapedData/parse_log.txt", "a", encoding='utf8') as f:
                f.write(url + "\n")
                f.write("\tParse failed: parser could not find main content\n")
            return None

        # Log details if successful
        with open("ScrapedData/parse_log.txt", "a", encoding='utf8') as f:
            main_content_name = main_content_info["main_element"].xpath("@class").get()
            log_msg = f"; Max Density: {main_content_info['text_density']}, " \
                      f"Percent of total text: {main_content_info['percent_total']}, " \
                      f"Length: {main_content_info['text_length']}, " \
                      f"File: {outfile}"
            if main_content_name is not None:
                log_msg = main_content_name + log_msg
            f.write(url + "\n")
            f.write("\t" + log_msg + "\n")
