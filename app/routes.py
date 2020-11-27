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


userID = None
@app.template_global()
def set_user(user):
    global userID
    userID = user


@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST' and request.form.get("login"):
        user = request.form['username']
        password = request.form['password']
        # if username doesnt exist
        if  db.session.execute("Select username From User Where username=:param", {'param':user}).first() == None:
            error = 'This username does not exist'
        # if user exitst
        else :
            # if password is incorrect
            if db.session.execute("Select password From User Where username=:param", {'param':user}).first() != password: 
                error = 'Invalid Credentials. Please try again.'
            # if password is correct
            else:
                set_user(db.session.execute("Select id From User Where username=:param", {'param':user}).first())
                return redirect('/mealplanner')
                
    
    return render_template('login.html', error=error)


@app.route('/mealplanner', methods=['GET', 'POST'])
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
            temp = db.session.execute("Select meal From myPlan Where mealID/10=:param and userID=:id", {'param':i, 'id':userID})
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
    
    if request.method == 'POST' and request.form.get('submit'):
        name = request.form['name']
        date = request.form['date']
        meal = request.form['meal']
        
        update(name, date, meal)


    return render_template('mealplanner.html', headings=headings, data=calcData())


@app.route('/mylists', methods=['GET', 'POST'])
def mylists():
    
    headings = (" ", "Items", "Quatity", "Store")
    headings2 = ("Items", "Quatity")
    data = db.session.query(myGroceryList.ingredient, myGroceryList.qty, myGroceryList.store).all() #add more rows
    data2 = db.session.query(myFridge.ingredient, myFridge.qty).all()

    #buttons
    if request.method == 'POST':

        if request.form.get('remove'):
            input = request.form['value']
            db.session.execute("Delete From myGrceryList Where name=:param", {'param':input})

        else :
            ingredient = request.form['item']
            qty = request.form['qty']
            if request.form.get("grocery"):
                store = request.form['store']
                me = myGroceryList(ingredient, qty, store)
                

            if request.form.get("fridge"):
                me = myFridge(ingredient, qty)
                
        
            db.session.add(me)
            
        
        db.session.commit()

        data = db.session.query(myGroceryList.ingredient, myGroceryList.qty, myGroceryList.store).all()
        data2 = db.session.query(myFridge.ingredient, myFridge.qty).all()
        return render_template('mylists.html', headings=headings, headings2=headings2, data=data, data2=data2)

    return render_template('mylists.html', headings=headings, headings2=headings2, data=data, data2=data2)

@app.route('/myrecipes', methods=['GET', 'POST'])
def myrecipes():

    headings = ("Recipe Name")
    data = db.session.query(myRecList.name).all()

    if request.method == 'POST':
        if request.form.get('add_recipe') == 'submit':
            return render_template('new_rec.html')

        input = request.form['name']
        id = db.session.execute("Select recipeID From myRecList Where name=:param", {'param':input})
        return recipe_results(id.fetchone()[0])
        
    return render_template('myrecipes.html', headings=headings, data=data)

@app.route('/recipe_results', methods=['GET','POST'])
def recipe_results(id):
    
    headings = ("Quantity", "Ingredient")
    data = db.session.execute("Select qty, ingredient From myRec Where recipeID=:param", {'param':id})
    
    return render_template('recipe_results.html', headings=headings, data=data)

@app.route('/new_rec', methods=['GET', 'POST'])
def new_rec():

    headings = ("Quantity", "Ingredient")

    name = request.form['recipe_name']
    url = request.form['url']
    qty = request.form['qty']
    item = request.form['item']

    if request.method == 'POST':
        if db.session.execute("Select recipeID From myRecList Where name=:param", {'param':name}).first() == None:
            db.session.add(myRecList(name, url))
            db.session.commit()
        
        recipeID = db.session.execute("Select recipeID From myRecList Where name=:param", {'param':name}).fetchone()[0]
        
        me = myRec(recipeID, item, qty)
        db.session.add(me)
        db.session.commit()
        data = db.session.execute("Select qty, ingredient From myRec Where recipeID=:param", {'param':recipeID})
        

        return render_template('new_rec.html', headings=headings, data=data)
    
    data = db.session.execute("Select * From myRec Where recipeID=:param", {'param': recipeID})
    
    return render_template('new_rec.html', headings=headings, data=data, name=name)


