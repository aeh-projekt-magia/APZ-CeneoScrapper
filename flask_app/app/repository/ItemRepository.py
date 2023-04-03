from app.models.ItemModel import Item
from app.extensions import db
import datetime

def addItem(itemId, itemName, isAvailable, lowestPrice, offerUrl):
    newItem = Item(itemId,
                   itemName,
                   isAvailable,
                   lowestPrice,
                   offerUrl)
    db.session.add(newItem)
    db.session.commit()

def getItem(itemId):
    item = db.session.execute(db.select(Item).filter_by(item_id=itemId)).scalar_one()
    print(item)

def getAllItems():
    items = db.session.execute(db.select(Item)).scalars()
    for x in items:
        print(x)

def deleteItem(itemId):
    item = db.session.execute(db.select(Item).filter_by(item_id=itemId)).scalar_one()
    db.session.delete(item)
    db.session.commit()

def deleteAllItems():
    db.session.query(Item).delete()
    db.session.commit()

def updateItem(itemId,isAvailable,lowestPrice):

    item = db.session.execute(db.select(Item).filter_by(item_id=itemId)).scalar_one()

    item.is_available = isAvailable
    item.lowest_price = lowestPrice
    item.last_updated = datetime.datetime.now()

    db.session.commit()

