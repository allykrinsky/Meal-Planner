from flask import Flask, render_template, request, redirect, url_for, g, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
from app.models import myPlan
#from app.models import myFridge
#from app.models import myRecipes
#from app.models import myGroceryList
import pandas as pd 
import sys
import csv
import numpy as np 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

Session = sessionmaker(bind=myPlan)
session = Session()

@app.route('/')
def myplan():
    
    headings = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    data = session.query('Select meal From myPlan')
    #insert
    if request.method == 'POST':
        mealID = 1
        meal = request.form['mealname'].data
        date = '11/15'
        recipeID = 1
        me = models.myPlan(mealID=mealID, meal=meal, date=date, recipeID=recipeID)
        db.session.add(me)
        db.session.commit()
        

       #return render_template('mealplanner.html', headings=headings, data=data)


    
    ## show all
    #for i in range(21):
    #    data.append(myPlan.query.with_entities(myPlan.mealID == i))
    
    
    #data = (
    #    ('Breakfast', 'Breakfast', 'Breakfast', 'Breakfast', 'Breakfast', 'Breakfast', 'Breakfast'),
    #    ('Lunch','Lunch', 'Lunch', 'Lunch', 'Lunch', 'Lunch', 'Lunch'),
    #    ('Dinner', 'Dinner', 'Dinner', 'Dinner', 'Dinner', 'Dinner', 'Dinner')
    #)
    return render_template('mealplanner.html', headings=headings)


@app.route('/mylists')
def mylists():
    return render_template('mylists.html')

@app.route('/myrecipes')
def myrecipes():
    return render_template('myrecipes.html')


