from googleapiclient.discovery import build

def get_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey='apikey')
    request = youtube.videos().list(part='snippet,statistics', id=video_id)
    response = request.execute()
    return response

video_id = 'dQw4w9WgXcQ'
details = get_video_details(video_id)
print(details)

def get_playlist_by_channel(channel_id):
    youtube = build('youtube', 'v3', developerKey='apikey')
    request = youtube.playlists().list(part='snippet', channelId=channel_id)
    response = request.execute()
    return response

channel_id = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'
details = get_playlist_by_channel(channel_id)
print(details)

def get_channel_details(channel_id):
    youtube = build('youtube', 'v3', developerKey='apikey')
    request = youtube.channels().list(part='snippet', id=channel_id)
    response = request.execute()
    return response

channel_id = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'
details = get_channel_details(channel_id)
print(details)

def get_videos_by_playlists(playlist_id):
    youtube = build('youtube', 'v3', developerKey='apikey')
    request = youtube.playlistItems().list(part='snippet', id=playlist_id)
    response = request.execute()
    return response

playlist_id = 'PLOU2XLYxmsILxbiyDRGC94XuT2dBXNY3n'
get_videos_by_playlists(playlist_id)
print(details)

def get_playlists_detail(playlist_id):
    youtube = build('youtube', 'v3', developerKey='apikey')
    request = youtube.playlistItems().list(part='snippet', id=playlist_id)
    response = request.execute()
    return response

playlist_id = 'PLOU2XLYxmsILxbiyDRGC94XuT2dBXNY3n'
get_videos_by_playlists(playlist_id)
print(details)