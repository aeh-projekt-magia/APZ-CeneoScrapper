from datetime import datetime

import pytest
from services.ceneo.ceneo_item import CeneoItem
from services.ceneo.web_scrapper.data_objects.offer_data import OfferData
from services.ceneo.web_scrapper.operations.item_operations import ItemOperations
from unittest.mock import patch, MagicMock


@pytest.fixture
def mocked_webdriver_provider(mocker):
    class MockWebDriverProvider:
        def __init__(self):
            self.driver = None

    mocker.patch.object(
        CeneoItem,
        'provider',
        MockWebDriverProvider
    )


@pytest.fixture
def mocked_item_operations(mocker, offer_data, item_id_):
    class MockedItemOperations(ItemOperations):
        def __init__(self, driver):
            super().__init__(driver)

        def find_cheapest_offer(self, item_id: str) -> OfferData:
            if item_id == item_id_:
                return offer_data

    mocker.patch.object(
        CeneoItem,
        'item_operations',
        MockedItemOperations
    )


@pytest.fixture
def offer_data(offer_data_params):
    offer_data = OfferData(**offer_data_params)
    return offer_data


@pytest.fixture
def offer_data_params(item_id_):
    return {
        'item_name': 'test_item_name',
        'item_id': item_id_,
        'price': 1000.00,
        'shop_name': 'test_shop_name.com',
        'offer_url': 'https://test_shop_name.com/offers/abc12'
    }


@pytest.fixture
def item_id_():
    return '97863463'


@pytest.fixture
def ceneo_item_mocks(mocked_webdriver_provider, mocked_item_operations):
    ...


@pytest.mark.unit_test
def test_fetch_lowest_price(ceneo_item_mocks, offer_data_params, item_id_, offer_data):
    expected_lowest_price_dict = {
        'item_id': item_id_,
        'item_name': offer_data_params['item_name'],
        'price': offer_data_params['price'],
        'offer': offer_data_params['offer_url'],
        'shop_name': offer_data_params['shop_name'],
        'timestamp': datetime.now()
    }

    ceneo_item = CeneoItem()
    lowest_price_dict = ceneo_item.fetch_lowest_price(item_id_)
    assert isinstance(lowest_price_dict.pop('timestamp'), datetime)
    expected_lowest_price_dict.pop('timestamp')
    assert lowest_price_dict == expected_lowest_price_dict


@pytest.mark.e2e
def test_e2e_fetch_lowest_price(item_id_):
    ceneo_item = CeneoItem()
    lowest_price_dict = ceneo_item.fetch_lowest_price(item_id_)
    assert lowest_price_dict['item_id'] == item_id_
    assert "Apple iPhone 13" in lowest_price_dict['item_name']
    assert lowest_price_dict['price'] > 0.0
    assert len(lowest_price_dict['offer']) > 0
    assert len(lowest_price_dict['shop_name']) > 0

