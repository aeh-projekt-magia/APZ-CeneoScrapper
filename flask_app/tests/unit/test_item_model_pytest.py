import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from app.models.ItemModel import Item
from app.repository.ItemRepository import addItem,getItem,getAllItems,updateItem,deleteItem,deleteAllItems
from app import db

test_item = {
            'itemId': 12345,
            'itemName':'test',
            'isAvailable': False,
            'lowestPrice': 9.99,
            'offerUrl':'www.test.com'
            }


def test_item_model():
    '''Checks if the Item model works properly'''
    item = Item(test_item['itemId'],test_item['itemName'],test_item['isAvailable'],test_item['lowestPrice'],test_item['offerUrl'])
    
    assert test_item['itemId'] is item.item_id
    assert test_item['itemName'] is item.item_name
    assert test_item['isAvailable'] is item.is_available
    assert test_item['lowestPrice'] is item.lowest_price
    assert test_item['offerUrl'] is item.offer_url


def test_item_model_add(app,database):
    with app.app_context():
        addItem(test_item['itemId'],test_item['itemName'],test_item['isAvailable'],test_item['lowestPrice'],test_item['offerUrl'])
        item = db.session.execute(db.select(Item).filter_by(item_id=test_item['itemId'])).scalar_one()


    assert test_item['itemId'] == item.item_id
    assert test_item['itemName'] == item.item_name
    assert test_item['isAvailable'] == item.is_available
    assert test_item['lowestPrice'] == float(item.lowest_price)
    assert test_item['offerUrl'] == item.offer_url
    assert item.last_updated is not None

def test_item_model_get(app,database,capfd):
    with app.app_context():
        addItem(test_item['itemId'],test_item['itemName'],test_item['isAvailable'],test_item['lowestPrice'],test_item['offerUrl'])
        getItem(test_item['itemId'])
        out, err = capfd.readouterr()

    assert str(test_item['itemId']) in out
    assert str(test_item['itemName']) in out
    assert str(test_item['isAvailable']) in out
    assert str(test_item['lowestPrice']) in out
    assert str(test_item['offerUrl']) in out

def test_item_model_get_all(app,database,capfd):
    with app.app_context():
        addItem(test_item['itemId'],test_item['itemName'],test_item['isAvailable'],test_item['lowestPrice'],test_item['offerUrl'])
        addItem(54321,'flask',test_item['isAvailable'],test_item['lowestPrice'],test_item['offerUrl'])
        getAllItems()
        out, err = capfd.readouterr()

    assert str(test_item['itemId']) in out
    assert str(test_item['itemName']) in out
    assert str(54321) in out
    assert str('flask') in out

def test_item_model_update(app,database):
    with app.app_context():
        addItem(test_item['itemId'],test_item['itemName'],test_item['isAvailable'],test_item['lowestPrice'],test_item['offerUrl'])
        updateItem(test_item['itemId'],True,1.01)

        item = db.session.execute(db.select(Item).filter_by(item_id=test_item['itemId'])).scalar_one()

    assert item.is_available != test_item['isAvailable']
    assert float(item.lowest_price) != test_item['lowestPrice']

def test_item_model_delete_one(app,database):
    with app.app_context():
        addItem(test_item['itemId'],test_item['itemName'],test_item['isAvailable'],test_item['lowestPrice'],test_item['offerUrl'])
        deleteItem(test_item['itemId'])

        with pytest.raises(sqlalchemy.exc.NoResultFound):
            user = db.session.execute(db.select(Item).filter_by(item_id=test_item['itemId'])).scalar_one()
        
def test_item_model_delete_all(app,database,capfd):
    with app.app_context():
        addItem(test_item['itemId'],test_item['itemName'],test_item['isAvailable'],test_item['lowestPrice'],test_item['offerUrl'])
        addItem(54321,'flask',test_item['isAvailable'],test_item['lowestPrice'],test_item['offerUrl'])
        deleteAllItems()
        getAllItems()
        out, err = capfd.readouterr()
    
    assert out is ''