# import libraries 
from sense_hat import SenseHat
import time
import requests
import json

# initialise sensehat, led switch off, led color
sense = SenseHat()
sense.clear(0, 0, 0)
display_colour = (100, 30, 150)


# Fetch a new profile from the random user API and put data in object
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
        'state': ''
    }
    
    profileStr = profileObj['firstname'] + ' ' + profileObj['lastname'] + ' ' + profileObj['age']
fetchProfile()


# define like function, triggered on joystick left movement
# adds a state of 'liked' to object and add object to data.json
def like(profileObj):
    with open("data.json", "a") as json_file:
        profileObj['state'] = 'liked'
        json_file.write("{}\n".format(json.dumps(profileObj)))

# define skip function, triggered on joystick right movement
# adds a state of 'skipped' to object and add object to data.json
def skip(profileObj):
    with open("data.json", "a") as json_file:
        profileObj['state'] = 'skipped'
        json_file.write("{}\n".format(json.dumps(profileObj)))


def main():
    while True:
        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == "left":
                    print('left')
                    like(profileObj)
                    sense.show_message(profileStr, text_colour=display_colour)
                    fetchProfile()
                elif event.direction == "right":
                    print('right')
                    skip(profileObj)
                    sense.show_message(profileStr, text_colour=display_colour)
                    fetchProfile()
main()