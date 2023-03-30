from app.models.ItemModel import Item
from app.extensions import db
import datetime

def addItem(itemId, itemName, isAvailable, lowestPrice, offerUrl):
    newItem = Item(item_id = itemId,
                   item_name = itemName,
                   is_available = isAvailable,
                   lowest_price = lowestPrice,
                   offer_url = offerUrl)
    db.session.add(newItem)
    db.session.commit()

def getItem(itemId):
    for x in db.session.query(Item).filter(Item.item_id == itemId):
        print(x)

def getAllItems():
    for x in db.session.query(Item):
        print(x)

def deleteItem(itemId):
    db.session.query(Item).filter(Item.item_id == itemId).delete()
    db.session.commit()

def deleteAllItems():
    db.session.query(Item).delete()
    db.session.commit()

def updateItem(itemId,isAvailable,lowestPrice):

    updatedItem = db.session.query(Item).get(itemId)

    updatedItem.is_available = isAvailable
    updatedItem.lowest_price = lowestPrice
    updatedItem.last_updated = datetime.datetime.now()

    db.session.commit()

