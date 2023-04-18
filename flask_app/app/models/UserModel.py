from app.extensions import db
import datetime
from dataclasses import dataclass

#datetime.datetime.utcnow
@dataclass
class User(db.Model):

    __tablename__ = "users"

    user_id: int
    email: str
    password: str
    is_admin: bool
    created_on: datetime

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String,unique = True,nullable=False)
    password = db.Column(db.String , nullable=False)
    is_admin = db.Column(db.Boolean, default = False, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    
    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return f"<email {self.email}>"
    
    def __str__(self):
        return (str(self.user_id) + " " + self.email + " " + 
                str(self.password) + " " + str(self.is_admin) + " " +
                str(self.created_on))