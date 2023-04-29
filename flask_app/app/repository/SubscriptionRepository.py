from app.models.SubscriptionModel import Subscription
from app.extensions import db


def addSubscriber(itemId, userId, notificationFreq, notifyOnPriceChange):
    newSubscriber = Subscription(itemId, userId, notificationFreq, notifyOnPriceChange)
    db.session.add(newSubscriber)
    db.session.commit()


def getSubscriber(subscriptionId):
    subscriber = db.session.execute(
        db.select(Subscription).filter_by(id=subscriptionId)
    ).scalar_one()
    print(subscriber)


def getAllSubscribers():
    subscribers = db.session.execute(db.select(Subscription)).scalars()
    for x in subscribers:
        print(x)


def deleteSubscriber(subscriptionId):
    subscriber = db.session.execute(
        db.select(Subscription).filter_by(id=subscriptionId)
    ).scalar_one()
    db.session.delete(subscriber)
    db.session.commit()


def deleteAllSubscribers():
    db.session.query(Subscription).delete()
    db.session.commit()


def updateSubscriber(
    subscriptionId, notificationFreq, notifyOnPriceChange, sendNotification
):
    subscriber = db.session.execute(
        db.select(Subscription).filter_by(id=subscriptionId)
    ).scalar_one()

    subscriber.notification_frequency = notificationFreq
    subscriber.notify_on_price_change = notifyOnPriceChange
    subscriber.send_notification = sendNotification

    db.session.commit()
