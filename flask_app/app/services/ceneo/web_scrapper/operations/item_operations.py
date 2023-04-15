from selenium.webdriver.chrome.webdriver import WebDriver

from app.services.ceneo.web_scrapper.data_objects.offer_data import OfferData
from app.services.ceneo.web_scrapper.page_objects.item_page import ItemPage, SortingOptions


class ItemOperations:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def find_cheapest_offer(self, item_id: str) -> OfferData:
        item_page = ItemPage(self.driver, item_id)
        item_page.load()
        item_page.sort_offers_by(SortingOptions.LOWEST_PRICE)
        cheapest_offer = item_page.get_first_offer()
        return cheapest_offer
