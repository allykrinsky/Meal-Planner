from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from app import app
from app.models import myPlan
from app.models import myFridge
from app.models import myRec
from app.models import myRecList
from app.models import myGroceryList
from app.models import User
import pandas as pd 
import sys
import csv
import numpy as np 
from sqlalchemy import create_engine
from app import db


@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST' and request.form.get('login'):
        user = request.form['username']
        password_attempt = request.form['password']
        #if username exists
        username = db.session.query(User.username).filter_by(username=user).first()
        if bool(username) :
            password = db.session.query(User.password).filter_by(username=user).one()
            if str(password[0]) == password_attempt:
                userID= db.session.execute("Select id From User Where username=:user", {'user':user}).fetchone()[0]
                session['userID'] = userID

                return redirect(url_for('myplan'))   
            else :
                error = "Password Incorrect. Please try again."
        else :
            error = "Username does not exist. Please Sign up."

    if request.method == 'POST' and request.form.get('signup'):   

        return redirect(url_for('sign_up'))  
       
    
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password'] 
        db.session.add(User(user, password))
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html')


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
            temp = db.session.execute("Select meal From myPlan Where mealID/10=:param and userID=:id", {'param':i, 'id':session['userID']})
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
                me = myGroceryList(ingredient, qty, store, session['userID'])
                

            if request.form.get("fridge"):
                me = myFridge(ingredient, qty, session['userID'])
                
        
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
            db.session.add(myRecList(name, url, session['userID']))
            db.session.commit()
        
        recipeID = db.session.execute("Select recipeID From myRecList Where name=:param", {'param':name}).fetchone()[0]
        
        me = myRec(recipeID, item, qty, session['userID'])
        db.session.add(me)
        db.session.commit()
        data = db.session.execute("Select qty, ingredient From myRec Where recipeID=:param", {'param':recipeID})
        

        return render_template('new_rec.html', headings=headings, data=data)
    
    data = db.session.execute("Select * From myRec Where recipeID=:param", {'param': recipeID})
    
    return render_template('new_rec.html', headings=headings, data=data, name=name)
