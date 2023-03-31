from enum import Enum
from typing import List, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from flask_app.app.services.ceneo.web_scrapper.ceneo_offer_data import CeneoOfferData
from flask_app.app.services.ceneo.web_scrapper.ceneo_page import CeneoPage


class SortingOptions(Enum):
    BEST_OFFERS = "najlepszych ofert"
    LOWEST_PRICE = "najniższej ceny"
    HIGHEST_PRICE = "najwyższej ceny"
    LOWEST_PRICE_W_SHIPPING = "najniższej ceny z dostawą"
    HIGHEST_PRICE_W_SHIPPING = "najwyższej ceny z dostawą"
    HIGHEST_AVAILABILITY = "najlepszej dostępności"
    HIGHEST_RANKED = "najwyżej ocenianych"
    LOWEST_RANKED = "najniższej ocenianych"

    @staticmethod
    def locator(sorting_option) -> Tuple[By, str]:
        """
        Builds a locator for the given sorting option
        Args:
            sorting_option: SortingOptions enum member

        Returns:
            XPATH Locator of the given sorting option
        """
        return By.XPATH, f"//div[contains(@class, 'dropdown-menu')]/a[text() = '{sorting_option.value}']"


class CeneoItemPage(CeneoPage):

    # selenium locators
    l_sort_dropdown = (By.XPATH, "//body/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]"
                                 "/div[5]/div[2]/div[1]/div[1]/div[1]/div[1]/a[1]")
    l_offers = (By.CSS_SELECTOR, ".product-offers__list__item")

    def __init__(self, driver: webdriver.Chrome, item_id: str):
        super().__init__(driver)
        self.url = item_id
        self.sort_dropdown: WebElement = ...
        self.sort_dropdown_items: List[WebElement] = ...
        self.offers: List[CeneoOfferData] = ...

    def init_web_elements(self):
        self.sort_dropdown = self.driver.find_element(*self.l_sort_dropdown)
        self._load_offers()

    def sort_offers_by(self, by: SortingOptions):
        """
        Sorts the displayed offers related to the item by chosen option.
        Args:
            by: sorting option - enum member of SortingOptions.
        """
        l_sorting_option = SortingOptions.locator(by)
        wait = WebDriverWait(self.driver, 5)

        self.sort_dropdown.click()
        wait.until(EC.element_to_be_clickable(l_sorting_option))
        sorting_option = self.driver.find_element(*l_sorting_option)
        sorting_option.click()

        self._load_offers()

    def get_first_offer(self) -> CeneoOfferData:
        """
        Locates the web element of the top offer displayed and converts it to a data object.
        Returns:
            Data object that represents the offer located on the top of the offers list.
        """
        if not self.offers:
            self._load_offers()
        return self.offers[0]

    def _load_offers(self):
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_all_elements_located(self.l_offers))
        self.offers = [
            CeneoOfferData(element) for element in self.driver.find_elements(*self.l_offers)
        ]

