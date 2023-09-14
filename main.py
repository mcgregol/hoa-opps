import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import googlemaps, json, requests, time, schedule

def change_name(place_id):
	global count
	count = count + 1
	driver = uc.Chrome(headless=False)
	#   place id should be variable
	driver.get('https://www.google.com/maps/search/?api=1&query=sunset+lake+park+saline+michigan&query_place_id=' + place_id)
	main_form = driver.find_element(By.XPATH, "/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]")
	main_form.send_keys(Keys.DOWN)
	driver.find_element(By.XPATH, "/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div/button").click()
	time.sleep(5)
	driver.find_element(By.XPATH, "//*[@id=\"rap-card\"]/div/div/div[2]/button").click()
	time.sleep(5)
	driver.find_element(By.XPATH, "//*[@id=\"identifierId\"]").send_keys("")
	time.sleep(5)
	driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button").click()
	time.sleep(5)
	driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys("")
	time.sleep(5)
	driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button").click()
	time.sleep(5)
	driver.find_element(By.XPATH, "//*[@id=\"modal-dialog\"]/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div/button").click()
	time.sleep(5)
	driver.switch_to.frame('rap-on-boq')
	driver.find_element(By.CSS_SELECTOR, "#i4").clear()
	driver.find_element(By.CSS_SELECTOR, "#i4").send_keys("Sunset Lake Park (Public)")
	driver.find_element(By.XPATH, "//*[@id=\"dCuTx\"]").click()
	driver.switch_to.default_content()

def notify(body_count, had_to_change):
	if had_to_change == False:
		r = requests.post('https://maker.ifttt.com/trigger/name_update/json/with/key/o3ilKzP0a_hGrSCwV7nTYjMc72KGffKIJV1o9aGt7Af', json={'Body Count': count})
	else:
		r = requests.post('https://maker.ifttt.com/trigger/name_update/json/with/key/o3ilKzP0a_hGrSCwV7nTYjMc72KGffKIJV1o9aGt7Af', json={'New Body Count': count})

def go_time(maps):
	# get current name of park
	park = maps.find_place('sunset lake park saline mi', 'textquery')
	details = maps.place(park['candidates'][0]['place_id'])
	park_name = details['result']['name']

	# check that the name is what it should be
	# change it back if not, then send notification
	if not park_name == 'Sunset Lake Park (Public)':
		change_name(park['candidates'][0]['place_id'])
		notify(count, True)
	else:
		notify(count, False)

# start sesh
count = 3
api_key = open('key.txt', 'r').read()
gmaps = googlemaps.Client(key=api_key)

schedule.every(12).hours.do(go_time, maps=gmaps)

while True:
	schedule.run_pending()
	time.sleep(1)