from models import app, db, Channel, Playlist, Video
import os
import json

def process_channelJSON(db, channelJSONfilepath):
	with open(channelJSONfilepath, "r") as channelFile:
		channelsDict = json.load(channelFile)
		for curr_channel_id in channelsDict:
			curr_channel_data = channelsDict[curr_channel_id]
			curr_channel_obj = Channel(
				channelID=curr_channel_data["channelID"], 
				channelName=curr_channel_data["channelName"], 
				description=curr_channel_data["description"], 
				subscriberCount=curr_channel_data["subscriberCount"], 
				viewCount=curr_channel_data["viewCount"], 
				videoCount=curr_channel_data["videoCount"], 
				thumbnail=curr_channel_data["thumbnail"]
			)
			db.session.add(curr_channel_obj)
		db.session.commit()

#channelJSONfilepath = "allData/channels.json"
#process_channelJSON(db, channelJSONfilepath)