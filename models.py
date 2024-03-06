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


# uncomment playlistID lines after creating playlists table
class Video(db.Model):
    __tablename__ = 'videos'

    videoID = db.Column(db.String, primary_key=True)
    channelID = db.Column(db.String, db.ForeignKey('channels.channelID'))
    # playlistID = db.Column(db.String, db.ForeignKey('playlists.playlistID'))
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    views = db.Column(db.BigInteger, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    commentCount = db.Column(db.Integer, nullable=False)
    thumbnail = db.Column(db.Text, nullable=False)


class Channel(db.Model):
    __tablename__ = 'channels'

    channelID = db.Column(db.String, primary_key=True)
    videoID = db.Column(db.String, db.ForeignKey('videos.videoID'))
    # playlistID = db.Column(db.String, db.ForeignKey('playlists.playlistID'))
    channelName = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    subscriberCount = db.Column(db.BigInteger, nullable=True)
    videoCount = db.Column(db.Integer, nullable=True)
    thumbnail = db.Column(db.Text, nullable=True)


db.create_all()
