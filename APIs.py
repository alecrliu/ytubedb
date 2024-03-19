from googleapiclient.discovery import build
import os
import json

YT_KEY = os.getenv("YT_KEY")
YOUTUBE = build("youtube", "v3", developerKey=YT_KEY)

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
        description = channel_data["snippet"].get("description")
        if not description:
            description = "No description available"
        subscriber_count = channel_data["statistics"].get("subscriberCount", 0)
        view_count = channel_data["statistics"].get("viewCount", 0)
        video_count = channel_data["statistics"].get("videoCount", 0)
        thumbnail_url = "No thumbnail available"
        if channel_data["snippet"].get("thumbnails"):
            thumbnail_url = channel_data["snippet"].get("thumbnails")[
                "high"]["url"]
        channelData["channelID"] = channel_id
        channelData["channelName"] = channel_name
        channelData["description"] = description
        channelData["subscriberCount"] = subscriber_count
        channelData["viewCount"] = view_count
        channelData["videoCount"] = video_count
        channelData["thumbnail"] = thumbnail_url
    return channelData

# Get channel id and video json of a video
def get_one_video(video_id, channel_id, youtube, checkChannelID=True):
    videoData = {}
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()
    if response.get("items") and (not checkChannelID or response["items"][0]["snippet"]["channelId"] == channel_id):
        video_data = response["items"][0]
        title = video_data["snippet"]["title"]
        description = video_data["snippet"].get("description")
        if not description:
            description = "No description available"
        view_count = video_data["statistics"].get("viewCount", 0)
        like_count = video_data["statistics"].get("likeCount", 0)
        comment_count = video_data["statistics"].get("commentCount", 0)
        thumbnail_url = "No thumbnail available"
        if video_data["snippet"].get("thumbnails"):
            thumbnail_url = video_data["snippet"].get("thumbnails")[
                "high"]["url"]
        videoData["videoID"] = video_id
        videoData["channelID"] = channel_id
        videoData["title"] = title
        videoData["description"] = description
        videoData["viewCount"] = view_count
        videoData["likeCount"] = like_count
        videoData["commentCount"] = comment_count
        videoData["thumbnail"] = thumbnail_url
    return videoData

# Get all video ids and their data sharing same channel id with the playlist


def get_all_videoIDs_from_playlistID(channel_id, playlist_id, youtube):
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    video_ids = set()
    video_dicts = []
    if response.get("items", []):
        for item in response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_dict = get_one_video(video_id, channel_id, youtube)
            if video_dict:
                video_ids.add(video_id)
                video_dicts.append(video_dict)

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
                video_dict = get_one_video(video_id, channel_id, youtube)
                if video_dict:
                    video_ids.add(video_id)
                    video_dicts.append(video_dict)
            next_page_token = response.get("nextPageToken")

    return video_ids, video_dicts

# Get one playlist dictionary from youtube api response
def get_one_playlist(playlist_response, channel_id):
    playlistData = {}
    if playlist_response:
        playlist_id = playlist_response["id"]
        title = playlist_response["snippet"]["title"]
        description = playlist_response["snippet"].get("description")
        if not description:
            description = "No description available"
        published_at = playlist_response["snippet"]["publishedAt"]
        thumbnail_url = "No thumbnail available"
        if playlist_response["snippet"].get("thumbnails"):
            thumbnail_url = playlist_response["snippet"].get("thumbnails")[
                "high"]["url"]
        playlistData["playlistID"] = playlist_id
        playlistData["channelID"] = channel_id
        playlistData["title"] = title
        playlistData["description"] = description
        playlistData["publishedAt"] = published_at
        playlistData["thumbnail"] = thumbnail_url
    return playlistData

# Get at most 10 playlist data (contains individual playlist's videos data) and their video ids of a channel
def get_all_playlistsIDs_from_channelID(channel_id, youtube):
    request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id,
        maxResults=10
    )
    response = request.execute()
    playlists_data = []
    channel_playlist_video_ids = set()
    if response.get("items", []):
        for item in response["items"]:
            playlist_id = item["id"]
            video_ids, video_dicts = get_all_videoIDs_from_playlistID(
                channel_id, playlist_id, youtube)
            if len(video_ids) > 0:
                playlistData = get_one_playlist(item, channel_id)
                if playlistData:
                    playlistData["videoCount"] = len(video_ids)
                    playlistData["videos"] = video_dicts
                    playlists_data.append(playlistData)
                    channel_playlist_video_ids.update(video_ids)

    return playlists_data, channel_playlist_video_ids

# Get remaining at most 25 video ids of a channel only if current
# video count is less than 25
# Max videos per channel if current video count < 25 will be 50
def get_all_videoIDs_from_channelID(channel_id, curr_videos, youtube):
    new_videos_data = []
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
                if video_id not in curr_videos:
                    video_dict = get_one_video(
                        video_id, channel_id, youtube, checkChannelID=False)
                    if video_dict:
                        new_videos_data.append(video_dict)

    return new_videos_data


# Source: https://blog.hubspot.com/marketing/best-youtube-channels
channel_ids = [
    'UC-lHJZR3Gqxm24_Vd_AJ5Yw',     # 1. PewDiePie
    'UCIPPMRA040LQr5QPyJEbmXA',     # 2. MrBeast Gaming
    'UCYiGq8XF7YQD00x7wAd62Zg',     # 3. JuegaGerman
    'UCV4xOVpbcV8SdueDCOxLXtQ',     # 4. Fernanfloo
    'UCJFp8uSYCjXOMnkUyb3CQ3Q',     # 5. Tasty
    'UCpSgg_ECBj25s9moCDfSTsA',     # 6. Jamie Oliver
    'UCNbngWUqL2eqRw12yAwcICg',     # 7. Laura in the Kitchen
    'UCJHA_jMfCvEnv-3kRjTCQXw',     # 8. Babish Culinary Universe
    'UC1dVfl5-I98WX3yCy8IJQMg',     # 9. Quiet Quest - Study Music
    'UCNlfGuzOAKM1sycPuM_QTHg',     # 10. 4K Video Nature - Focus Music
    'UC-l1GAYzCSb8TtWqGxU2K5Q',     # 11. Lofi Everyday
    'UC1bjWVLp2aaJmPcNbi9OOsw',     # 12. Greenred Productions - Relaxing Music
    'UChTHJT8xRQ0ghLjpXu-RgSg',     # 13. StainedHands
    'UCk1HnZpqA3HDHkiAbMnGFaA',     # 14. Yasmin Art Drawing
    'UClQubH2NeMmGLTLgNdLBwXg',     # 15. ZHC
    'UC63mNFJR8EAb8wAIJwoCmTA',     # 16. 5-Minute Crafts FAMILY
    'UC_zgOsTPdML6tol9hLYh4fQ',     # 17. Ballislife
    'UCiWLfSweyRNmLpgEHekhoAg',     # 18. ESPN
    'UCojyGFb8W2xxSsJ5c_XburQ',     # 19. The Fumble
    'UCpVm7bg6pXKo1Pr6k5kxG9A',     # 20. Nat Geo
    'UCsooa4yRKGN_zEE8iknghZA',     # 21. Ted Ed
    'UCHnyfMqiRRG1u-2MsSQLbXA',     # 22. Veritasium
    'UCFKE7WVJfvaHW5q283SxchA',     # 23. Yoga With Adriene
    'UC9MAhZQQd9egwWCxrwSIsJQ',     # 24. HISTORY
    'UCsXVk37bltHxD1rDPwtNM8Q',     # 25. Kurzgesagt – In a Nutshell
    'UCC552Sd-3nyi_tk2BudLUzA',     # 26. AsapSCIENCE
    'UCn8zNIfYAQNdrFRrr8oibKw',     # 27. VICE
    'UCupvZG-5ko_eiXAupbDfxWw',     # 28. CNN
    'UCa10nxShhzNrCE1o2ZOPztg',     # 29. Trap Nation
    'UCpDJl2EmP7Oh90Vylx0dZtA',     # 30. Spinnin' Records
]

# Retrieve existing data
try:
    with open("data/channels.json", "r") as channelFile, open("data/playlists.json", "r") as playlistFile, open("data/videos.json", "r") as videoFile:
        channelsJSON = json.load(channelFile)
        playlistsJSON = json.load(playlistFile)
        videosJSON = json.load(videoFile)
except FileNotFoundError:
    channelsJSON = {}
    playlistsJSON = {}
    videosJSON = {}

for ind, channel_id in enumerate(channel_ids):
    if channel_id not in channelsJSON:
        currChannelDict = get_one_channel(channel_id, YOUTUBE)
        print(currChannelDict["channelName"])
        if currChannelDict:
            channelsJSON[channel_id] = currChannelDict
            currPlaylistsList, currVideoIDs = get_all_playlistsIDs_from_channelID(
                channel_id, YOUTUBE)
            playlistsJSON[channel_id] = currPlaylistsList
            newVideos = get_all_videoIDs_from_channelID(
                channel_id, currVideoIDs, YOUTUBE)
            videosJSON[channel_id] = newVideos
    else:
        print(channelsJSON[channel_id]["channelName"])
    print()
    print(f"{ind + 1}/{len(channel_ids)} DONE")
    print("-" * 50)

# Push/Update data
with open("data/channels.json", "w+") as channelFile, open("data/playlists.json", "w+") as playlistFile, open("data/videos.json", "w+") as videoFile:
    json.dump(channelsJSON, channelFile, indent=4, ensure_ascii=False)
    json.dump(playlistsJSON, playlistFile, indent=4, ensure_ascii=False)
    json.dump(videosJSON, videoFile, indent=4, ensure_ascii=False)
