import requests
from bs4 import BeautifulSoup
import logging

from entity import Entity
from fields import StringField

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class BatteryData(Entity):
    """Represents data about a specific battery type."""
    battery_name = StringField('h1')
    capacity = StringField('div.capacity')
    voltage = StringField('div.voltage')
    weight = StringField('div.weight')
    # images = StringField('img::attr(src)', all=True)
    # images = StringField('a[class="S_C_full_size"]::attr("data-src")')

class BatteryScraper:
    BASE_URL = 'https://doi.org/10.3390/en11051073'

    def __init__(self, battery_type):
        self.battery_type = battery_type
        self.entity = BatteryData

    def fetch_and_parse(self, url):
        log.info(f'Fetching data from {url}...')
        response = requests.get(url)
        if response.status_code != 200:
            log.error(f'Failed to fetch {url}. Status code: {response.status_code}')
            return None
        return BeautifulSoup(response.content, 'html.parser')

    def extract_data(self, soup):
        log.info(f'Extracting data for {self.battery_type}...')
        return self.entity.from_soup(soup)

    def run(self):
        url = self.BASE_URL
        soup = self.fetch_and_parse(url)
        if soup:
            battery_data = self.extract_data(soup)
            log.info(f'Successfully extracted data for {self.battery_type}')
            return battery_data
        else:
            log.error(f'Failed to extract data for {self.battery_type}')
            return None

def main():
    # Example usage:
    battery_type = 'NCR18650B'
    scraper = BatteryScraper(battery_type)
    battery_data = scraper.run()

    if battery_data:
        print("Battery Information:")
        print(f"Battery Name: {battery_data.battery_name}")
        print(f"Capacity: {battery_data.capacity}")
        print(f"Voltage: {battery_data.voltage}")
        print(f"Weight: {battery_data.weight}")
        # if battery_data.images:
        #    print("Images:")
        # for image in battery_data.images:
        #     print(image)
    else:
        print(f"Failed to fetch data for {battery_type}")

if __name__ == "__main__":
    main()
