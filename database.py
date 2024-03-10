"""JSON file data modification for entries into database"""

from models import app, db, Channel, Playlist, Video
from googleapiclient.discovery import build
import os
import json

YT_KEY = os.getenv("YT_KEY")

channel_ids = [
	'UC-lHJZR3Gqxm24_Vd_AJ5Yw', 
	'UCIPPMRA040LQr5QPyJEbmXA', 
	'UCYiGq8XF7YQD00x7wAd62Zg', 
	'UCV4xOVpbcV8SdueDCOxLXtQ', 
	'UCJFp8uSYCjXOMnkUyb3CQ3Q', 
	'UCpSgg_ECBj25s9moCDfSTsA', 
	'UCNbngWUqL2eqRw12yAwcICg', 
	'UCJHA_jMfCvEnv-3kRjTCQXw', 
	'UC1dVfl5-I98WX3yCy8IJQMg', 
	'UCNlfGuzOAKM1sycPuM_QTHg', 
	'UC-l1GAYzCSb8TtWqGxU2K5Q', 
	'UC1bjWVLp2aaJmPcNbi9OOsw', 
	'UChTHJT8xRQ0ghLjpXu-RgSg', 
	'UCk1HnZpqA3HDHkiAbMnGFaA', 
	'UClQubH2NeMmGLTLgNdLBwXg', 
	'UC63mNFJR8EAb8wAIJwoCmTA', 
	'UC_zgOsTPdML6tol9hLYh4fQ', 
	'UCiWLfSweyRNmLpgEHekhoAg', 
	'UCojyGFb8W2xxSsJ5c_XburQ'
]

# Get channel id of video with video id
def get_channelID_of_videoID(video_id):
	youtube = build("youtube", "v3", developerKey=YT_KEY)
	request = youtube.videos().list(
		part="snippet",
		id=video_id
	)
	response = request.execute()
	channel_id = response["items"][0]["snippet"]["channelId"]

	return channel_id

# Get video data
def get_one_video(video_id, channel_obj, playlist_obj=None):
	videoData = None
	youtube = build('youtube', 'v3', developerKey=YT_KEY)
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
			title=title,
			description=description,
			viewCount=view_count,
			likeCount=like_count,
			commentCount=comment_count,
			thumbnail=thumbnail_url,
			channels=channel_obj
		)
		if playlist_obj:
			videoData.inPlaylist.append(playlist_obj)
	return videoData

# Push video to the database. Check if it's not present in the database already
def push_one_video(db, video_id, video_obj, checkFirst=True):
	pushed = False
	if not checkFirst or not db.session.query(Video).filter_by(videoID=video_id).first():
		db.session.add(video_obj)
		db.session.commit()
		pushed = True
	return pushed

# Get playlist data
def get_one_playlist(playlist_id, channel_obj):
	playlistData = None
	youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
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
			title=title, 
			description=description, 
			publishedAt=published_at,
			videoCount=video_count,
			thumbnail=thumbnail_url,
			channels=channel_obj
		)
	return playlistData

# Push playlist to the database
def push_one_playlist(db, playlist_obj):
	db.session.add(playlist_obj)
	db.session.commit()
	return True

# Get channel data
def get_one_channel(channel_id):
	channelData = None
	youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
	request = youtube.channels().list(
		part="snippet,statistics",
		id=channel_id
	)
	response = request.execute()
	items = response.get("items", [])
	if items:
		channel_data = items[0]
		channel_name = channel_data["snippet"]["title"]
		description = channel_data["snippet"].get("description", "No description available")
		subscriber_count = channel_data["statistics"].get("subscriberCount", 0)
		view_count = channel_data["statistics"].get("viewCount", 0)
		video_count = channel_data["statistics"].get("videoCount", 0)
		thumbnail_url = "No thumbnail available"
		if channel_data["snippet"].get("thumbnails"):
			thumbnail_url = channel_data["snippet"].get("thumbnails")["default"]["url"]
		channelData = Channel(
			channelID=channel_id,
			channelName=channel_name,
			description=description,
			subscriberCount=subscriber_count,
			viewCount=view_count,
			videoCount=video_count,
			thumbnail=thumbnail_url
		)
	return channelData

# Push channel to the database
def push_one_channel(db, channel_obj):
	db.session.add(channel_obj)
	db.session.commit()
	return True

# Push all videos from a particular playlist. Check if it shares same channel id with playlist
def push_all_videos_from_playlist(db, playlist_id, channel_id, channel_obj):
	youtube = build('youtube', 'v3', developerKey=YT_KEY)
	request = youtube.playlistItems().list(
		part="snippet",
		playlistId=playlist_id,
		maxResults=50
	)
	response = request.execute()
	video_count = 0
	currPlaylistObj = get_one_playlist(playlist_id, channel_obj)

	if currPlaylistObj:
		# Add videos of the same channel in the playlist to the database
		for item in response["items"]:
			if get_channelID_of_videoID(item["snippet"]["resourceId"]["videoId"]) == channel_id:
				video_id = item["snippet"]["resourceId"]["videoId"]
				currVideoObj = get_one_video(video_id, channel_obj, currPlaylistObj)
				if currVideoObj:
					push_one_video(db, video_id, currVideoObj)
					video_count += 1

		# Next page if any
		next_page_token = response.get("nextPageToken")
		while next_page_token:
			request = youtube.playlistItems().list(
				part="snippet",
				playlistId=playlist_id,
				maxResults=50,
				pageToken=next_page_token
			)
			response = request.execute()
			for item in response["items"]:
				if get_channelID_of_videoID(item["snippet"]["resourceId"]["videoId"]) == channel_id:
					video_id = item["snippet"]["resourceId"]["videoId"]
					currVideoObj = get_one_video(video_id, channel_obj, currPlaylistObj)
					if currVideoObj:
						push_one_video(db, video_id, currVideoObj)
						video_count += 1
			next_page_token = response.get("nextPageToken")

	return video_count, currPlaylistObj

# Push at most 50 videos from a particular channel
def push_all_videos_from_channel(db, channel_id):
	youtube = build('youtube', 'v3', developerKey=YT_KEY)
	request = youtube.search().list(
		part="snippet",
		channelId=channel_id,
		maxResults=50,
		type="video"
	)
	response = request.execute()
	currChannelObj = get_one_channel(channel_id)

	if currChannelObj:
		for item in response["items"]:
			video_id = item["id"]["videoId"]
			currVideoObj = get_one_video(video_id, currChannelObj)
			push_one_video(db, video_id, currVideoObj, checkFirst=False)

	return currChannelObj

# Push all the playlist from a particular channel. Make sure that playlist after filtration of 
# videos not sharing same channel id has positive number of videos in it
def push_all_playlists_from_channel(db, channel_id):
	youtube = build('youtube', 'v3', developerKey=YT_KEY)
	request = youtube.playlists().list(
		part="snippet",
		channelId=channel_id,
		maxResults=50
	)
	response = request.execute()
	currChannelObj = push_all_videos_from_channel(db, channel_id)

	if currChannelObj:
		for item in response["items"]:
			playlist_id = item["id"]
			video_count, currPlaylistObj = push_all_videos_from_playlist(db, playlist_id, channel_id, currChannelObj)
			if video_count > 0:
				push_one_playlist(db, currPlaylistObj)

		# Next page if any
		next_page_token = response.get("nextPageToken")
		while next_page_token:
			request = youtube.playlists().list(
				part="snippet",
				channelId=channel_id,
				maxResults=50,
				pageToken=next_page_token
			)
			response = request.execute()
			for item in response["items"]:
				playlist_id = item["id"]
				video_count, currPlaylistObj = push_all_videos_from_playlist(db, playlist_id, channel_id, currChannelObj)
				if video_count > 0:
					push_one_playlist(db, currPlaylistObj)
			next_page_token = response.get("nextPageToken")

	return currChannelObj

'''
	Push all channels

	Pushing flow
	For each channel
		1) Push at most 50 videos of the channel (Fills videos table)
		2) Push all the unique videos from all the playlists of the channel (Fills videos table)
		3) Push all the playlists of the channel (Fills playlists table)
		4) Push the channel (Fills channels table)
'''
def push_all_channels(db, channel_ids):
	for channel_id in channel_ids:
		currChannelObj = push_all_playlists_from_channel(db, channel_id)
		push_one_channel(db, currChannelObj)
	return True