from selenium.webdriver.remote.webelement import WebElement

from services.ceneo.web_scrapper.data_objects.ceneo_data_object import CeneoDataObject


class OfferData(CeneoDataObject):
    def __init__(self, item_name: str = '', item_id: str = '', price: float = 0,
                 shop_url: str = '', offer_url: str = ''):
        self.item_name = item_name
        self.item_id = item_id
        self.price = price
        self.shop_url = shop_url
        self.offer_url = offer_url

    def as_string(self):
        return f"item name = {self.item_name}\n" \
               f"item id = {self.item_id}\n" \
               f"price = {self.price}\n" \
               f"shop url = {self.shop_url}\n" \
               f"offer url = {self.offer_url}"

    def as_dict(self):
        return dict(
            item_name=self.item_name,
            item_id=self.item_id,
            price=self.price,
            shop_url=self.shop_url,
            offer_url=self.offer_url,
        )