"""Creates classes (tables) for each model in the database"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# initializing Flask app
app = Flask(__name__)

app.app_context().push()

# Change this accordingly
PASSWORD = ""
PUBLIC_IP_ADDRESS = "localhost:5432"
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

	channelID = db.Column(db.String, primary_key=True)
	channelName = db.Column(db.String, nullable=False)
	description = db.Column(db.Text, nullable=True)
	subscriberCount = db.Column(db.Integer, nullable=False)
	viewCount = db.Column(db.BigInteger, nullable=False)
	videoCount = db.Column(db.Integer, nullable=False)
	thumbnail = db.Column(db.Text, nullable=True)

	videos = db.relationship('Video', backref = 'channels')
	playlists = db.relationship('Playlist', backref = 'channels')

# Video table
# Many-to-Many with Playlist table
class Video(db.Model):
	__tablename__ = 'videos'

	videoID = db.Column(db.String, primary_key=True)
	title = db.Column(db.String, nullable=False)
	description = db.Column(db.Text, nullable=True)
	viewCount = db.Column(db.BigInteger, nullable=False)
	likeCount = db.Column(db.Integer, nullable=False)
	commentCount = db.Column(db.Integer, nullable=False)
	thumbnail = db.Column(db.Text, nullable=True)

	channelID = db.Column(db.String, db.ForeignKey('channels.channelID'))

# Playlist table
# Many-to-Many with Video table
class Playlist(db.Model):
	__tablename__ = 'playlists'

	playlistID = db.Column(db.String, primary_key=True)
	title = db.Column(db.String, nullable=False)
	description = db.Column(db.Text, nullable=True)
	publishedAt = db.Column(db.DateTime(timezone=False), nullable=False)
	videoCount = db.Column(db.Integer, nullable=False)
	thumbnail = db.Column(db.Text, nullable=True)

	channelID = db.Column(db.String, db.ForeignKey('channels.channelID'))

	videos = db.relationship('Video', secondary='VideoPlaylist', backref='inPlaylist')

# Video-Playlist association table
VideoPlaylist = db.Table('videoplaylist',
   db.Column('videoID', db.String, db.ForeignKey('videos.videoID')), 
   db.Column('playlistID', db.String, db.ForeignKey('playlists.playlistID'))
   )

db.create_all()
