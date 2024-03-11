from models import app, db, Channel, Playlist, Video
from googleapiclient.discovery import build
import os
import json

YT_KEY = "AIzaSyCKzJGAupHgrCSsv0KUdPJo2cEl_MG3zWU"#os.getenv("YT_KEY")
YOUTUBE = build('youtube', 'v3', developerKey=YT_KEY)

# Create channel object
def get_one_channel(channelDict):
	channelData = Channel(
		channelID=channelDict["channelID"], 
		channelName=channelDict["channelName"], 
		description=channelDict["description"], 
		subscriberCount=channelDict["subscriberCount"], 
		viewCount=channelDict["viewCount"], 
		videoCount=channelDict["videoCount"], 
		thumbnail=channelDict["thumbnail"]
	)
	return channelData

# Push channel object
def push_one_channel(db, channel_obj):
	db.session.add(channel_obj)
	db.session.commit()
	return True

# Get playlist data
def get_one_playlist(youtube, playlist_id, channel_id, videosObjList):
	playlistData = None
	request = youtube.playlists().list(
		part="snippet",
		id=playlist_id
	)
	response = request.execute()
	items = response.get("items", [])
	if items:
		playlist_data = items[0]
		title = playlist_data["snippet"]["title"]
		description = playlist_data["snippet"].get("description", "No description available")
		published_at = playlist_data["snippet"]["publishedAt"]
		video_count = playlist_data["contentDetails"].get("itemCount", 0)
		thumbnail_url = "No thumbnail available"
		if playlist_data["snippet"].get("thumbnails"):
			thumbnail_url = playlist_data["snippet"].get("thumbnails")["default"]["url"]
		playlistData = Playlist(
			playlistID=playlist_id, 
			channelID=channel_id, 
			title=title, 
			description=description, 
			publishedAt=published_at,
			videoCount=video_count,
			thumbnail=thumbnail_url
		)
		playlistData.videos.extend(videosObjList)
	return playlistData

# Get video data
def get_one_video(youtube, video_id, channel_id):
	videoData = None
	request = youtube.videos().list(
		part="snippet,statistics",
		id=video_id
	)
	response = request.execute()
	items = response.get("items", [])
	if items:
		video_data = items[0]
		title = video_data["snippet"]["title"]
		description = video_data["snippet"].get("description", "No description available")
		view_count = video_data["statistics"].get("viewCount", 0)
		like_count = video_data["statistics"].get("likeCount", 0)
		comment_count = video_data["statistics"].get("commentCount", 0)
		thumbnail_url = "No thumbnail available"
		if video_data["snippet"].get("thumbnails"):
			thumbnail_url = video_data["snippet"].get("thumbnails")["default"]["url"]
		videoData = Video(
			videoID=video_id,
			channelID=channel_id,
			title=title,
			description=description,
			viewCount=view_count,
			likeCount=like_count,
			commentCount=comment_count,
			thumbnail=thumbnail_url
		)
	return videoData

'''
	Push all channels

	Pushing flow
	For each channel
		1) 	Push channel data from json
		2)	Initialize empty playlistvideo set
		3) 	From channel json, get playlist data and its videos and push. 
			Easy for playlist. For videos, chek if it doesn't exist in the 
			playlist video set and then push. 
			Make sure to include playlistObj for videoplaylist relationship
		4)	From channel json, get video data and push

	Pseudo code
	for each channelDict:
		currChannelObj = get_one_channel(channelDict)
		channelPlaylists = channelDict["playlists"]
		newChannelVideos = channelDict["videos"]
		for each playlistDict (key=playlistId, value=videos list) in channelPlaylists:
			playlistVideoObjs = list(len(videos_list))
			for each videoID in videos_list:
				currVideoObj = get_one_video(youtube, videoID, currChannelID)
				push_one_video(currVideoObj)
				playlistVideoObjs.append(currVideoObj)
			currPlaylistObj = get_one_playlist(youtube, playlistId, currChannelID, playlistVideoObjs)
			push_one_playlist(currPlaylistObj)
		for each newVideo (value=videoID) in newChannelVideos:
			currVideoObj = get_one_video(youtube, videoID, currChannelID)
			push_one_video(currVideoObj)
		push_one_channel(currChannelObj)
'''
