from googleapiclient.discovery import build
import os
import json

YT_KEY = os.getenv("YT_KEY")
YOUTUBE = build("youtube", "v3", developerKey=YT_KEY)

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

# Get channel id of a video
def get_channelID_of_videoID(video_id, youtube):
	request = youtube.videos().list(
		part="snippet",
		id=video_id
	)
	response = request.execute()
	channel_id = ""
	if response.get("items"):
		channel_id = response["items"][0]["snippet"]["channelId"]

	return channel_id

# Get channel data
def get_one_channel(channel_id, youtube):
	channelData = {}
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
		channelData["channelID"] = channel_id
		channelData["channelName"] = channel_name
		channelData["description"] = description
		channelData["subscriberCount"] = subscriber_count
		channelData["viewCount"] = view_count
		channelData["videoCount"] = video_count
		channelData["thumbnail"] = thumbnail_url
	return channelData

# Get all video ids of a playlist sharing same channel id
def get_all_videoIDs_from_playlistID(channel_id, playlist_id, youtube):
	request = youtube.playlistItems().list(
		part="snippet",
		playlistId=playlist_id,
		maxResults=50
	)
	response = request.execute()
	video_ids = set()
	if response.get("items", []):
		for item in response["items"]:
			video_id = item["snippet"]["resourceId"]["videoId"]
			if get_channelID_of_videoID(video_id, youtube) == channel_id:
				video_ids.add(video_id)

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
				video_id = item["snippet"]["resourceId"]["videoId"]
				if get_channelID_of_videoID(video_id, youtube) == channel_id:
					video_ids.add(video_id)
			next_page_token = response.get("nextPageToken")

	return video_ids

# Get at most 10 playlist ids and their video ids of a channel
def get_all_playlistsIDs_from_channelID(channel_id, youtube):
	request = youtube.playlists().list(
		part="snippet",
		channelId=channel_id,
		maxResults=10
	)
	response = request.execute()
	playlist_ids = {}
	channel_playlist_video_ids = set()
	if response.get("items", []):
		for item in response["items"]:
			playlist_id = item["id"]
			video_set = get_all_videoIDs_from_playlistID(channel_id, playlist_id, youtube)
			if len(video_set) > 0:
				playlist_ids[playlist_id] = list(video_set)
				channel_playlist_video_ids.update(video_set)

	return playlist_ids, channel_playlist_video_ids

# Get remaining at most 25 video ids of a channel only if current 
# video count is less than 25
# Max videos per channel if current video count < 25 will be 50
def get_all_videoIDs_from_channelID(channel_id, curr_videos, youtube):
	if len(curr_videos) < 25:
		request = youtube.search().list(
			part="snippet",
			channelId=channel_id,
			maxResults=25,
			type="video"
		)
		response = request.execute()
		if response.get("items", []):
			for item in response["items"]:
				video_id = item["id"]["videoId"]
				curr_videos.add(video_id)

	return curr_videos

with open("allData/channels.json", "w+") as channelFile:
	for channel_id in channel_ids:
		currChannelDict = get_one_channel(channel_id, YOUTUBE)
		if currChannelDict:
			currPlaylists, currVideos = get_all_playlistsIDs_from_channelID(channel_id, YOUTUBE)
			currVideos = get_all_videoIDs_from_channelID(channel_id, currVideos, YOUTUBE)
			currChannelDict["videos"] = list(currVideos)
			currChannelDict["playlists"] = currPlaylists
			json.dump(currChannelDict, channelFile)
