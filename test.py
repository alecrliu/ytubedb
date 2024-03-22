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

VIDEO_DATA = {
    "video_id": "A1",
    "title": "ABC",
    "description": "ABC",
    "viewCount": 0,
    "likeCount": 0,
    "commentCount": 0,
    "thumbnail": "THUMBNAIL",
    "channel_id": CHANNEL_DATA["channel_id"]
}

PLAYLIST_DATA = {
    "playlist_id": "A1",
    "title": "ABC",
    "description": "ABC",
    "publishedAt": "2023-12-11T15:57:10Z",
    "videoCount": 0,
    "thumbnail": "THUMBNAIL",
    "channel_id": CHANNEL_DATA["channel_id"]
}


class DBTestCases(unittest.TestCase):
    def test1_channel(self):
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        db.session.commit()
        r = db.session.query(Channel).filter_by(
            channel_id=CHANNEL_DATA["channel_id"]).one()
        self.assertEqual(r.channel_id, CHANNEL_DATA["channel_id"])
        self.assertEqual(r.channelName, CHANNEL_DATA["channelName"])
        self.assertEqual(r.description, CHANNEL_DATA["description"])
        self.assertEqual(r.subscriberCount, CHANNEL_DATA["subscriberCount"])
        self.assertEqual(r.viewCount, CHANNEL_DATA["viewCount"])
        self.assertEqual(r.videoCount, CHANNEL_DATA["videoCount"])
        self.assertEqual(r.thumbnail, CHANNEL_DATA["thumbnail"])
        db.session.query(Channel).filter_by(
            channel_id=CHANNEL_DATA["channel_id"]).delete()
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
        db.session.query(Channel).filter_by(
            channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()

    def test1_video(self):
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        test_video = Video(**VIDEO_DATA)
        db.session.add(test_video)
        db.session.commit()
        r = db.session.query(Video).filter_by(
            video_id=VIDEO_DATA["video_id"]).one()
        self.assertEqual(r.video_id, VIDEO_DATA["video_id"])
        self.assertEqual(r.title, VIDEO_DATA["title"])
        self.assertEqual(r.description, VIDEO_DATA["description"])
        self.assertEqual(r.viewCount, VIDEO_DATA["viewCount"])
        self.assertEqual(r.likeCount, VIDEO_DATA["likeCount"])
        self.assertEqual(r.commentCount, VIDEO_DATA["commentCount"])
        self.assertEqual(r.thumbnail, VIDEO_DATA["thumbnail"])
        self.assertEqual(r.channel_id, VIDEO_DATA["channel_id"])
        db.session.query(Video).filter_by(
            video_id=VIDEO_DATA["video_id"]).delete()
        db.session.query(Channel).filter_by(
            channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()

    def test2_video(self):
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        v2_data = VIDEO_DATA.copy()
        v2_data["video_id"] = "A2"
        test_video1 = Video(**VIDEO_DATA)
        test_video2 = Video(**v2_data)
        db.session.add(test_video1)
        db.session.add(test_video2)
        db.session.commit()
        r = db.session.query(Video).filter_by(thumbnail="THUMBNAIL").all()
        self.assertEqual(len(r), 2)
        db.session.query(Video).filter_by(thumbnail="THUMBNAIL").delete()
        db.session.query(Channel).filter_by(
            channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()

    def test3_video(self):
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        test_video = Video(**VIDEO_DATA)
        before_count = db.session.query(Video).count()
        db.session.add(test_video)
        db.session.commit()
        after_count = db.session.query(Video).count()
        self.assertEqual(after_count, before_count + 1)
        db.session.query(Video).filter_by(
            video_id=VIDEO_DATA["video_id"]).delete()
        db.session.query(Channel).filter_by(
            channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()

    def test1_playlist(self):
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        test_playlist = Playlist(**PLAYLIST_DATA)
        db.session.add(test_playlist)
        db.session.commit()
        r = db.session.query(Playlist).filter_by(
            playlist_id=PLAYLIST_DATA["playlist_id"]).one()
        self.assertEqual(r.playlist_id, PLAYLIST_DATA["playlist_id"])
        self.assertEqual(r.title, PLAYLIST_DATA["title"])
        self.assertEqual(r.description, PLAYLIST_DATA["description"])
        # self.assertEqual(r.publishedAt, PLAYLIST_DATA["publishedAt"])
        self.assertEqual(r.videoCount, PLAYLIST_DATA["videoCount"])
        self.assertEqual(r.thumbnail, PLAYLIST_DATA["thumbnail"])
        self.assertEqual(r.channel_id, PLAYLIST_DATA["channel_id"])
        db.session.query(Playlist).filter_by(
            playlist_id=PLAYLIST_DATA["playlist_id"]).delete()
        db.session.query(Channel).filter_by(
            channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()

    def test2_playlist(self):
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        p2_data = PLAYLIST_DATA.copy()
        p2_data["playlist_id"] = "A2"
        test_playlist1 = Playlist(**PLAYLIST_DATA)
        test_playlist2 = Playlist(**p2_data)
        db.session.add(test_playlist1)
        db.session.add(test_playlist2)
        db.session.commit()
        r = db.session.query(Playlist).filter_by(thumbnail="THUMBNAIL").all()
        self.assertEqual(len(r), 2)
        db.session.query(Playlist).filter_by(thumbnail="THUMBNAIL").delete()
        db.session.query(Channel).filter_by(
            channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()

    def test3_playlist(self):
        c = Channel(**CHANNEL_DATA)
        db.session.add(c)
        test_playlist = Playlist(**PLAYLIST_DATA)
        before_count = db.session.query(Playlist).count()
        db.session.add(test_playlist)
        db.session.commit()
        after_count = db.session.query(Playlist).count()
        self.assertEqual(after_count, before_count + 1)
        db.session.query(Playlist).filter_by(
            playlist_id=PLAYLIST_DATA["playlist_id"]).delete()
        db.session.query(Channel).filter_by(
            channel_id=CHANNEL_DATA["channel_id"]).delete()
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
