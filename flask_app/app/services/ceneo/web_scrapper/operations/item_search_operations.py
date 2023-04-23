from selenium.webdriver.chrome.webdriver import WebDriver

from services.ceneo.web_scrapper.data_objects.item_data import ItemData
from services.ceneo.web_scrapper.page_objects.items_search_page import ItemsSearchPage


class ItemSearchOperations:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def find_item_by_name(self, item_name: str) -> ItemData:
        item_search_page = ItemsSearchPage(self.driver, item_name)
        item_search_page.load()
        return item_search_page.get_first_product()
