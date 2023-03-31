from selenium import webdriver

from flask_app.app.services.ceneo.web_scrapper.ceneo_page import CeneoPage


class CeneoItemsSearchPage(CeneoPage):
    def __init__(self, driver: webdriver.Chrome):
        pass

    def init_web_elements(self):
        pass
