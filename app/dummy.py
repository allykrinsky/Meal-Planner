import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

engine = create_engine('sqlite:///mealplanner.db?check_same_thread=False', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("ally","ally")
session.add(user)


# commit the record the database
session.commit()

session.commit()