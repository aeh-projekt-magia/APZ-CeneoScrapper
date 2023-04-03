from app.extensions import db
import datetime

class User(db.Model):

    __tablename__ = "users"

    user_id: int
    email: str
    password: str
    is_admin: bool
    created_on: datetime

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.text,unique = True,nullable=False)
    password = db.Column(db.text, nullable=False)
    is_admin = db.Column(db.boolean, default = False, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    
    def __init__(self, email, password, is_admin=False, is_confirmed=False):
        self.email = email
        self.password = password
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"<email {self.email}>"
    
    def __str__(self):
        return (str(self.user_id) + " " + self.email_address + " " + 
                str(self.password) + " " + str(self.is_admin) + " " +
                str(self.created_on))