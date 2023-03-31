from abc import ABC, abstractmethod
from selenium import webdriver


class CeneoPage(ABC):
    @abstractmethod
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.base_url = 'https://www.ceneo.pl/'

        self.url = ''  # override in subclasses

    @abstractmethod
    def init_web_elements(self):
        """
        Initializes all the web elements that are available after loading the page and are needed
        for the page object to work properly.
        """
        ...

    def load(self):
        """
        Opens the browser loads the url and initializes the basic web elements.
        """
        full_url = self.base_url + self.url
        self.driver.get(full_url)
        self.driver.maximize_window()
        self.init_web_elements()

