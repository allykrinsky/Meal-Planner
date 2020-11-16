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
    ingredientID = db.Column(db.Integer, primary_key=True, nullable=False)
    ingredient = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Text, nullable=False)

    def __init__(self, ingredientID, ingredient, qty):
        self.ingredientID = ingredientID
        self.ingredient = ingredient
        self.qty = qty

class myRecipes(db.Model):
    __tablename__ = 'myRecipes'
    recipeID = db.Column(db.Integer, primary_key=True, index=True)
    recipe = db.Column(db.Text, nullable=False)
    ingredient = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Text, nullable=False)

    def __init__(self, recipeID, recipe, ingredient, qty):
            self.recipeID = recipeID
            self.recipe = recipe
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


    

     
