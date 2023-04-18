import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from app.models.SubscriptionModel import Subscription
from app.repository.SubscriptionRepository import addSubscriber,getSubscriber,getAllSubscribers,updateSubscriber,deleteSubscriber,deleteAllSubscribers
from app import db


test_subscription ={
            'itemId': 12345,
            'userId':333,
            'notificationFreq': 1,
            'notifyOnPriceChange': False
            }

def test_subscription_model():
    sub = Subscription(test_subscription['itemId'],test_subscription['userId'],test_subscription['notificationFreq'],test_subscription['notifyOnPriceChange'])

    assert test_subscription['itemId'] is sub.item_id
    assert test_subscription['userId'] is sub.user_id
    assert test_subscription['notificationFreq'] is sub.notification_frequency
    assert test_subscription['notifyOnPriceChange'] is sub.notify_on_price_change

def test_subscription_model_add(app,database):
    with app.app_context():
        addSubscriber(test_subscription['itemId'],test_subscription['userId'],test_subscription['notificationFreq'],test_subscription['notifyOnPriceChange'])
        
        sub = db.session.execute(db.select(Subscription).filter_by(subscription_id=1)).scalar_one()

    assert test_subscription['itemId'] == sub.item_id
    assert test_subscription['userId'] == sub.user_id
    assert test_subscription['notificationFreq'] == sub.notification_frequency
    assert test_subscription['notifyOnPriceChange'] == sub.notify_on_price_change
    assert sub.send_notification is not None

def test_subscription_model_get(app,database,capfd):
    with app.app_context():
        addSubscriber(test_subscription['itemId'],test_subscription['userId'],test_subscription['notificationFreq'],test_subscription['notifyOnPriceChange'])
        getSubscriber(1)
        out, err = capfd.readouterr()

            
    assert str(test_subscription['itemId']) in out
    assert str(test_subscription['userId']) in out
    assert str(test_subscription['notificationFreq']) in out
    assert str(test_subscription['notifyOnPriceChange']) in out

def test_subscription_model_get_all(app,database,capfd):

    with app.app_context():
        addSubscriber(test_subscription['itemId'],test_subscription['userId'],test_subscription['notificationFreq'],test_subscription['notifyOnPriceChange'])
        addSubscriber(test_subscription['itemId']+1,test_subscription['userId']+1,test_subscription['notificationFreq'],True)
        
        getAllSubscribers()
        out, err = capfd.readouterr()
    
    assert str(test_subscription['itemId']) in out
    assert str(test_subscription['userId']) in out
    assert str(test_subscription['notificationFreq']) in out
    assert str(test_subscription['notifyOnPriceChange']) in out
    assert str(test_subscription['itemId']+1) in out
    assert str(test_subscription['userId']+1) in out
    assert str(True) in out

def test_subscription_model_update(app,database):
    with app.app_context():
        addSubscriber(test_subscription['itemId'],test_subscription['userId'],test_subscription['notificationFreq'],test_subscription['notifyOnPriceChange'])
        updateSubscriber(1,0,True,True)

        sub = db.session.execute(db.select(Subscription).filter_by(subscription_id=1)).scalar_one()

    assert test_subscription['notificationFreq'] != sub.notification_frequency
    assert test_subscription['notifyOnPriceChange'] != sub.notify_on_price_change
    assert sub.send_notification != False

def test_subscription_model_delete_one(app,database):
    with app.app_context():
        addSubscriber(test_subscription['itemId'],test_subscription['userId'],test_subscription['notificationFreq'],test_subscription['notifyOnPriceChange'])
        deleteSubscriber(1)

        with pytest.raises(sqlalchemy.exc.NoResultFound):
            sub = db.session.execute(db.select(Subscription).filter_by(subscription_id=1)).scalar_one()

def test_subscription_model_delete_all(app,database,capfd):
    with app.app_context():
        addSubscriber(test_subscription['itemId'],test_subscription['userId'],test_subscription['notificationFreq'],test_subscription['notifyOnPriceChange'])
        addSubscriber(test_subscription['itemId']+1,test_subscription['userId']+1,test_subscription['notificationFreq'],True)
        deleteAllSubscribers
        getAllSubscribers
        out, err = capfd.readouterr()
    
    assert out is ''