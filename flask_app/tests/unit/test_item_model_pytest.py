import pytest
import sqlalchemy

from app.models.ItemModel import Item
from app.repository.ItemRepository import (
    addItem,
    getItem_by_name,
    getAllItems,
    updateItem,
    deleteItem,
    deleteAllItems,
)
from app import db

test_item = {
    "name": "test",
    "is_available": False,
    "lowest_price": 9.99,
    "offer_url": "www.test.com",
}


# TODO: Przerobiłem trochę te testy - Jakub Turek


def test_item_model():
    """Checks if the Item model works properly"""
    item = Item(**test_item)

    assert test_item["name"] == item.name
    assert test_item["is_available"] == item.is_available
    assert test_item["lowest_price"] == item.lowest_price
    assert test_item["offer_url"] == item.offer_url


def test_item_model_add(app):
    addItem(**test_item)
    item = Item.query.where(Item.name == test_item["name"]).first()

    assert item.id is not None
    assert test_item["name"] == item.name
    assert test_item["is_available"] == item.is_available
    assert test_item["lowest_price"] == float(item.lowest_price)
    assert test_item["offer_url"] == item.offer_url
    assert item.last_updated is not None


def test_item_model_get(app):
    addItem(**test_item)
    item = getItem_by_name(test_item["name"])

    assert item.id is not None
    assert (test_item["name"]) == item.name
    assert (test_item["is_available"]) == item.is_available
    assert float(test_item["lowest_price"]) == float(item.lowest_price)
    assert (test_item["offer_url"]) == item.offer_url


def test_item_model_get_all(app):
    addItem(**test_item)
    addItem(
        "flask",
        test_item["is_available"],
        test_item["lowest_price"],
        test_item["offer_url"],
    )
    items = getAllItems()
    assert any(item.name in [test_item["name"], "flask"] for item in items)


def test_item_model_update(app):
    addItem(**test_item)
    item_to_update = getItem_by_name(name=test_item["name"])

    updateItem(item_to_update.id, True, 1.01)

    item = Item.query.where(Item.name == test_item["name"]).first()

    assert item.is_available != test_item["is_available"]
    assert float(item.lowest_price) != test_item["lowest_price"]


def test_item_model_delete_one(app):
    item = addItem(**test_item)
    deleteItem(item.id)

    with pytest.raises(sqlalchemy.exc.NoResultFound):
        db.session.execute(db.select(Item).filter_by(id=item.id)).scalar_one()


def test_item_model_delete_all(app, capfd):
    with app.app_context():
        addItem(**test_item)
        addItem(
            "flask",
            test_item["is_available"],
            test_item["lowest_price"],
            test_item["offer_url"],
        )
        deleteAllItems()
        getAllItems()
        out, err = capfd.readouterr()

    assert out == ""
