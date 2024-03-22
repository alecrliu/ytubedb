"""Database unit testing for website"""


import os
import sys
import unittest
from models import db, Channel, Playlist, Video

class DBTestCases(unittest.TestCase):
    def test1_playlist(self):
        playlist_data = {
            "playlist_id": "A1",
            "title": "ABC",
            "description": "ABC",
            "publishedAt": "2023-12-11T15:57:10Z",
            "videoCount": 0,
            "thumbnail": "THUMBNAIL",
            "channel_id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
        }
        s = Playlist(**playlist_data)
        db.session.add(s)
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
        db.session.commit()
    
    def test2_playlist(self):
        playlist_data1 = {
            "playlist_id": "A1",
            "title": "ABC",
            "description": "ABC",
            "publishedAt": "2023-12-11T15:57:10Z",
            "videoCount": 0,
            "thumbnail": "THUMBNAIL",
            "channel_id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
        }
        playlist_data2 = {
            "playlist_id": "A2",
            "title": "ABC",
            "description": "ABC",
            "publishedAt": "2023-12-11T15:57:10Z",
            "videoCount": 0,
            "thumbnail": "THUMBNAIL",
            "channel_id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
        }
        s1 = Playlist(**playlist_data1)
        s2 = Playlist(**playlist_data2)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()
        r = db.session.query(Playlist).filter_by(thumbnail="THUMBNAIL").all()
        self.assertEqual(len(r), 2)
        db.session.query(Playlist).filter_by(thumbnail="THUMBNAIL").delete()
        db.session.commit()
    
    def test3_playlist(self):
        playlist_data = {
            "playlist_id": "A1",
            "title": "ABC",
            "description": "ABC",
            "publishedAt": "2023-12-11T15:57:10Z",
            "videoCount": 0,
            "thumbnail": "THUMBNAIL",
            "channel_id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
        }
        s = Playlist(**playlist_data)
        before_count = db.session.query(Playlist).count()
        db.session.add(s)
        db.session.commit()
        after_count = db.session.query(Playlist).count()
        self.assertEqual(after_count, before_count + 1)
        db.session.query(Playlist).filter_by(playlist_id=playlist_data["playlist_id"]).delete()
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
