import pytest
import sqlalchemy

from app.models.PriceHistoryModel import PriceHistory
from app.models.ItemModel import Item
from repository.price_history.PriceHistoryRepository import (
    addPriceHistoryRecord,
    getPriceHistoryRecord,
    getAllPriceHistoryRecords,
    deletePriceHistoryRecord,
    deleteAllPriceHistoryRecords,
)
from app import db


# TODO: Nie działają testy pod postgresem

test_price_history = {
    "itemId": 12345,
    "price": 9.99,
}


def test_price_history_model():
    """Checks if the price history model works properly"""
    priceHis = PriceHistory(
        item_id=test_price_history["itemId"], price=test_price_history["price"]
    )

    assert test_price_history["itemId"] is priceHis.item_id
    assert test_price_history["price"] is priceHis.price


def test_price_history_model_add(app):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    addPriceHistoryRecord(test_item.id, test_price_history["price"])

    priceHis = db.session.execute(
        db.select(PriceHistory).filter_by(price_id=1)
    ).scalar_one()

    assert test_item.id == priceHis.item_id
    assert test_price_history["price"] == float(priceHis.price)
    assert priceHis.price_id is not None
    assert priceHis.date is not None


def test_price_history_model_get(app, capfd):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    addPriceHistoryRecord(test_item.id, test_price_history["price"])
    getPriceHistoryRecord(1)
    out, err = capfd.readouterr()

    assert str(test_item.id) in out
    assert str(test_price_history["price"]) in out


def test_price_history_model_get_all(app, capfd):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    test_item_2 = Item(name="test_item_2")
    db.session.add(test_item_2)
    db.session.commit()

    addPriceHistoryRecord(test_item.id, test_price_history["price"])
    addPriceHistoryRecord(test_item_2.id, test_price_history["price"] + 1)

    getAllPriceHistoryRecords()
    out, err = capfd.readouterr()

    assert str(test_item.id) in out
    assert str(test_price_history["price"]) in out
    assert str(test_item.id + 1) in out
    assert str(test_price_history["price"] + 1) in out


def test_price_history_model_delete_one(app):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    addPriceHistoryRecord(test_item.id, test_price_history["price"])
    deletePriceHistoryRecord(1)

    with pytest.raises(sqlalchemy.exc.NoResultFound):
        db.session.execute(db.select(PriceHistory).filter_by(price_id=1)).scalar_one()


def test_price_history_model_delete_all(app, capfd):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    test_item_2 = Item(name="test_item_2")
    db.session.add(test_item_2)
    db.session.commit()

    addPriceHistoryRecord(test_item.id, test_price_history["price"])
    addPriceHistoryRecord(test_item_2.id, test_price_history["price"] + 1)

    deleteAllPriceHistoryRecords()
    out, err = capfd.readouterr()

    assert out == ""
