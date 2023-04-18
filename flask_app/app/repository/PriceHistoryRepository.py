from app.models.PriceHistoryModel import PriceHistory
from app.extensions import db

def addPriceHistoryRecord(itemId, price):
    newRecord = PriceHistory(itemId,
                             price)
    db.session.add(newRecord)
    db.session.commit()

def getPriceHistoryRecord(id):
    record = db.session.execute(db.select(PriceHistory).filter_by(price_id=id)).scalar_one()
    print(record)

def getAllPriceHistoryRecords():
    records = db.session.execute(db.select(PriceHistory)).scalars()
    for x in records:
        print(x)

def deletePriceHistoryRecord(id):
    record = db.session.execute(db.select(PriceHistory).filter_by(price_id=id)).scalar_one()
    db.session.delete(record)
    db.session.commit()

def deleteAllPriceHistoryRecords():
    db.session.query(PriceHistory).delete()
    db.session.commit()
