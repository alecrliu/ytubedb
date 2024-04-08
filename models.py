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


class Channel(db.Model):
    """

    Channel table

    Primary Key: channel_id

    Relationships:
        One-to-Many with Video table
        One-to-Many with Playlist table

    Attributes:
        channelName: Name of the channel
        description: Desription of the channel
        publishedAt: Standard datetime when the channel was published
        subscriberCount: Number of subscribers of the channel
        viewCount: Sum of all the view counts of videos of the channel
        videoCount: Number of videos of the channel
        thumbnail: A high quality thumbnail URL of the channel

    """
    __tablename__ = 'channels'

    channel_id = db.Column(db.String, primary_key=True)
    channelName = db.Column(db.String, nullable=False)
    # publishedAt = db.Column(db.DateTime(timezone=False), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subscriberCount = db.Column(db.Integer, nullable=False)
    viewCount = db.Column(db.BigInteger, nullable=False)
    videoCount = db.Column(db.Integer, nullable=False)
    thumbnail = db.Column(db.Text, nullable=True)

    videos = db.relationship('Video', backref='channels')
    playlists = db.relationship('Playlist', backref='channels')

    # Returns dictionary of channel instance
    def to_dict(self):
        return {
            "channelID": self.channel_id,
            "channelName": self.channelName,
            "description": self.description,
            "subscriberCount": self.subscriberCount,
            "viewCount": self.viewCount,
            "videoCount": self.videoCount,
            "thumbnail": self.thumbnail
        }


# Video-Playlist association table
VideoPlaylist = db.Table('videoplaylist',
                         db.Column('video_id', db.String,
                                   db.ForeignKey('videos.video_id')),
                         db.Column('playlist_id', db.String,
                                   db.ForeignKey('playlists.playlist_id'))
                         )


class Video(db.Model):
    """

    Video table

    Primary Key: video_id
    Foreign Key: channel_id

    Relationships:
        Many-to-Many with Playlist table

    Attributes:
        title: Title of the video
        description: Description of the video
        publishedAt: Standard datetime when the video was published
        viewCount: Number of views the video has
        likeCount: Number of likes the video has
        commentCount: Number of comments the video has
        thumbnail: A high quality thumbnail URL of the video

    """
    __tablename__ = 'videos'

    video_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    # publishedAt = db.Column(db.DateTime(timezone=False), nullable=False)
    description = db.Column(db.Text, nullable=True)
    viewCount = db.Column(db.BigInteger, nullable=False)
    likeCount = db.Column(db.Integer, nullable=False)
    commentCount = db.Column(db.Integer, nullable=False)
    thumbnail = db.Column(db.Text, nullable=True)

    channel_id = db.Column(db.String, db.ForeignKey('channels.channel_id'))

    # Returns dictionary of video instance
    def to_dict(self):
        return {
            "videoID": self.video_id,
            "title": self.title,
            "description": self.description,
            "viewCount": self.viewCount,
            "likeCount": self.likeCount,
            "commentCount": self.commentCount,
            "thumbnail": self.thumbnail,
            "channelID": self.channel_id,
            "channelName": self.channels.channelName,
            "channelThumbnail": self.channels.thumbnail
        }


class Playlist(db.Model):
    """

    Playlist table

    Primary Key: playlist_id
    Foreign Key: channel_id

    Relationships:
        Many-to-Many with Video table

    Attributes:
        title: Title of the playlist
        description: Description of the playlist
        publishedAt: Standard datetime when the playlist was published
        videoCount: Number of videos the playlist has
        totalViews: Sum of views of all the videos in the playlist
        totalLikes: Sum of likes of all the videos in the playlist
        totalComments: Sum of comments of all the videos in the playlist
        thumbnail: A high quality thumbnail URL of the video

    """
    __tablename__ = 'playlists'

    playlist_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    publishedAt = db.Column(db.DateTime(timezone=False), nullable=False)
    videoCount = db.Column(db.Integer, nullable=False)
    totalViews = db.Column(db.BigInteger, nullable=False)
    totalLikes = db.Column(db.BigInteger, nullable=False)
    totalComments = db.Column(db.BigInteger, nullable=False)
    thumbnail = db.Column(db.Text, nullable=True)

    channel_id = db.Column(db.String, db.ForeignKey('channels.channel_id'))

    videos = db.relationship(
        'Video', secondary='videoplaylist', backref='inPlaylist')

    # Returns dictionary of playlist instance
    def to_dict(self):
        return {
            "playlistID": self.playlist_id,
            "title": self.title,
            "description": self.description,
            "publishedAt": self.publishedAt,
            "videoCount": self.videoCount,
            "totalViews": self.totalViews,
            "totalLikes": self.totalLikes,
            "totalComments": self.totalComments,
            "thumbnail": self.thumbnail,
            "channelID": self.channel_id,
            "channelName": self.channels.channelName,
            "channelThumbnail": self.channels.thumbnail
        }
