from app.models.ItemModel import Item
from app.extensions import db
import datetime


# TODO: Przerobiłem troche repozytorium - Jakub Turek


def addItem(name, is_available, lowest_price, offer_url):
    newItem = Item(
        name=name,
        is_available=is_available,
        lowest_price=lowest_price,
        offer_url=offer_url,
    )
    db.session.add(newItem)
    db.session.commit()
    return newItem


def getItem_by_name(name):
    item = db.session.execute(db.select(Item).filter_by(name=name)).scalar_one()
    return item


def getAllItems():
    items = db.session.execute(db.select(Item)).all()
    items = Item.query.all()
    return items


def deleteItem(id):
    item = db.session.execute(db.select(Item).filter_by(id=id)).scalar_one()
    db.session.delete(item)
    db.session.commit()


def deleteAllItems():
    db.session.query(Item).delete()
    db.session.commit()


def updateItem(id, is_available, lowest_price):
    # item = db.session.execute(db.select(Item).filter_by(id=id)).scalar_one()
    item = Item.query.where(Item.id == id).first()

    item.is_available = is_available
    item.lowest_price = lowest_price
    item.last_updated = datetime.datetime.now()

    db.session.commit()
