from app import db 
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, index=True) 
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class myPlan(db.Model):
    __tablename__ = 'myPlan'
    mealID = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    recipeID = db.Column(db.Integer, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    

    def __init__(self, mealID, meal, date, recipeID, userID):
        self.mealID = mealID
        self.meal = meal
        self.date = date
        self.recipeID = recipeID
        self.userID = userID

class myFridge(db.Model):
    __tablename__ = 'myFridge'
    ingredientID = db.Column(db.Integer, primary_key=True, nullable=False, unique=False)
    ingredient = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Text, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, ingredient, qty, userID):
        self.ingredient = ingredient
        self.qty = qty
        self.userID = userID

class myRecList(db.Model):
    __tablename__ = 'myRecList'
    recipeID = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, name, url, userID):
        self.name = name
        self.url = url
        self.userID = userID

class myRec(db.Model):
    __tablename__ = 'myRec'
    index = db.Column(db.Integer, primary_key=True, index=True)
    recipeID = db.Column(db.Integer, nullable=False)
    ingredient = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Text, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, recipeID,  ingredient, qty, userID):
            self.recipeID = recipeID
            self.ingredient = ingredient
            self.qty = qty
            self.userID = userID


class myGroceryList(db.Model):
    __tablename__ = 'myGroceryList'
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Text, nullable=False)
    store = db.Column(db.Text)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, ingredient, qty, store, userID):
            self.ingredient = ingredient
            self.qty = qty
            self.store = store
            self.userID = userID

db.create_all()