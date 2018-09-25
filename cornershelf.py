from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from cornershelfdb_setup import Base, Cookbook, Recipes, User
from flask import session as login_session
import random
import string

app = Flask(__name__)

engine = create_engine('sqlite:///cornershelf.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# homepage, show all cookbooks, login, logout, createcookbook
@app.route('/')
@app.route('/cornershelf')
def homepage():
    return render_template('index.html')

# public cookbook view
@app.route('/cornershelf/<int:cookbook_id>')
def cookbookpublic(cookbook_id):
    if 'username' not in login_session or cookbook_user_id != user_id:
        return render_template('publicCookbook.html')
    else:
        return redirect(url_for('cookbook.html'))


# public recipe from cookbook view
@app.route('/cornershelf/<int:cookbook_id>/<int:recipes_id>')
def publicrecipes(cookbook_id, recipes_id):
    if 'username' not in login_session or cookbook_user_id != user_id:
        return render_template('publicRecipe.html')
    else:
        return redirect(url_for('recipe.html'))

# a users cookbook viewpage
@app.route('/conershelf/<int:user_id>/<int:cookbook_id>')
def personalCookbook(user_id, cookbook_id):
    return render_template('cookbook.html')

# add a recipe to a users cookbook
@app.route('/conershelf/<int:user_id>/<int:cookbook_id>/add')
def personalCookbookAdd(user_id, cookbook_id):
    return render_template('addRecipe.html')

# edit a recipe in a users cookbook
@app.route('/conershelf/<int:user_id>/<int:cookbook_id>/<int:recipes_id>/edit')
def personalCookbookEdit(user_id, cookbook_id, recipes_id):
    return render_template('editRecipe.html')

# delete a recipe from a users cookbook
@app.route('/conershelf/<int:user_id>/<int:cookbook_id>/<int:recipes_id>/delete')
def personalCookbookDelete(user_id, cookbook_id, recipes_id):
    return render_template('deleteRecipe.html')


# search for a recipe to add to your cookbook using the yummly API "fingers crossed"
@app.route('/cornershelf/search')
def search():
    return render_template('search.html')

# if user is new or does not have a cook book, will be able to create a cookbook
@app.route('/cornershelf/createcookbook')
def createCookbookNew():
    if username not in login_session:
        return redirect(url_for('login.html'))
    if user_id is not in Cookbook:
        return render_template()

# a login page for users to create login or use google+
@app.route('/cornershelf/login')
def login():
    if username not in login_session:
        return render_template('login.html')
    else:
        return redirect(url_for('index.html'))

# display a recipe from a users cookbook, will have the edit/delete options
@app.route('/conershelf/<int:user_id>/<int:cookbook_id>/<int:recipes_id>')
def personalRecipe(user_id, cookbook_id, recipes_id):
    return render_template('recipe.html')
# logout route for disconnect from personal session and google session
@app.route('/cornershelf/logout')




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
