import googlemaps, time

# start sesh
api_key = open('key.txt', 'r').read()
maps = googlemaps.Client(key=api_key)

# get current name of park
park = maps.find_place('sunset lake park saline mi', 'textquery')
details = maps.place(park['candidates'][0]['place_id'])
park_name = details['result']['name']

# check that the name is what it should be
# change it back if not
if park_name == 'Sunset Lake (Public)':
	print("YASSSSSS")
else:
	print("GRRRRRR")