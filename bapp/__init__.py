from urllib.parse import quote

import cloudinary
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flasgger import Swagger

app = Flask(__name__)
app.secret_key = 'jfroooewq920jvjdftd$#%^7cnnmm'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/sportbookingdb' % quote('admin123@')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['PAGE_SIZE']=5

swagger = Swagger(app, template_file='swagger.yml')

db = SQLAlchemy(app=app)
login_manager = LoginManager(app)

cloudinary.config(cloud_name='dyupzyqwj',
                  api_key='497522642724389',
                  api_secret='1qiLwjHVPTBX9_BYZKsRB2FfWJA')

