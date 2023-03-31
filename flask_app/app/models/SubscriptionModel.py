from app.extensions import db

class Subscription(db.Model):
    subscription_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('Item.item_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    notification_frequency = db.Column(db.Integer, default = 0)
    notify_on_price_change = db.Column(db.Boolean, default = False)
    send_notification = db.Column(db.Boolean, default = False)

    def __str__(self):
        return (str(self.subscription_id) + " " + self.item_id + " " + 
                str(self.user_id) + " " + str(self.notification_frequency) + " " +
                str(self.notify_on_price_change) + " " + str(self.send_notification))