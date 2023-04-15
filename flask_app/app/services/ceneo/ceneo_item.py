from app.services.ceneo.item_interface import ItemInterface

from app.services.ceneo.web_scrapper.webdriver_provider import WebdriverProvider
from app.services.ceneo.web_scrapper.operations.item_operations import ItemOperations
from datetime import datetime
import sys


class CeneoItem(ItemInterface):
    provider = WebdriverProvider
    item_operations = ItemOperations

    def __init__(self):
        self.driver = self.provider().driver
        self.item_operations = self.item_operations(self.driver)

    def fetch_lowest_price(self, item_id: str) -> dict:
        offer_data = self.item_operations.find_cheapest_offer(item_id).as_dict()
        lowest_price = dict(
            item_id=offer_data['item_id'],
            item_name=offer_data['item_name'],
            price=offer_data['price'],
            offer=offer_data['offer_url'],
            shop_name=offer_data['shop_name'],
            timestamp=datetime.now(),
        )
        return lowest_price

    def find_id_by_item_name(self, item_name: str) -> str:
        return ''
