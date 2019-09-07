import decimal
import sys
import tweepy
import json

from chalice import Chalice
import boto3
from boto3.dynamodb.conditions import Key, Attr

app = Chalice(app_name='soul-stone')

customerKey = "ddd"
customerSecret = "ddd"
accessToken = "ddd"
accessSecret = "T"
aws_access_key_id = 'AV'
aws_secret_access_key = "ddd"

session = boto3.Session(region_name='ap-southeast-1', aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)

TRACK = ['#python']
# expires_after_days = 30
# # oauth = OAuth(accessToken, accessSecret, customerKey, customerSecret)
# stream = TwitterStream(auth=oauth)

ddb = session.resource('dynamodb')
table = ddb.Table('thanos')


class DynamoStreamListener(tweepy.StreamListener):
    """ A listener that continuously receives tweets and stores them in a
        DynamoDB database.
    """

    def __init__(self, api, table):
        super(tweepy.StreamListener, self).__init__()
        self.api = api
        self.table = table

    def on_status(self, status):

        data = status._json

        content = {}
        content['tweet_id'] = data['id']
        content['timestamp'] = int(data['timestamp_ms'])
        content['lang'] = data['lang']
        content['n_retweets'] = data['retweet_count']
        content['hastags'] = [
            x['text'] for x in data['entities']['hashtags'] if x['text']]
        content['user_mentions'] = [
            x['name'] for x in data['entities']['user_mentions'] if x['name']]
        content['urls'] = [x['url'] for x in data['entities']['urls'] if x['url']]
        content['text'] = data['text']
        content['user_id'] = data['user']['id']
        content['user_name'] = data['user']['name']
        content['coordinates'] = data['coordinates']

        print(content['text'] + '\n')

        try:
            self.table.put_item(Item=content)
        except Exception as e:
            print(str(e))

    def on_error(self, status_code):
        print('Encountered error with status code: {}'.format(status_code))
        return True  # Don't kill the stream

    def on_timeout(self):
        print('Timeout...')
        return True  # Don't kill the stream


response = table.query(
    KeyConditionExpression=Key('tweet_id').eq(2019)
)

for i in response['Items']:
    print(i['tweet_id'], ":", i['text'])

@app.route('/')
def main():
    # Connect to Twitter streaming API
    auth = tweepy.OAuthHandler(customerKey, customerSecret)
    auth.set_access_token(accessToken, accessSecret)
    api = tweepy.API(auth)
    # Instantiate DynamoStreamListener and pass it as argument to the stream
    sapi = tweepy.streaming.Stream(auth, DynamoStreamListener(api, table))
    # Get tweets that match one of the tracked terms
    sapi.filter(track=TRACK)





if __name__ == '__main__':
    main()


