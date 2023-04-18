from app.models.UserModel import User
from app.extensions import db

def addUser(emailAddress,userPassword,isAdmin):
    newUser = User(emailAddress,
                   userPassword,
                   isAdmin)
    db.session.add(newUser)
    db.session.commit()

def getUser(emailAddress):
    user = db.session.execute(db.select(User).filter_by(email=emailAddress)).scalar_one()
    print(user)

def getAllUsers():
    users = db.session.execute(db.select(User)).scalars()
    for x in users:
        print(x)
    
def deleteUser(emailAddress):
    user = db.session.execute(db.select(User).filter_by(email=emailAddress)).scalar_one()
    db.session.delete(user)
    db.session.commit()

def deleteAllUsers():
    db.session.query(User).delete()
    db.session.commit()

def updateUser(oldemail,emailAddress,userPassword,isAdmin):

    user = db.session.execute(db.select(User).filter_by(email=oldemail)).scalar_one()

    user.email = emailAddress
    user.password = userPassword
    user.is_admin = isAdmin

    db.session.commit()