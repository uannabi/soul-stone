import sys
import tweepy
import json

from chalice import Chalice
import boto3
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
import twitter

app = Chalice(app_name='soul-stone')




@app.route('/')
class MyStreamListener(StreamListener):

    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print((f"{tweet.user.name}  : {tweet.text}"))

    def on_error(self, status_code):
        return {"status": status_code}


auth = OAuthHandler(customerKey, customerSecret)
auth.set_access_token(accessToken, accessSecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["Python", "Flask", "Django"], languages=["en"])

# def index():
#     timeline = api.home_timeline()
#     for tweet in timeline:
#         print(f"{tweet.user.name}  : {tweet.text}")

# return {'hello': 'world'}
# api = API(auth, wait_on_rate_limit=True,
#           wait_on_rate_limit_notify=True)


# class Listener(StreamListener):
#     def __init__(self, output_file=sys.stdout):
#         super(Listener, self).__init__()
#         self.output_file = output_file
#
#     def on_status(self, status):
#         print(status.text, file=self.output_file)
#
#     def on_error(self, status_code):
#         print(status_code)
#         return False
#
#
# output = open('stream_output.txt', 'w')
# listener = Listener(output_file=output)
#
# stream = Stream(auth=api.auth, listener=listener)
# try:
#     print('Start streaming.')
#     stream.sample(languages=['en'])
# except KeyboardInterrupt:
#     print("Stopped.")
# finally:
#     print('Done.')
#     stream.disconnect()
#     output.close()


#

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
