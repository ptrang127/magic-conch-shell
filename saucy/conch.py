import tweepy
import logging
import time
import configparser
from sassy import random_sass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):

    logger.info("Retrieving mentions")

    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id = since_id).items():

        new_since_id = max(tweet.id, new_since_id)

        if tweet.in_reply_to_status_id is not None:
            continue
        
        logger.info(f"The tweet content is {tweet.text}")
        logger.info(f"The tweet ID is {tweet.id}")
        logger.info(f"Answering to {tweet.user.screen_name}")

        userInfo = "@" + tweet.user.screen_name

        # if not following, follow the user
        if not tweet.user.following:
            tweet.user.follow()

        # if not favorited, favorite the tweet
        if not tweet.favorited:
            api.create_favorite(tweet.id)

        # reply to the tweet
        api.update_status(
            status= userInfo + " " + random_sass(),
            in_reply_to_status_id = tweet.id
        )
    return new_since_id

def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

    CONSUMER_KEY = config['AUTH']['consumer_key']
    CONSUMER_SECRET = config['AUTH']['consumer_secret']
    ACCESS_TOKEN = config['AUTH']['access_token']
    ACCESS_TOKEN_SECRET = config['AUTH']['access_token_secret']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    since_id = int(config['COMMON']['since_id'])
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")

        # update the .ini file
        config['COMMON']['since_id'] = str(since_id)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
            
        time.sleep(60)

if __name__ == "__main__":
    main()