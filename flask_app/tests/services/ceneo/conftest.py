import pytest
from app.services.ceneo.ceneo_item import CeneoItem
from app.services.ceneo.web_scrapper.data_objects.offer_data import OfferData
from app.services.ceneo.web_scrapper.operations.item_operations import ItemOperations

from app.services.ceneo.web_scrapper.data_objects.item_data import ItemData
from app.services.ceneo.web_scrapper.operations.item_search_operations import (
    ItemSearchOperations,
)


@pytest.fixture
def mocked_webdriver_provider(mocker):
    class MockWebDriverProvider:
        def __init__(self):
            self.driver = None

    mocker.patch.object(CeneoItem, "provider", MockWebDriverProvider)


@pytest.fixture
def mocked_item_operations(mocker, offer_data, item_id_):
    class MockedItemOperations(ItemOperations):
        def __init__(self, driver):
            super().__init__(driver)

        def find_cheapest_offer(self, item_id: str) -> OfferData:
            if item_id == item_id_:
                return offer_data

    mocker.patch.object(CeneoItem, "item_operations", MockedItemOperations)


@pytest.fixture
def mocked_item_search_operations(mocker, item_data, item_name_):
    class MockedItemSearchOperations(ItemSearchOperations):
        def __init__(self, driver):
            super().__init__(driver)

        def find_item_by_name(self, item_name: str) -> ItemData:
            if item_name == item_name_:
                return item_data

    mocker.patch.object(CeneoItem, "item_search_operations", MockedItemSearchOperations)


@pytest.fixture
def item_data_params(item_id_):
    return {
        "item_id": item_id_,
        "item_name": "test_item_name",
        "item_search_name": "test_item_search_name",
        "image_url": "img.url",
        "item_price": 1000.00
    }


@pytest.fixture
def item_data(item_data_params):
    item_data = ItemData(**item_data_params)
    return item_data


@pytest.fixture
def offer_data_params(item_id_):
    return {
        "item_name": "test_item_name",
        "item_id": item_id_,
        "price": 1000.00,
        "shop_name": "test_shop_name.com",
        "offer_url": "https://test_shop_name.com/offers/abc12",
    }


@pytest.fixture
def offer_data(offer_data_params):
    offer_data = OfferData(**offer_data_params)
    return offer_data


@pytest.fixture
def item_id_():
    return "97863463"


@pytest.fixture
def item_name_():
    return "Apple iPhone 13"


@pytest.fixture
def ceneo_item_mocks(
    mocked_webdriver_provider, mocked_item_operations, mocked_item_search_operations
):
    # mock all dependencies using fixtures
    ...
