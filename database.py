from models import app, db, Channel, Playlist, Video
import os
import json

def create_Channel(channel_data):
	channel_obj = Channel(
		channelID=channel_data["channelID"], 
		channelName=channel_data["channelName"], 
		description=channel_data["description"], 
		subscriberCount=channel_data["subscriberCount"], 
		viewCount=channel_data["viewCount"], 
		videoCount=channel_data["videoCount"], 
		thumbnail=channel_data["thumbnail"]
	)
	return channel_obj

def create_Playlist(playlist_data):
	playlist_obj = Playlist(
		playlistID=playlist_data["playlistID"], 
		title=playlist_data["title"], 
		description=playlist_data["description"], 
		publishedAt=playlist_data["publishedAt"], 
		videoCount=playlist_data["videoCount"], 
		thumbnail=playlist_data["thumbnail"], 
		channelID=playlist_data["channelID"]
	)
	return playlist_obj

def create_Video(video_data):
	video_obj = Video(
		videoID=video_data["videoID"], 
		title=video_data["title"], 
		description=video_data["description"], 
		viewCount=video_data["viewCount"], 
		likeCount=video_data["likeCount"], 
		commentCount=video_data["commentCount"], 
		thumbnail=video_data["thumbnail"], 
		channelID=video_data["channelID"]
	)
	return video_obj

def process_channelJSON(db, channelJSONfilepath):
	with open(channelJSONfilepath, "r") as channelFile:
		channelsDict = json.load(channelFile)
		for curr_channel_id in channelsDict:
			curr_channel_data = channelsDict[curr_channel_id]
			curr_channel_obj = create_Channel(curr_channel_data)
			db.session.add(curr_channel_obj)
		db.session.commit()

def process_playlistJSON(db, playlistJSONfilepath):
	with open(playlistJSONfilepath, "r") as playlistFile:
		playlistsDict = json.load(playlistFile)
		for curr_channel_id in playlistsDict:
			curr_playlists = playlistsDict[curr_channel_id]
			for curr_playlist_data in curr_playlists:
				curr_playlist_obj = create_Playlist(curr_playlist_data)
				for curr_video_data in curr_playlist_data["videos"]:
					curr_video_obj = create_Video(curr_video_data)
					curr_playlist_obj.videos.append(curr_video_obj)
					db.session.add(curr_video_obj)
				db.session.add(curr_playlist_obj)
		db.session.commit()

def process_videoJSON(db, videoJSONfilepath):
	with open(videoJSONfilepath, "r") as videoFIle:
		videosDict = json.load(videoFIle)
		for curr_channel_id in videosDict:
			curr_videos = videosDict[curr_channel_id]
			for curr_video_data in curr_videos:
				curr_video_obj = create_Video(curr_video_data)
				db.session.add(curr_video_obj)
		db.session.commit()

channelJSONfilepath = "allData/channels.json"
process_channelJSON(db, channelJSONfilepath)
playlistJSONfilepath = "allData/playlists.json"
process_playlistJSON(db, playlistJSONfilepath)
videoJSONfilepath = "allData/videos.json"
process_videoJSON(db, videoJSONfilepath)
