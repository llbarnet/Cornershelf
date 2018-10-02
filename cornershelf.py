from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, abort, g, session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, relationship
from cornershelfdb_setup import Base, Cookbook, Recipes, User
from flask import session as login_session
import json
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Cornershelf"

engine = create_engine('sqlite:///cornershelf.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# login page with gplus
@app.route('/cornershelf/login')
def login():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    request.get_data()
    code = request.data.decode('utf-8')

    try:

        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check for valid token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit the request, parse response
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# to logout of a user session 
@app.route('/logout')
def gdisconnect():
    # disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # delete  user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response




# homepage, show all cookbooks, login, logout, createcookbook
@app.route('/')
@app.route('/cornershelf/')
def homepage():
    cookbooks = session.query(Cookbook).all()
    return render_template('index.html', cookbooks=cookbooks)

# public cookbook view
@app.route('/cornershelf/<int:cookbook_id>')
def cookbookpublic(cookbook_id):
    cookbook=session.query(Cookbook).filter_by(id=cookbook_id).one()
    recipes=session.query(Recipes).filter_by(cookbookID=cookbook_id).all()
    return render_template('publicCookbook.html', cookbook=cookbook, recipes=recipes)


# public recipe from cookbook view
@app.route('/cornershelf/<int:cookbook_id>/<int:recipes_id>')
def publicrecipes(cookbook_id, recipes_id):
    cookbook=session.query(Cookbook).filter_by(id=cookbook_id).one()
    recipes=session.query(Recipes).filter_by(cookbookID=Cookbook_id).filter_by(id=recipes_id).one()
    return render_template('publicRecipe.html', cookbook=cookbook, recipes=recipes)

# if user is new or does not have a cook book, will be able to create a cookbook
@app.route('/cornershelf/createcookbook', methods=['GET', 'POST'])
def createCookbookNew():
    if 'username' not in login_session:
        return redirect('cornershelf/login')
    if request.method == 'POST':
        createCookbook = Cookbook(
            name=request.form['name'], userID=login_session['user_id'])
        session.add(createCookbook)
        flash('%s was whipped up!' % createCookbook.name)
        session.commit()
        return redirect(url_for('personalCookbook', cookbook_id=createCookbook.id))
    else:
        return render_template('createCookbook.html')

# a users cookbook viewpage
@app.route('/cornershelf/u/<int:cookbook_id>')
def personalCookbook(cookbook_id):
    cookbook=session.query(Cookbook).filter_by(id=cookbook_id).one()
    recipes=session.query(Recipes).filter_by(cookbookID=cookbook_id).all()
    if cookbook.userID == login_session['user_id']:
        return render_template('cookbook.html', cookbook=cookbook, recipes=recipes)
    else:
        return redirect(url_for('cookbookpublic', cookbook_id=cookbook_id))

# display a recipe from a users cookbook, will have the edit/delete options
@app.route('/cornershelf/u/<int:cookbook_id>/<int:recipes_id>')
def personalRecipe(cookbook_id, recipes_id):
    cookbook=session.query(Cookbook).filter_by(id=cookbook_id).one()
    recipes=session.query(Recipes).filter_by(cookbookID=cookbook_id).filter_by(id=recipes_id).one()
    if cookbook.userID == login_session['user_id']:
        return render_template('recipe.html', cookbook=cookbook, recipes=recipes)
    else:
        return redirect(url_for('publicrecipes', cookbook_id=cookbook_id, recipes_id=recipes_id))

# add a recipe to a users cookbook
@app.route('/cornershelf/u/<int:cookbook_id>/add', methods=['GET', 'POST'])
def personalCookbookAdd(cookbook_id):
    cookbook=session.query(Cookbook).filter_by(id=cookbook_id).one()
    if cookbook.userID != login_session['user_id']:
        return redirect(url_for('publicCookbook', cookbook_id=cookbook_id))
    if request.method == 'POST':
        newRecipe = Recipes(name=request.form['name'], ingredients=request.form['ingredients'], directions=request.form['directions'], type=request.form['type'], cookbookID=cookbook_id)
        session.add(newRecipe)
        session.commit()
        return redirect(url_for('personalCookbook', cookbook_id=cookbook_id))
    else:
        return render_template('addRecipe.html', cookbook_id=cookbook_id, cookbook=cookbook)
    return render_template('addRecipe.html', cookbook=cookbook)


# edit a recipe in a users cookbook
@app.route('/cornershelf/u/<int:cookbook_id>/<int:recipes_id>/edit', methods=['GET', 'POST'])
def personalCookbookEdit(cookbook_id, recipes_id):
    cookbook=session.query(Cookbook).filter_by(id=cookbook_id).one()
    editedRecipe = session.query(Recipes).filter_by(id=recipes_id).one()
    if cookbook.userID != login_session['user_id']:
        return redirect(url_for('publicrecipes', cookbook_id=cookbook_id, recipes_id=recipes_id))
    if request.method == 'POST':
        if request.form['name']:
            editedRecipe.name=request.form['name']
        if request.form['ingredients']:
            editedRecipe.ingredients=request.form['ingredients']
        if request.form['directions']:
            editedRecipe.directions=request.form['directions']
        if request.form['type']:
            editedRecipe.type=request.form['type']
        session.add(editedRecipe)
        session.commit()
        return redirect(url_for('personalRecipe', cookbook_id=cookbook_id, recipes_id=recipes_id))
    else:
        return render_template('editRecipe.html', cookbook=cookbook, recipes=editedRecipe)
    return render_template('editRecipe.html', cookbook=cookbook)

# delete a recipe from a users cookbook

@app.route('/cornershelf/u/<int:cookbook_id>/<int:recipes_id>/delete', methods=['GET', 'POST'])
def personalCookbookDelete(cookbook_id, recipes_id):
    cookbook=session.query(Cookbook).filter_by(id=cookbook_id).one()
    deleterecipe = session.query(Recipes).filter_by(id=recipes_id).one()
    if cookbook.userID != login_session['user_id']:
        return redirect(url_for('publicrecipes', cookbook_id=cookbook_id, recipes_id=recipes_id))
    if request.method == 'POST':
        session.delete(deleterecipe)
        session.commit()
        return redirect(url_for('personalCookbook', cookbook_id=cookbook_id))
    else:
        return render_template('deleteRecipe.html', cookbook=cookbook, recipes=deleterecipe)
    return render_template('deleteRecipe.html', cookbook=cookbook, recipes=deleterecipe)


# search for a recipe to add to your cookbook using the yummly API "fingers crossed"
@app.route('/cornershelf/search')
def search():
    return render_template('searchRecipe.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
