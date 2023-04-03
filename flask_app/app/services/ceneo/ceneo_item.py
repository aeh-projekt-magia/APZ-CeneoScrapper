from app.services.ceneo.item_interface import ItemInterface

from services.ceneo.web_scrapper.webdriver_provider import WebdriverProvider
from services.ceneo.web_scrapper.operations.item_operations import ItemOperations
from datetime import datetime


class CeneoItem(ItemInterface):
    def __init__(self):
        self.driver = WebdriverProvider().driver

    def fetch_lowest_price(self, item_id: str) -> dict:
        offer_data = ItemOperations(self.driver).find_cheapest_offer(item_id).as_dict()
        lowest_price = dict(
            item_id=offer_data['item_id'],
            item_name=offer_data['item_name'],
            price=offer_data['price'],
            offer=offer_data['offer_url'],
            timestamp=datetime.now(),
        )
        return lowest_price

    def find_id_by_item_name(self, item_name: str) -> str:
        return ''
