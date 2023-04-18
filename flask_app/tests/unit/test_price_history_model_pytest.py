import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from app.models.PriceHistoryModel import PriceHistory
from app.repository.PriceHistoryRepository import addPriceHistoryRecord,getPriceHistoryRecord,getAllPriceHistoryRecords,deletePriceHistoryRecord,deleteAllPriceHistoryRecords
from app import db

test_price_history= {
                    'itemId': 12345,
                    'price':9.99,
                    }

def test_price_history_model():
    '''Checks if the price history model works properly'''
    priceHis = PriceHistory(test_price_history['itemId'],test_price_history['price'])

    assert test_price_history['itemId'] is priceHis.item_id
    assert test_price_history['price'] is priceHis.price

def test_price_history_model_add(app,database):
    with app.app_context():
        addPriceHistoryRecord(test_price_history['itemId'],test_price_history['price'])
        
        priceHis = db.session.execute(db.select(PriceHistory).filter_by(price_id=1)).scalar_one()

    assert test_price_history['itemId'] == priceHis.item_id
    assert test_price_history['price'] == float(priceHis.price)
    assert priceHis.price_id is not None
    assert priceHis.date is not None

def test_price_history_model_get(app,database,capfd):
    with app.app_context():
        addPriceHistoryRecord(test_price_history['itemId'],test_price_history['price'])
        getPriceHistoryRecord(1)
        out, err = capfd.readouterr()

            
    assert str(test_price_history['itemId']) in out
    assert str(test_price_history['price']) in out

def test_price_history_model_get_all(app,database,capfd):

    with app.app_context():
        addPriceHistoryRecord(test_price_history['itemId'],test_price_history['price'])
        addPriceHistoryRecord(test_price_history['itemId']+1,test_price_history['price']+1)
        
        getAllPriceHistoryRecords()
        out, err = capfd.readouterr()
    
    assert str(test_price_history['itemId']) in out
    assert str(test_price_history['price']) in out
    assert str(test_price_history['itemId']+1) in out
    assert str(test_price_history['price']+1) in out

def test_price_history_model_delete_one(app,database):
    with app.app_context():
        addPriceHistoryRecord(test_price_history['itemId'],test_price_history['price'])
        deletePriceHistoryRecord(1)

        with pytest.raises(sqlalchemy.exc.NoResultFound):
            priceHis = db.session.execute(db.select(PriceHistory).filter_by(price_id=1)).scalar_one()

def test_price_history_model_delete_all(app,database,capfd):
    with app.app_context():
        addPriceHistoryRecord(test_price_history['itemId'],test_price_history['price'])
        addPriceHistoryRecord(test_price_history['itemId']+1,test_price_history['price']+1)
        
        deleteAllPriceHistoryRecords()
        out, err = capfd.readouterr()
    
    assert out is ''
    