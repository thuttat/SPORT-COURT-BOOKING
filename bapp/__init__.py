import os
from urllib.parse import quote

import cloudinary
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flasgger import Swagger
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'jfroooewq920jvjdftd$#%^7cnnmm'

# <<<<<<< HEAD
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#     "SQLALCHEMY_DATABASE_URI",
#     'mysql+pymysql://root:%s@localhost/sportbookingdb' % quote('anhthu')
# )
# =======
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#     "DATABASE_URL",
#     'mysql+pymysql://root:%s@localhost/sportbookingdb' % quote('root')
#     )


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    'mysql+pymysql://root:%s@localhost/sportbookingdb' % quote('admin123@')
    )

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['PAGE_SIZE']=5 
app.config['MAX_CANCELLATIONS_PER_WEEK'] = 3

swagger = Swagger(app, template_file='swagger.yml')

db = SQLAlchemy(app=app)
login_manager = LoginManager(app)

cloudinary.config(cloud_name='dyupzyqwj',
                  api_key='497522642724389',
                  api_secret='1qiLwjHVPTBX9_BYZKsRB2FfWJA')


