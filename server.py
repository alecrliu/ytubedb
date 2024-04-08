"""Postman API server for project"""


from flask import jsonify
from flask_cors import CORS
from database import app, db, Channel, Playlist, Video
from gitlabStats import commit_counts, issue_counts

CORS(app)

def Channel_to_dict(self):
        return {
            "channelID": self.channel_id,
            "channelName": self.channelName,
            "description": self.description,
            "subscriberCount": self.subscriberCount,
            "viewCount": self.viewCount,
            "videoCount": self.videoCount,
            "thumbnail": self.thumbnail
        },

def Video_to_dict(self):
        return {
            "videoID": self.video_id,
            "title": self.title,
            "description": self.description,
            "viewCount": self.viewCount,
            "likeCount": self.likeCount,
            "thumbnail": self.thumbnail,
            "commentCount":self.commentCount,
            "channelID":self.channel_id
        },

def Playlist_to_dict(self):
        return {
            "playlistID": self.playlist_id,
            "channelID": self.channel_id,
            "title": self.title,
            "publishedAt": self.publishedAt,
            "description": self.description,
            "videoCount": self.videoCount,
            "thumbnail": self.thumbnail
        },

@app.route('/api/about', methods=['GET'])
def about():
    response = {
        'nirmalCommits': commit_counts["Nirmal"],
        'nirmalIssues': issue_counts["Nirmal"],
        'adrianCommits':commit_counts["Adrian"],
        'adrianIssues':issue_counts["Adrian"],
        'alecCommits':commit_counts["Alec"],
        'alecIssues':issue_counts["Alec"],
        'junyuCommits':commit_counts["Junyu"],
        'junyuIssues':issue_counts["Junyu"],
        'totalCommits': sum(commit_counts.values()),
        'totalIssues': sum(issue_counts.values())
    }
    return jsonify(response)

@app.route('/api/channels/<int:page_num>', methods=['GET'])
def showChannels(page_num):
    per_page = 12
    total_channels = Channel.query.count()
    total_pages = round(total_channels/ per_page)
    channels_info = Channel.query.paginate(per_page=12, page=page_num, error_out=False)
    channels = [Channel_to_dict(channel) for channel in channels_info.items]  # Assuming a to_dict method on your model
    return jsonify(channels=channels, current_page=page_num,total_pages=total_pages)

@app.route('/api/channel/<string:channelId>', methods=['GET'])
def showChannel(channelId):
    channel_info = Channel.query.filter_by(channel_id=channelId).first()
    if channel_info is None:
        return jsonify({'error': 'Channel not found'}), 404
    videos = [Video_to_dict(video) for video in Video.query.filter_by(channel_id=channelId).all()]
    playlists = [Playlist_to_dict(playlist) for playlist in Playlist.query.filter_by(channel_id=channelId).all()]
    return jsonify(channel=Channel_to_dict(channel_info), videos=videos, playlists=playlists)

@app.route('/api/videos/<int:page_num>', methods=['GET'])  # videos page displays multiple videos
def showVideos(page_num):
    per_page = 12
    total_videos = Video.query.count()
    total_pages = round(total_videos / per_page)
    videos_info = Video.query.paginate(per_page=12, page=page_num, error_out=True)
    videos_info = [Video_to_dict(videos) for videos in videos_info.items]
    return jsonify(videos=videos_info, current_page=page_num,total_pages=total_pages)

@app.route('/api/video/<string:videoId>', methods=['GET'])  # video page displays single video
def oneVideo(videoId):
    video = Video.query.filter_by(video_id=videoId).first()
    if video is None:
        return jsonify({'error': 'Video not found'}), 404
    channel_dict = Channel_to_dict(video.channels) if video.channels else None
    playlists_dict = [Playlist_to_dict(playlist) for playlist in video.inPlaylist] if video.inPlaylist else []
    video_dict = Video_to_dict(video)
    return jsonify(video=video_dict, channel=channel_dict, playlists=playlists_dict)


# playlists page display multiple videos
@app.route('/api/playlists/<int:page_num>', methods=['GET'])
def showPlaylist(page_num):
    per_page = 12
    total_playlists = Playlist.query.count()
    total_pages = round(total_playlists / per_page)
    playlists_info = Playlist.query.paginate(per_page=12, page=page_num, error_out=True)
    playlists_info = [Playlist_to_dict(playlists) for playlists in playlists_info.items]
    return jsonify(playlists=playlists_info, current_page=page_num, total_pages=total_pages)


# playlists page display single playlist
@app.route('/api/playlist/<string:playlistId>', methods=['GET'])
def playList(playlistId):
    playlist_info = Playlist.query.filter_by(playlist_id=playlistId).first()
    if playlist_info is None:
        return jsonify({'error': 'Playlist not found'}), 404
    channel_dict = Channel_to_dict(playlist_info.channels) if playlist_info.channels else None
    videos_dict = [Video_to_dict(video) for video in playlist_info.videos] if playlist_info.videos else []
    playlist_dict = Playlist_to_dict(playlist_info)
    return jsonify(playlist=playlist_dict, channel=channel_dict, videos=videos_dict)


# debug=True to avoid restart the local development server manually after each change to your code.
# host='0.0.0.0' to make the server publicly available.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')