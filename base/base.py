import requests
from lxml import etree

class BaseSpider:
    def __init__(self, url, xpath_dict):
        self.url = url
        self.xpath_dict = xpath_dict

    def fetch_page(self, url):
        """Fetch the content of the webpage."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")
            return None


# Example usage:
if __name__ == "__main__":
    url = "https://example.com"  # Replace with your target URL
    xpath = "//a/@href"  # Replace with your desired XPath expression
    xpath_dict = {}
    spider = BaseSpider(url, xpath_dict)
    spider.run()
