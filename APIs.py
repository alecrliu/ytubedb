"""Uses APIs to get, parse, and dump data into JSON files"""


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

def get_channelID_of_videoID(video_id):
	youtube = build("youtube", "v3", developerKey=YT_KEY)
	request = youtube.videos().list(
		part="snippet",
		id=video_id
	)
	response = request.execute()
	if not response.get("items"):
		return None
	channel_id = response["items"][0]["snippet"]["channelId"]

	return channel_id

def get_all_videoIDs_from_playlistID(channel_id, playlist_id):
	youtube = build('youtube', 'v3', developerKey=YT_KEY)
	request = youtube.playlistItems().list(
		part="snippet",
		playlistId=playlist_id,
		maxResults=50
	)
	response = request.execute()
	video_ids = []
	for item in response["items"]:
		if get_channelID_of_videoID(item["snippet"]["resourceId"]["videoId"]) == channel_id:
			video_ids.append(item["snippet"]["resourceId"]["videoId"])

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
				video_ids.append(item["snippet"]["resourceId"]["videoId"])
		next_page_token = response.get("nextPageToken")

	return video_ids

def get_all_videoIDs_from_channelID(channel_id):
	youtube = build("youtube", "v3", developerKey=YT_KEY)
	request = youtube.search().list(
		part="snippet",
		channelId=channel_id,
		maxResults=50,
		type="video"
	)
	response = request.execute()
	video_ids = []
	for item in response["items"]:
		video_ids.append(item["id"]["videoId"])

	return video_ids

def get_all_playlistsIDs_from_channelID(channel_id):
	youtube = build('youtube', 'v3', developerKey=YT_KEY)
	request = youtube.playlists().list(
		part="snippet",
		channelId=channel_id,
		maxResults=50
	)
	response = request.execute()
	playlist_ids = {}
	for item in response["items"]:
		video_list = get_all_videoIDs_from_playlistID(channel_id, item["id"])
		if len(video_list) > 0:
			playlist_ids[item["id"]] = video_list

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
			video_list = get_all_videoIDs_from_playlistID(channel_id, item["id"])
			if len(video_list) > 0:
				playlist_ids[item["id"]] = video_list
		next_page_token = response.get("nextPageToken")

	return playlist_ids

#print(get_all_playlistsIDs_from_channelID("UC-l1GAYzCSb8TtWqGxU2K5Q"))
