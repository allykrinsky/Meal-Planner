from mealplanner import db #this might be a problem not sure yet

class MyPlan(db.Model):
    __tablename__ = 'myPlan'
    mealID = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.Text, nullable=False)
    date = db.Colum(db.DateTime, nullable=False)
    recipeID = db.Column(db.Integer, nullable=False)
    #ingredients = db.Colum(db.Text) --> create new recipe 

    def __init__(self, mealID, meal, date, recipeID, ingredients):
        self.mealID = mealID
        self.meal = meal
        self.date = date
        self.recipeID = recipeID
        self.ingredients = ingredients

class myFridge(db.Model):
    __tablename__ = 'myFridge'
    ingredientID = db.Colum(db,Integer, nullable=False)
    ingredient = db.Colum(db.Text, nullable=False)
    qty = db.Colum(db.Text, nullable)

    def __init__(self, ingredientID, ingredient, qty):
        self.ingredientID = ingredientID
        self.ingredient = ingredient
        self.qty = qty

class recipes(db.Model):
    __tablename__ = 'recipes'
    recipeID = db.Colum(db.Integer, primary_key=True, index=True)
    recipe = db.Colum(db.Text, nullable=False)
    ingredient = db.Colum(db.Text, nullable=False)
    qty = db.Colum(db.Text, nullable=False)

    def __init__(self, recipeID, recipe ingredient, qty):
            self.recipeID = recipeID
            self.recipe = recipe
            self.ingredient = ingredient
            self.qty = qty

class myGroceryList(db.Model):
    __tablename__ = 'myGroceryList'
    ingredient = db.Colum(db.Text, nullable=False)
    qty = db.Colum(db.Text, nullable=False)
    store = db.Colum(db.Text)

    def __init__(self, ingredient, qty, store):
            self.ingredient = ingredient
            self.qty = qty
            self.store = store


    

     
