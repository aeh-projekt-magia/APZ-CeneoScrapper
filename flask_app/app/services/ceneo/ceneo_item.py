from app.services.ceneo.item_interface import ItemInterface

from app.services.ceneo.web_scrapper.webdriver_provider import WebdriverProvider
from app.services.ceneo.web_scrapper.operations.item_operations import ItemOperations
from datetime import datetime
import sys

from services.ceneo.web_scrapper.operations.item_search_operations import ItemSearchOperations


class CeneoItem(ItemInterface):
    provider = WebdriverProvider
    item_operations = ItemOperations
    item_search_operations = ItemSearchOperations

    def __init__(self):
        self.driver = self.provider().driver
        self.item_operations = self.item_operations(self.driver)
        self.item_search_operations = self.item_search_operations(self.driver)

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

    def find_id_by_item_name(self, item_name: str) -> dict:
        item_data = self.item_search_operations.find_item_by_name(item_name).as_dict()
        item_id = dict(
            item_id=item_data['item_id'],
            item_name=item_data['item_name'],
            item_search_name=item_data['item_search_name']
        )
        return item_id
