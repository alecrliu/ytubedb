"""Uses APIs to get, parse, and dump data into JSON files"""


from googleapiclient.discovery import build
import os
import json


YT_KEY = os.getenv("YT_KEY")


def get_multiple_channels(channel_ids):
    channels_ids_str = ",".join(channel_ids)
    youtube = build('youtube', 'v3', developerKey=YT_KEY)
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channels_ids_str,
        maxResults=50
    )
    response = request.execute()
    with open('data/multiple_channels.json', 'w') as fp:
        json.dump(response, fp, indent=4)


channel_ids = ['UCSJ4mUlpWv1AE6umAC4RlvQ','UC-l1GAYzCSb8TtWqGxU2K5Q']  # Lofi Everyday, Piano cover
get_multiple_channels(channel_ids)


def get_all_playlistsIDs_from_channelID(channel_id):
    youtube = build('youtube', 'v3', developerKey=YT_KEY)
    request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50
    )
    response = request.execute()
    playlist_ids = []
    for item in response["items"]:
        playlist_ids.append(item["id"])

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
            playlist_ids.append(item["id"])
        next_page_token = response.get("nextPageToken")

    return playlist_ids


def get_all_videoIDs_from_playlistID(playlist_id):
    youtube = build('youtube', 'v3', developerKey=YT_KEY)
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_ids[0],
        maxResults=50
    )
    response = request.execute()
    video_ids = []
    for item in response["items"]:
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
            video_ids.append(item["snippet"]["resourceId"]["videoId"])
        next_page_token = response.get("nextPageToken")

    return channel_ids


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
