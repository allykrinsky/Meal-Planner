from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__, static_url_path='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mealplan.db'
db = SQLAlchemy(app)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000)

from mealplanner import routes