from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mealplanner.db'
db = SQLAlchemy(app)
engine = create_engine('sqlite:///mealplanner.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()

from app import routes