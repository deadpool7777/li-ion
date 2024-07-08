from bs4 import BeautifulSoup

class StringField:
    def __init__(self, selector):
        self.selector = selector

    def extract_value(self, soup):
        element = soup.select_one(self.selector)
        return element.text.strip() if element else None
