import requests
import urllib.request
import datetime
import os
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
from random import randrange
from PIL import Image
from resizeimage import resizeimage

USERNAME="user_name"
PASSWORD="user_pass"

url = ["https://meme-api.com/gimme/wholesomememes", "https://meme-api.com/gimme/memes", "https://meme-api.com/gimme/meirl", "https://meme-api.com/gimme/funny", "https://meme-api.com/gimme/OnlyWholesomeMemes"]
current_time = datetime.datetime.now()
date = str(current_time)[:10]
text = str(date) + str(current_time.microsecond)



res = requests.get(url[randrange(5)]).json()
while('.gif' in res['preview'][-1]):
    print("here")
    res = requests.get(url[randrange(5)]).json()

imageurl = res['preview'][-1]
urllib.request.urlretrieve(imageurl, f'./{text}.jpeg')

# print(res)

logger = logging.getLogger()
caption = "caption"

def login_user():

    cl = Client()
    session = cl.load_settings("./session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
    
    
    media = cl.photo_upload(path="./"+text+"1.jpeg", caption=caption)
    os.remove("./"+text+".jpeg")
    
login_user()
