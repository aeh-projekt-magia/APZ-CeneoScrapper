from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.services.ceneo.web_scrapper.page_objects.ceneo_page import CeneoPage
from services.ceneo.web_scrapper.data_objects.item_data import ItemData


class ItemsSearchPage(CeneoPage):

    # selenium locators
    l_products = (By.CSS_SELECTOR, ".cat-prod-row")
    l_category_list = (By.CSS_SELECTOR, "category-list-body")
    l_first_product = (By.XPATH,
                       "//div[contains(@class, 'category-list-body')]/div[contains(@class, 'cat-prod-row')]")

    def __init__(self, driver: webdriver.Chrome, item_name: str):
        super().__init__(driver)
        self.item_search_name = item_name.strip()
        self.url = f'szukaj-{self._format_whitespaces(item_name)}'
        self.first_product: WebElement = ...

    def init_web_elements(self):
        self.first_product = self.driver.find_element(*self.l_first_product)

    def get_first_product(self) -> ItemData:
        return self._web_element_to_product(self.first_product)

    def _web_element_to_product(self, web_element: WebElement) -> ItemData:
        item_id = web_element.get_attribute('data-productid')
        item_name = web_element.get_attribute('data-productname')
        return ItemData(
            item_id=item_id,
            item_name=item_name,
            item_search_name=self.item_search_name
        )

    @staticmethod
    def _format_whitespaces(string: str):
        return string.strip().replace(' ', '+')
