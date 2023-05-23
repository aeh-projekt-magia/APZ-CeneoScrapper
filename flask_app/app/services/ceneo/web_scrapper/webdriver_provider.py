from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


class WebdriverProviderMeta(type):
    """
    Singleton metaclass. Thread unsafe, do not use for multithreading.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class WebdriverProvider(metaclass=WebdriverProviderMeta):
    """
    Singleton class that assures only one webdriver instance is used in the application.
    """

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        self._driver = webdriver.Remote("http://selenium:4444/wd/hub", options=options)

    @property
    def driver(self):
        return self._driver
