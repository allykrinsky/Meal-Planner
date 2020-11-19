from app import db 

class myPlan(db.Model):
    __tablename__ = 'myPlan'
    mealID = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    recipeID = db.Column(db.Integer, nullable=False)
    

    def __init__(self, mealID, meal, date, recipeID):
        self.mealID = mealID
        self.meal = meal
        self.date = date
        self.recipeID = recipeID

class myFridge(db.Model):
    __tablename__ = 'myFridge'
    ingredientID = db.Column(db.Integer, primary_key=True, nullable=False, unique=False)
    ingredient = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Text, nullable=False)

    def __init__(self, ingredient, qty):
        self.ingredient = ingredient
        self.qty = qty

class myRecList(db.Model):
    __tablename__ = 'myRecList'
    recipeID = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)

    def __init__(self, recipeID, name, url):
        self.recipeID = recipeID
        self.name = name
        self.url = url

class myRec(db.Model):
    __tablename__ = 'myRec'
    index = db.Column(db.Integer, primary_key=True, index=True)
    recipeID = db.Column(db.Integer, nullable=False)
    ingredient = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Text, nullable=False)

    def __init__(self, recipeID,  ingredient, qty):
            self.recipeID = recipeID
            self.ingredient = ingredient
            self.qty = qty


class myGroceryList(db.Model):
    __tablename__ = 'myGroceryList'
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Text, nullable=False)
    store = db.Column(db.Text)

    def __init__(self, ingredient, qty, store):
            self.ingredient = ingredient
            self.qty = qty
            self.store = store


    

     
