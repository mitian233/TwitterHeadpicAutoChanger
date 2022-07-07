import os
import json
import tweepy
import schedule
import time

#os.environ["http_proxy"] = "http://127.0.0.1:18899"
#os.environ["https_proxy"] = "http://127.0.0.1:18899"

app_config_file = 'app.config.json'
user_config_file = 'user.config.json'
with open(app_config_file, 'r') as json_file:
    json_dict = json.load(json_file)
    consumer_key = json_dict['consumer_key']
    consumer_secret = json_dict['consumer_secret']
    json_file.close()
with open(user_config_file, 'r') as json_file:
    json_dict = json.load(json_file)
    access_token = json_dict['access_token']
    access_token_secret = json_dict['access_token_secret']
    json_file.close()
API_KEY = consumer_key
API_SECRET = consumer_secret

ACCESS_TOKEN = access_token
ACCESS_TOKEN_SECRET = access_token_secret

def last_headpic():
    if not os.path.exists("last_headpic.json"):
        writeToFile(0)
    with open("last_headpic.json", "r") as f:
        jsdict = json.load(f)
        last_headpic = jsdict["last_headpic"]
        f.close()
    return last_headpic

def writeToFile(Number):
    jsdict = {"last_headpic": Number}
    with open("last_headpic.json", "w") as f:
        json.dump(jsdict, f)
        f.close()

def pickImg():
    currentNumber = last_headpic()
    if currentNumber == 1:
        return 2
    elif currentNumber == 2:
        return 1

def job():
    print("Now changing headpic...")
    picNumber = pickImg()
    print("I choose " + str(picNumber) + ".jpg")
    writeToFile(picNumber)
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    current = os.getcwd()
    os.chdir("headpics/")
    filename = str(picNumber) + ".jpg"
    api.update_profile_image(filename)
    os.chdir(current)

schedule.every().day.at("17:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
