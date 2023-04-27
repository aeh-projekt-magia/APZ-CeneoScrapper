from enum import Enum
from typing import List, Tuple

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.services.ceneo.web_scrapper.data_objects.offer_data import OfferData
from app.services.ceneo.web_scrapper.page_objects.ceneo_page import CeneoPage


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
        return (
            By.XPATH,
            f"//div[contains(@class, 'dropdown-menu')]/a[text() = '{sorting_option.value}']",
        )


class ItemPage(CeneoPage):
    # selenium locators
    l_sort_dropdown = (
        By.XPATH,
        "//body/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]"
        "/div[5]/div[2]/div[1]/div[1]/div[1]/div[1]/a[1]",
    )
    l_offers = (By.CSS_SELECTOR, ".product-offer__container")
    l_item_name = (By.XPATH, "//div[contains(@class, 'product-top__title')]/h1")

    def __init__(self, driver: webdriver.Chrome, item_id: str):
        super().__init__(driver)
        self.url = item_id
        self.sort_dropdown: WebElement = ...
        self.item_name: WebElement = ...
        self.offers: List[OfferData] = ...

    def init_web_elements(self):
        self.sort_dropdown = self.driver.find_element(*self.l_sort_dropdown)
        self.item_name = self.driver.find_element(*self.l_item_name)

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
        self.init_web_elements()
        self._load_offers()

    def get_all_offers(self) -> List[OfferData]:
        self._load_offers()
        return self.offers

    def get_first_offer(self) -> OfferData:
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
            self._web_element_to_offer(element)
            for element in self.driver.find_elements(*self.l_offers)
        ]

    def _web_element_to_offer(self, web_element: WebElement) -> OfferData:
        l_offer_url = (By.XPATH, ".//a[contains(@class, 'go-to-shop')]")
        l_buy_now_button = (
            By.XPATH,
            ".//button[contains(@class, 'add-to-basket-no-popup')]",
        )
        l_data_and_opinions = (
            By.XPATH,
            "./parent::node()//ul[contains(@class, 'product-offer__details__toolbar__links')]/li[1]/a[1]",
        )

        item_name = self.item_name.text
        shop_name = (
            web_element.find_element(*l_data_and_opinions)
            .get_attribute("textContent")
            .replace("Dane i opinie o ", "")
            .strip()
        )

        try:
            # handle offers with go-to-shop layout
            offer_url_web_element = web_element.find_element(*l_offer_url)
            item_id = web_element.get_attribute("data-productid")
            price = float(web_element.get_attribute("data-price"))
            offer_url = offer_url_web_element.get_attribute("href")
        except (TypeError, NoSuchElementException):
            # handle offers with add-to-cart layout
            buy_now_button = web_element.find_element(*l_buy_now_button)
            item_id = buy_now_button.get_attribute("data-product")
            price = float(buy_now_button.get_attribute("data-price"))
            offer_url = f'ceneo.pl{web_element.get_attribute("data-click-url")}'

        return OfferData(
            item_name=item_name,
            item_id=item_id,
            price=price,
            shop_name=shop_name,
            offer_url=offer_url,
        )
