"""Database unit testing for website"""


import os
import sys
import unittest
from models import db, Channel, Playlist, Video

CHANNEL_DATA = {
    "channel_id": "ChABC",
    "channelName": "ABC",
    "description": "ABC",
    "subscriberCount": 0,
    "viewCount": 0,
    "videoCount": 0,
    "thumbnail": "ABC",
}

class DBTestCases(unittest.TestCase):
    def test1_channel(self):
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        db.session.commit()
        r = db.session.query(Channel).filter_by(channel_id=CHANNEL_DATA["channel_id"]).one()
        self.assertEqual(r.channel_id, CHANNEL_DATA["channel_id"])
        self.assertEqual(r.channelName, CHANNEL_DATA["channelName"])
        self.assertEqual(r.description, CHANNEL_DATA["description"])
        self.assertEqual(r.subscriberCount, CHANNEL_DATA["subscriberCount"])
        self.assertEqual(r.viewCount, CHANNEL_DATA["viewCount"])
        self.assertEqual(r.videoCount, CHANNEL_DATA["videoCount"])
        self.assertEqual(r.thumbnail, CHANNEL_DATA["thumbnail"])
        db.session.query(Channel).filter_by(channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()
    
    def test2_channel(self):
        c2_data = CHANNEL_DATA.copy()
        c2_data["channel_id"] = "ChZYX"
        c1 = Channel(**CHANNEL_DATA)
        c2 = Channel(**c2_data)
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        r = db.session.query(Channel).filter_by(thumbnail="ABC").all()
        self.assertEqual(len(r), 2)
        db.session.query(Channel).filter_by(thumbnail="ABC").delete()
        db.session.commit()
    
    def test3_channel(self):
        c = Channel(**CHANNEL_DATA)
        before_count = db.session.query(Channel).count()
        db.session.add(c)
        db.session.commit()
        after_count = db.session.query(Channel).count()
        self.assertEqual(after_count, before_count + 1)
        db.session.query(Channel).filter_by(channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()

    def test1_playlist(self):
        playlist_data = {
            "playlist_id": "A1",
            "title": "ABC",
            "description": "ABC",
            "publishedAt": "2023-12-11T15:57:10Z",
            "videoCount": 0,
            "thumbnail": "THUMBNAIL",
            "channel_id": CHANNEL_DATA["channel_id"]
        }
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        test_playlist = Playlist(**playlist_data)
        db.session.add(test_playlist)
        db.session.commit()
        r = db.session.query(Playlist).filter_by(playlist_id=playlist_data["playlist_id"]).one()
        self.assertEqual(r.playlist_id, playlist_data["playlist_id"])
        self.assertEqual(r.title, playlist_data["title"])
        self.assertEqual(r.description, playlist_data["description"])
        # self.assertEqual(r.publishedAt, playlist_data["publishedAt"])
        self.assertEqual(r.videoCount, playlist_data["videoCount"])
        self.assertEqual(r.thumbnail, playlist_data["thumbnail"])
        self.assertEqual(r.channel_id, playlist_data["channel_id"])
        db.session.query(Playlist).filter_by(playlist_id=playlist_data["playlist_id"]).delete()
        db.session.query(Channel).filter_by(channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()
    
    def test2_playlist(self):
        playlist_data1 = {
            "playlist_id": "A1",
            "title": "ABC",
            "description": "ABC",
            "publishedAt": "2023-12-11T15:57:10Z",
            "videoCount": 0,
            "thumbnail": "THUMBNAIL",
            "channel_id": CHANNEL_DATA["channel_id"]
        }
        playlist_data2 = {
            "playlist_id": "A2",
            "title": "ABC",
            "description": "ABC",
            "publishedAt": "2023-12-11T15:57:10Z",
            "videoCount": 0,
            "thumbnail": "THUMBNAIL",
            "channel_id": CHANNEL_DATA["channel_id"]
        }
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        test_playlist1 = Playlist(**playlist_data1)
        test_playlist2 = Playlist(**playlist_data2)
        db.session.add(test_playlist1)
        db.session.add(test_playlist2)
        db.session.commit()
        r = db.session.query(Playlist).filter_by(thumbnail="THUMBNAIL").all()
        self.assertEqual(len(r), 2)
        db.session.query(Playlist).filter_by(thumbnail="THUMBNAIL").delete()
        db.session.query(Channel).filter_by(channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()
    
    def test3_playlist(self):
        playlist_data = {
            "playlist_id": "A1",
            "title": "ABC",
            "description": "ABC",
            "publishedAt": "2023-12-11T15:57:10Z",
            "videoCount": 0,
            "thumbnail": "THUMBNAIL",
            "channel_id": CHANNEL_DATA["channel_id"]
        }
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        test_playlist = Playlist(**playlist_data)
        before_count = db.session.query(Playlist).count()
        db.session.add(test_playlist)
        db.session.commit()
        after_count = db.session.query(Playlist).count()
        self.assertEqual(after_count, before_count + 1)
        db.session.query(Playlist).filter_by(playlist_id=playlist_data["playlist_id"]).delete()
        db.session.query(Channel).filter_by(channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
