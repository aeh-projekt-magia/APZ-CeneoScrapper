from datetime import datetime

import pytest
from app.services.ceneo.ceneo_item import CeneoItem


@pytest.mark.unit_test
def test_fetch_lowest_price(ceneo_item_mocks, offer_data_params, item_id_, offer_data):
    expected_lowest_price_dict = {
        "item_id": item_id_,
        "item_name": offer_data_params["item_name"],
        "price": offer_data_params["price"],
        "offer": offer_data_params["offer_url"],
        "shop_name": offer_data_params["shop_name"],
        "timestamp": datetime.now(),
    }

    ceneo_item = CeneoItem()
    lowest_price_dict = ceneo_item.fetch_lowest_price(item_id_)
    assert isinstance(lowest_price_dict.pop("timestamp"), datetime)
    expected_lowest_price_dict.pop("timestamp")
    assert lowest_price_dict == expected_lowest_price_dict


@pytest.mark.unit_test
def test_find_id_by_item_name(ceneo_item_mocks, item_name_, item_data_params):
    expected_id_dict = {
        "item_id": item_data_params["item_id"],
        "item_name": item_data_params["item_name"],
        "item_search_name": item_data_params["item_search_name"],
        "image_url": "img.url"
    }

    ceneo_item = CeneoItem()
    item_id_dict = ceneo_item.find_id_by_item_name(item_name_)
    assert item_id_dict == expected_id_dict


@pytest.mark.e2e
def test_e2e_fetch_lowest_price(item_id_):
    ceneo_item = CeneoItem()
    lowest_price_dict = ceneo_item.fetch_lowest_price(item_id_)
    assert lowest_price_dict["item_id"] == item_id_
    assert "Apple iPhone 13" in lowest_price_dict["item_name"]
    assert lowest_price_dict["price"] > 0.0
    assert len(lowest_price_dict["offer"]) > 0
    assert len(lowest_price_dict["shop_name"]) > 0


@pytest.mark.e2e
def test_e2e_find_id_by_item_name(item_name_):
    ceneo_item = CeneoItem()
    item_id_dict = ceneo_item.find_id_by_item_name(item_name_)
    assert len(item_id_dict["item_id"]) > 0
    assert "Apple iPhone 13" in item_id_dict["item_name"]
    assert item_id_dict["item_search_name"] == item_name_
    assert len(item_id_dict["image_url"]) > 0
