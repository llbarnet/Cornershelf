from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User
from flask import session as login_session
import random
import string

app = Flask(__name__)

engine = create_engine('sqlite:///cornershelf.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#homepage, show all cookbooks, login, logout, createcookbook
@app.route('/')
@app.route('/cornershelf')
    print ('here is the homepage')












if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
