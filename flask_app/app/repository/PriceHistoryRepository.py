from app.models.PriceHistoryModel import PriceHistory
from app.extensions import db

def addPriceHistoryRecord(itemId, price):
    newRecord = PriceHistory(item_id = itemId,
                             price = price)
    db.session.add(newRecord)
    db.session.commit()

def getPriceHistoryRecord(id):
    record = db.session.execute(db.select(PriceHistory).filter_by(id=id)).scalar_one()
    print(record)

def getAllPriceHistoryRecords():
    records = db.session.execute(db.select(PriceHistory)).scalars()
    for x in records:
        print(x)

def deleteItem(id):
    record = db.session.execute(db.select(PriceHistory).filter_by(id=id)).scalar_one()
    db.session.delete(record)
    db.session.commit()

def deleteAllItems():
    db.session.query(PriceHistory).delete()
    db.session.commit()
