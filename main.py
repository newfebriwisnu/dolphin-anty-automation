import os
import time
import requests
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

def log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] {message}")
    
def get_profile(profile_id=""):
    headers = {"Authorization" : AUTH_TOKEN}
    response = requests.get(f"https://dolphin-anty-api.com/browser_profiles/{profile_id}", headers=headers)
    result = json.loads(response.text)
    return result

def start_profile(profile_id):
    return f"http://{HOST}:{PORT}/v1.0/browser_profiles/{profile_id}/start?automation=1"

def stop_profile(profile_id):
    return f"http://{HOST}:{PORT}/v1.0/browser_profiles/{profile_id}/stop"


list_profile = []
for index, profile in enumerate(get_profile()["data"]):
    list_profile.append({"id": profile["id"], "name": profile["name"]})
list_profile = sorted(list_profile, key=lambda k: (k["id"], k["name"]))

for index, profile in enumerate(list_profile):
    print(f"{index+1}. {profile['id']} - {profile['name']}")

selected_index = int(input("Please input profile target: "))
profile_id = list_profile[selected_index-1]["id"]
profile_name = list_profile[selected_index-1]["name"]
log(f"Selected profile: {profile_id} - {profile_name}")

response = requests.get(start_profile(profile_id))
result = json.loads(response.text)
log(result)
    
try:
    remote_host = HOST
    remote_port = result["automation"]["port"]
except:
    input("Press enter to exit")
    exit()

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", f"{remote_host}:{remote_port}")

log("Starting chrome driver")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(chrome_type="chromium").install()), options=options)

time.sleep(3)
driver.get('https://github.com/newfebriwisnu')

time.sleep(3)
driver.get('https://github.com/newfebriwisnu?tab=repositories')

time.sleep(3)
driver.get('https://google.com')

time.sleep(3)
# send script to browser to execute alert "thank you"
driver.execute_script("alert('thank you')")

log("Stop chrome driver")
driver.quit()

log("Stop profile")
response = requests.get(stop_profile(profile_id))
result = json.loads(response.text)
print(result)