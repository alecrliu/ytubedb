"""JSON file data modification for entries into database"""


import json
# # Uncomment when done with models.py
# from models import app, db, Channel, Playlist, Video


def load_json(filename):
    with open(filename) as file:
        jsn = json.load(file)
        file.close()

    return jsn


# def create_channels():
#     channels = load_json('channels.json')

#     for channel in channels:
#         title = channel['title']
#         id = channel['id']

#         newChannel = Channel(title = title, id = id)

#         # After I create the channel, I can then add it to my session.
#         db.session.add(newChannel)
#         # commit the session to my DB.
#         db.session.commit()

# create_channels()
