"""Creates classes (tables) for each model in the database"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()

# initializing Flask app
app = Flask(__name__)

app.app_context().push()

# Change this accordingly
PASSWORD = os.getenv("DB_PASSWORD")
PUBLIC_IP_ADDRESS = "localhost:5432"  # use for local database
DBNAME = "ytubedb"

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DB_STRING", f'postgresql://postgres:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}'
)
# To suppress a warning message
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Channel table
# One-to-Many with Video table
# One-to-Many with Playlist table
class Channel(db.Model):
    __tablename__ = 'channels'

    channel_id = db.Column(db.String, primary_key=True)
    channelName = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    subscriberCount = db.Column(db.Integer, nullable=False)
    viewCount = db.Column(db.BigInteger, nullable=False)
    videoCount = db.Column(db.Integer, nullable=False)
    thumbnail = db.Column(db.Text, nullable=True)

    videos = db.relationship('Video', backref='channels')
    playlists = db.relationship('Playlist', backref='channels')


# Video-Playlist association table
VideoPlaylist = db.Table('videoplaylist',
                         db.Column('video_id', db.String,
                                   db.ForeignKey('videos.video_id')),
                         db.Column('playlist_id', db.String,
                                   db.ForeignKey('playlists.playlist_id'))
                         )

# Video table
# Many-to-Many with Playlist table
class Video(db.Model):
    __tablename__ = 'videos'

    video_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    viewCount = db.Column(db.BigInteger, nullable=False)
    likeCount = db.Column(db.Integer, nullable=False)
    commentCount = db.Column(db.Integer, nullable=False)
    thumbnail = db.Column(db.Text, nullable=True)

    channel_id = db.Column(db.String, db.ForeignKey('channels.channel_id'))

# Playlist table
# Many-to-Many with Video table
class Playlist(db.Model):
    __tablename__ = 'playlists'

    playlist_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    publishedAt = db.Column(db.DateTime(timezone=False), nullable=False)
    videoCount = db.Column(db.Integer, nullable=False)
    thumbnail = db.Column(db.Text, nullable=True)

    channel_id = db.Column(db.String, db.ForeignKey('channels.channel_id'))

    videos = db.relationship(
        'Video', secondary='videoplaylist', backref='inPlaylist')
