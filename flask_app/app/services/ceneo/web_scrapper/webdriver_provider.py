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
        self._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    @property
    def driver(self):
        return self._driver
