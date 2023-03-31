from app.extensions import db
import datetime

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.text)
    password = db.Column(db.text)
    is_admin = db.Column(db.boolean, default = False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __str__(self):
        return (str(self.user_id) + " " + self.email_address + " " + 
                str(self.password) + " " + str(self.is_admin) + " " +
                str(self.created_on))