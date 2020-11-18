from flask import Flask, render_template, request, redirect, url_for, g, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
from app.models import myPlan
from app.models import myFridge
from app.models import myRec
from app.models import myRecList
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
    def formatQuery(temp):
        row = []
        for el in temp:
            row.append(str(el).strip("',()"))
        return row

    def getID(date, meal):
        dates = {'Monday':'1', 'Tuesday':'2', 'Wednesday':'3', 'Thursday':'4', 'Friday':'5', 'Saturday':'6', 'Sunday':'7'}
        meals = {'Breakfast':'1', 'Lunch':'2', 'Dinner':'3'}
        return int(meals.get(meal) + dates.get(date))

    def calcData():
        data = []
        for i in [1,  2, 3]:
            temp = db.session.execute("Select meal From myPlan Where mealID/10=:param", {'param':i})
            row = formatQuery(temp)
            data.append(row)    

        return data

    def update(name, date, time):
        mealID = getID(date, time)
        meal = name
        date = date 
        recipeID = 1 #UPDATE if recipe in db then add recipeID else create new
        db.session.query(myPlan).filter(myPlan.mealID == mealID).update({'meal':meal, 'recipeID':recipeID})

        db.session.commit()

    headings = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        meal = request.form['meal']
        
        update(name, date, meal)


    return render_template('mealplanner.html', headings=headings, data=calcData())


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

    headings = ("Recipe Name")
    data = db.session.query(myRecList.name).all()

    if request.method == 'POST':
        #input = request.form.get('name')
        #sys.stdout.write(str(input))
        input = 'White Chocolate Cranberry Cookies (Gluten Free)  '
        id = db.session.execute("Select recipeID From myRecList Where name=:param", {'param':input})
        
        return recipe_results(id.fetchone()[0])
        
    return render_template('myrecipes.html', headings=headings, data=data)

@app.route('/recipe_results', methods=['GET','POST'])
def recipe_results(id):
    
    headings = ("Quantity", "Ingredient")
    data = db.session.execute("Select qty, ingredient From myRec Where recipeID=:param", {'param':id})
    
    return render_template('recipe_results.html', headings=headings, data=data)


