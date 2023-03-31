from selenium.webdriver.remote.webelement import WebElement

from flask_app.app.services.ceneo.web_scrapper.ceneo_data_object import CeneoDataObject


class CeneoOfferData(CeneoDataObject):
    def __init__(self, web_element: WebElement):
        ...

    def as_string(self):
        pass

    def as_dict(self):
        pass

