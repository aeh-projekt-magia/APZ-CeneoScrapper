from app.extensions import db
import datetime
from dataclasses import dataclass
from flask_login import UserMixin
from app.extensions import db, bcrypt



@dataclass
class User(UserMixin, db.Model):

    __tablename__ = "users"

    id: int
    email: str
    password: str
    is_admin: bool
    created_on: datetime

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String,unique = True,nullable=False)
    password = db.Column(db.String , nullable=False)
    is_admin = db.Column(db.Boolean, default = False, nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    
    def __init__(self, email, password, is_admin=False,is_confirmed=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed

    def __repr__(self):
        return f"<email {self.email}>"
    
    def __str__(self):
        return (str(self.id) + " " + self.email + " " + 
                str(self.password) + " " + str(self.is_admin) + " " +
                str(self.created_on))