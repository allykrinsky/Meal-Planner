from flask import Flask, render_template, request, redirect, url_for, g, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
##import models
import pandas as pd 
import sys
import csv
import numpy as np 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mealplan.db'
#db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('mealplanner.html')

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000, debug=True)

#import routes