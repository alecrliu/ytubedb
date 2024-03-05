"""Creates classes (tables) for each model in the database"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


# initializing Flask app
app = Flask(__name__)

app.app_context().push()

# Change this accordingly
USER = "postgres"
PASSWORD = ""
PUBLIC_IP_ADDRESS = "localhost:5432"
DBNAME = "ytubedb"

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = \
    os.environ.get(
        "DB_STRING", f'postgresql://{USER}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}')
# To suppress a warning message
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# class Channel(db.Model):
# 	__tablename__ = 'channels'

# 	title = db.Column(db.String(80), nullable = False)
# 	id = db.Column(db.Integer, primary_key = True)

# db.create_all()
