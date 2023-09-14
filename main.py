import googlemaps, json, requests, time

def change_name():
	global count
	count = count + 1
	pass

def notify(body_count):
	r = requests.post('https://maker.ifttt.com/trigger/name_update/json/with/key/o3ilKzP0a_hGrSCwV7nTYjMc72KGffKIJV1o9aGt7Af', json={'Body Count': count})

# start sesh
count = 2
api_key = open('key.txt', 'r').read()
maps = googlemaps.Client(key=api_key)

# get current name of park
#park = maps.find_place('sunset lake park saline mi', 'textquery')
#details = maps.place(park['candidates'][0]['place_id'])
#park_name = details['result']['name']
park_name = 'don\'t forget to reenable maps api requests, you goober'

# check that the name is what it should be
# change it back if not, then send notification
if not park_name == 'Sunset Lake Park (Public)':
	change_name()
	notify(count)
else:
	notify(count)
