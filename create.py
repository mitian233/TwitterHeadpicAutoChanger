import os
import tweepy
import json

# Proxy settings(optional)
#os.environ["http_proxy"] = "http://127.0.0.1:18899"
#os.environ["https_proxy"] = "http://127.0.0.1:18899"
# Proxy settings end

app_config_file = 'app.config.json'
user_config_file = 'user.config.json'

# Authentication
if not os.path.exists(app_config_file):
    print('Collect app key and secret')
    consumer_key = input('Consumer key of your application:')
    consumer_secret = input('Consumer secret of your application:')
    application_info = {'consumer_key': consumer_key, 'consumer_secret': consumer_secret}
    with open(app_config_file, 'w') as json_file:
        json.dump(application_info, json_file)
        json_file.close()
        print('Successfully linked to your app. ')
with open(app_config_file, 'r') as json_file:
    json_dict = json.load(json_file)
    consumer_key = json_dict['consumer_key']
    consumer_secret = json_dict['consumer_secret']
    json_file.close()

print('Consumer key:\033[92m' + consumer_key + '\033[0m \nConsumer secret:\033[92m' + consumer_secret + '\033[0m')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback='oob')

if not os.path.exists(user_config_file):
    print('It seems that you are running this application for the first time. Let\'s creat a config file:')
    print('Authorization:' + auth.get_authorization_url(signin_with_twitter=True))
    verifier = input('Type the PIN code you got here:')
    access_token, access_token_secret = auth.get_access_token(verifier)
    userdata = {'access_token': access_token, 'access_token_secret': access_token_secret}
    with open(user_config_file, 'w') as json_file:
        json.dump(userdata, json_file)
        json_file.close()
        print('Successfully created config file. ')
with open(user_config_file, 'r') as json_file:
    json_dict = json.load(json_file)
    access_token = json_dict['access_token']
    access_token_secret = json_dict['access_token_secret']
    json_file.close()
print('Access Token:\033[92m' + access_token + '\033[0m \nAccess Token secret:\033[92m' + access_token_secret + '\033[0m')
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
