from flask import Flask, render_template, request, redirect, url_for, g, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
from app.models import myPlan
from app.models import myFridge
from app.models import myRecipes
from app.models import myGroceryList
import pandas as pd 
import sys
import csv
import numpy as np 
from sqlalchemy import create_engine
from app import session
from app import db 

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def myplan():
    headings = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    data = (
        ('Breakfast', 'Breakfast', 'Breakfast', 'Breakfast', 'Breakfast', 'Breakfast', 'Breakfast'),
        ('Lunch','Lunch', 'Lunch', 'Lunch', 'Lunch', 'Lunch', 'Lunch'),
        ('Dinner', 'Dinner', 'Dinner', 'Dinner', 'Dinner', 'Dinner', 'Dinner')
    )
    
    #insert
    if request.method == 'POST':
        mealID = 3
        meal = request.form['mealname']
        sys.stdout.write(meal)
        date = '11/15'
        recipeID = 1
        me = myPlan(mealID, meal, date, recipeID)
        db.session.add(me)
        db.session.commit()
    
    return render_template('mealplanner.html', headings=headings, data=data)


@app.route('/mylists', methods=['GET', 'POST'])
def mylists():
    
    headings = ("Items", "Quatity", "Store")
    data = db.session.query(myGroceryList.ingredient, myGroceryList.qty, myGroceryList.store).all() #add more rows

    #insert
    if request.method == 'POST':
        ingredient = request.form['item']
        qty = request.form['qty']
        store = request.form['store']
        me = myGroceryList(ingredient, qty, store)
        db.session.add(me)
        db.session.commit()

        data = db.session.query(myGroceryList.ingredient, myGroceryList.qty, myGroceryList.store).all()
        return render_template('mylists.html', headings=headings, data=data)

    return render_template('mylists.html', headings=headings, data=data)

@app.route('/myrecipes', methods=['GET', 'POST'])
def myrecipes():
    return render_template('myrecipes.html')


