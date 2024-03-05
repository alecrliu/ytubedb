"""Uses APIs to get, parse, and dump data into JSON files"""


from googleapiclient.discovery import build
import os
import json


YT_KEY = os.getenv("YT_KEY")

# # dump data into json file and change number of results
# # repeat for all other api methods you need to use
# # using search is 100 credits so it might be better to use other ways


def get_playlists(channel_ids):
    youtube = build('youtube', 'v3', developerKey=YT_KEY)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_ids,  # filter can be a string of channel ids
        maxResults=20,  # does not matter since list will limit results
        type="playlist"
    )
    response = request.execute()
    print(response)
    with open('data/example.json', 'w') as fp:
        json.dump(response, fp, indent=4)


# # use a list of ids in other methods to get multiple data
# # loop thru channels json file to get the right ids for playlists
# # useless for videos cuz we need playlist id for videos (no filter for that)
channel_ids = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'
get_playlists(channel_ids)


# def get_channel_details(channel_id):
#     youtube = build('youtube', 'v3', developerKey=YT_KEY)
#     request = youtube.channels().list(part='snippet', id=channel_id)
#     response = request.execute()
#     return response


# channel_id = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'
# details = get_channel_details(channel_id)
# print(details)


# def get_playlist_by_channel(channel_id):
#     youtube = build('youtube', 'v3', developerKey=YT_KEY)
#     request = youtube.playlists().list(part='snippet', channelId=channel_id)
#     response = request.execute()
#     return response


# channel_id = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'
# details = get_playlist_by_channel(channel_id)
# print(details)


# def get_playlists_detail(playlist_id):
#     youtube = build('youtube', 'v3', developerKey=YT_KEY)
#     request = youtube.playlistItems().list(part='snippet', id=playlist_id)
#     response = request.execute()
#     return response


# playlist_id = 'PLOU2XLYxmsILxbiyDRGC94XuT2dBXNY3n'
# get_videos_by_playlists(playlist_id)
# print(details)


# def get_videos_by_playlists(playlist_id):
#     youtube = build('youtube', 'v3', developerKey=YT_KEY)
#     request = youtube.playlistItems().list(part='snippet', id=playlist_id)
#     response = request.execute()
#     return response


# playlist_id = 'PLOU2XLYxmsILxbiyDRGC94XuT2dBXNY3n'
# get_videos_by_playlists(playlist_id)
# print(details)


# def get_video_details(video_id):
#     youtube = build('youtube', 'v3', developerKey=YT_KEY)
#     request = youtube.videos().list(part='snippet,statistics', id=video_id)
#     response = request.execute()
#     return response


# video_id = 'dQw4w9WgXcQ'
# details = get_video_details(video_id)
# print(details)
