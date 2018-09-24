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
    return 'here is the homepage'

# public cookbook view
@app.route('/cornershelf/<int:cookbook_id>')

# public recipe from cookbook view
@app.route('/cornershelf/<int:cookbook_id>/<int:recipes_id>')

# a users cookbook viewpage
@app.route('/conershel/<int:user_id>/<int:cookbook_id>')

# add a recipe to a users cookbook
@app.route('/conershel/<int:user_id>/<int:cookbook_id>/add')

# edit a recipe in a users cookbook
@app.route('/conershel/<int:user_id>/<int:cookbook_id>/edit')

# delete a recipe from a users cookbook
@app.route('/conershel/<int:user_id>/<int:cookbook_id>/delete')

# search for a recipe to add to your cookbook using the yummly API "fingers crossed"
@app.route('/cornershelf/search')

# if user is new or does not have a cook book, will be able to create a cookbook
@app.route('/cornershelf/createcookbook')

# a login page for users to create login or use google+
@app.route('/cornershelf/login')

# display a recipe from a users cookbook, will have the edit/delete options
@app.route('/conershel/<int:user_id>/<int:cookbook_id>/<int:recipes_id>')

# logout route for disconnect from personal session and google session
@app.route('/cornershelf/logout')




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
