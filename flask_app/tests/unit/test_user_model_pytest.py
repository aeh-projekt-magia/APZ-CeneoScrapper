import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from app.models.UserModel import User
from app.repository.UserRepository import addUser, getUser, getAllUsers, updateUser, deleteUser, deleteAllUsers
from app import db

test_user = {
            'email': 'test@test.com',
            'password':'strongpassword',
            'is_admin': False
            }


def test_user_model():
    user = User(test_user['email'],test_user['password'],test_user['is_admin'])

    assert test_user['email'] is user.email
    assert test_user['password'] != user.password
    assert test_user['is_admin'] is user.is_admin

def test_user_model_add(app,database):
    with app.app_context():
        addUser(test_user['email'],test_user['password'],test_user['is_admin'])
        user = db.session.execute(db.select(User).filter_by(email=test_user['email'])).scalar_one()


    assert user.id is not None
    assert user.email == test_user['email']
    assert user.password != test_user['password']
    assert user.is_admin == test_user['is_admin']
    assert user.created_on is not None

def test_user_model_get(app,database,capfd):
    with app.app_context():
        addUser(test_user['email'],test_user['password'],test_user['is_admin'])
        getUser(test_user['email'])
        out, err = capfd.readouterr()
    
    assert test_user['email'] in out
    #assert test_user['password'] in out
    assert str(test_user['is_admin']) in out

def test_user_model_get_all(app,database,capfd):

    with app.app_context():
        addUser(test_user['email'],test_user['password'],test_user['is_admin'])
        addUser("1" +test_user['email'],'1'+test_user['password'],True)
        
        getAllUsers()
        out, err = capfd.readouterr()
    
    assert test_user['email'] in out
    #assert test_user['password'] in out
    assert str(test_user['is_admin']) in out
    assert ('1'+test_user['email']) in out
    #assert ('1'+test_user['password']) in out
    assert 'True' in out


def test_user_model_update(app,database):
    with app.app_context():
        addUser(test_user['email'],test_user['password'],test_user['is_admin'])
        updateUser(test_user['email'],"newmail@mail.com","newpass",True)

        user = db.session.execute(db.select(User).filter_by(email="newmail@mail.com")).scalar_one()

    assert user.email != test_user['email']
    assert user.password != test_user['password']
    assert user.is_admin != test_user['is_admin']

def test_user_model_delete_one(app,database):
    with app.app_context():
        addUser(test_user['email'],test_user['password'],test_user['is_admin'])
        deleteUser(test_user['email'])

        with pytest.raises(sqlalchemy.exc.NoResultFound):
            user = db.session.execute(db.select(User).filter_by(email=test_user['email'])).scalar_one()

def test_user_model_delete_all(app,database,capfd):
    with app.app_context():
        addUser(test_user['email'],test_user['password'],test_user['is_admin'])
        addUser("1" +test_user['email'],'1'+test_user['password'],True)
        deleteAllUsers()
        getAllUsers()
        out, err = capfd.readouterr()
    
    assert out is ''
    