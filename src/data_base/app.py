# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/models/

"""Create Database"""
# https://wiki.postgresql.org/wiki/Psycopg2_Tutorial
# Go to src/database directory
# On the terminal, run:
# 1. export FLASK_APP=app.py 
# 2. flask shell
# 3. from app import db # This will load app.py
# 4. db.create_all() 

import os
#import psycopg2
from contextlib import closing
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

db_url = os.getenv('DATABASE_URL')


# Instatiate Flask app
app = Flask(
    __name__,
    static_folder='static',  # contains images & css
    static_url_path='',
    template_folder='template',)  # contains html files

# Connection to database
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

# Instantiate SQLAlchemy object
db = SQLAlchemy(app)
#db.init_app(app)  # alternative to instantiating SQLAlchemy object if using multiple files

#@app.route('/')
#def index():
#    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)