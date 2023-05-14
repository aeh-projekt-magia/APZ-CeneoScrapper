import pytest
import sqlalchemy

from app.models.SubscriptionModel import Subscription
from app.models.ItemModel import Item
from app.models.UserModel import User
from repository.subscription.SubscriptionRepository import (
    addSubscriber,
    getSubscriber,
    getAllSubscribers,
    updateSubscriber,
    deleteSubscriber,
    deleteAllSubscribers,
)
from app import db


# TODO: Nie działają testy pod postgresem

test_subscription = {
    "itemId": 12345,
    "userId": 333,
    "notificationFreq": 1,
    "notifyOnPriceChange": False,
}


def test_subscription_model(app):
    sub = Subscription(
        test_subscription["itemId"],
        test_subscription["userId"],
        test_subscription["notificationFreq"],
        test_subscription["notifyOnPriceChange"],
    )

    assert test_subscription["itemId"] is sub.item_id
    assert test_subscription["userId"] is sub.user_id
    assert test_subscription["notificationFreq"] is sub.notification_frequency
    assert test_subscription["notifyOnPriceChange"] is sub.notify_on_price_change


def test_subscription_model_add(app):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    test_user = User(email="aa@aa.aa", password="a")
    db.session.add(test_user)
    db.session.commit()

    addSubscriber(
        test_item.id,
        test_user.id,
        test_subscription["notificationFreq"],
        test_subscription["notifyOnPriceChange"],
    )

    sub = db.session.execute(db.select(Subscription).filter_by(id=1)).scalar_one()

    assert test_item.id == sub.item_id
    assert test_user.id == sub.user_id
    assert test_subscription["notificationFreq"] == sub.notification_frequency
    assert test_subscription["notifyOnPriceChange"] == sub.notify_on_price_change
    assert sub.send_notification is not None


def test_subscription_model_get(app, capfd):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    test_user = User(email="aa@aa.aa", password="a")
    db.session.add(test_user)
    db.session.commit()

    addSubscriber(
        test_item.id,
        test_user.id,
        test_subscription["notificationFreq"],
        test_subscription["notifyOnPriceChange"],
    )
    getSubscriber(1)
    out, err = capfd.readouterr()

    assert str(test_item.id) in out
    assert str(test_user.id) in out
    assert str(test_subscription["notificationFreq"]) in out
    assert str(test_subscription["notifyOnPriceChange"]) in out


def test_subscription_model_get_all(app, capfd):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    test_user = User(email="aa@aa.aa", password="a")
    db.session.add(test_user)
    db.session.commit()

    test_item_2 = Item(name="test_item2")
    db.session.add(test_item)
    db.session.commit()

    test_user_2 = User(email="2aa@aa.aa", password="a")
    db.session.add(test_user)
    db.session.commit()

    addSubscriber(
        test_item.id,
        test_user.id,
        test_subscription["notificationFreq"],
        test_subscription["notifyOnPriceChange"],
    )
    addSubscriber(
        test_item_2.id,
        test_user_2.id,
        test_subscription["notificationFreq"],
        True,
    )

    getAllSubscribers()
    out, err = capfd.readouterr()

    assert str(test_item.id) in out
    assert str(test_user.id) in out
    assert str(test_subscription["notificationFreq"]) in out
    assert str(test_subscription["notifyOnPriceChange"]) in out
    assert str(test_item_2.id) in out
    assert str(test_user_2.id) in out
    assert str(True) in out


def test_subscription_model_update(app):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    test_user = User(email="aa@aa.aa", password="a")
    db.session.add(test_user)
    db.session.commit()

    addSubscriber(
        test_item.id,
        test_user.id,
        test_subscription["notificationFreq"],
        test_subscription["notifyOnPriceChange"],
    )
    updateSubscriber(1, 0, True, True)

    sub = db.session.execute(db.select(Subscription).filter_by(id=1)).scalar_one()

    assert test_subscription["notificationFreq"] != sub.notification_frequency
    assert test_subscription["notifyOnPriceChange"] != sub.notify_on_price_change
    assert sub.send_notification is not False


def test_subscription_model_delete_one(app):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    test_user = User(email="aa@aa.aa", password="a")
    db.session.add(test_user)
    db.session.commit()

    addSubscriber(
        test_item.id,
        test_user.id,
        test_subscription["notificationFreq"],
        test_subscription["notifyOnPriceChange"],
    )
    deleteSubscriber(1)

    with pytest.raises(sqlalchemy.exc.NoResultFound):
        db.session.execute(db.select(Subscription).filter_by(id=1)).scalar_one()


def test_subscription_model_delete_all(app, capfd):
    test_item = Item(name="test_item")
    db.session.add(test_item)
    db.session.commit()

    test_user = User(email="aa@aa.aa", password="a")
    db.session.add(test_user)
    db.session.commit()


    test_item_2 = Item(name="test_item2")
    db.session.add(test_item)
    db.session.commit()

    test_user_2 = User(email="2aa@aa.aa", password="a")
    db.session.add(test_user)
    db.session.commit()

    addSubscriber(
        test_item.id,
        test_user.id,
        test_subscription["notificationFreq"],
        test_subscription["notifyOnPriceChange"],
    )
    addSubscriber(
        test_item_2.id,
        test_user_2.id,
        test_subscription["notificationFreq"],
        True,
    )
    deleteAllSubscribers
    getAllSubscribers
    out, err = capfd.readouterr()

    assert out == ""
