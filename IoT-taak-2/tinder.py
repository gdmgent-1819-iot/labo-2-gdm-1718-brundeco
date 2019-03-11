from sense_hat import SenseHat
import time
import requests
import json

sense = SenseHat()
sense.clear(0, 0, 0)
display_colour = (100, 30, 150)

def fetchProfile():
    print('Fetch new profile')

    url = 'https://randomuser.me/api/?results=3'
    json_data = requests.get(url).json()['results'][0] 
    global profileObj
    global profileStr
    global led_string 

    profileObj = {
        'firstname': str(json_data['name']['first']),
        'lastname': str(json_data['name']['last']),
        'age': str(json_data['dob']['age']),
        # 'state': null
    }
    
    print profileObj

    profileStr = profileObj['firstname'] + ' ' + profileObj['lastname'] + ' ' + profileObj['age']
fetchProfile()

def like(profileObj):
    print(profileObj)
    with open("data.json", "a") as json_file:
        profileObj.state = 'liked'
        json_file.write("{}\n".format(json.dumps(profileObj)))

def skip(profileObj):
    print(profileObj)
    with open("data.json", "a") as json_file:
        profileObj.state = 'skipped'
        json_file.write("{}\n".format(json.dumps(profileObj)))

while True:
    for event in sense.stick.get_events():
        if event.action == "pressed":
            if event.direction == "left":
                print('left')
                like()
                sense.show_message(profileStr, text_colour=display_colour)
                fetchProfile()
            elif event.direction == "right":
                print('right')
                skip()
                sense.show_message(profileStr, text_colour=display_colour)
                fetchProfile()