import tweepy
import logging
from ..utils import create_api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def follow_followers(api):
    logger.info('Retrieving and following followers')
    for follower in tweepy.Cursor(api.get_followers, count=200).items(): # count 200 not helpful to reduce number of requests
        if not follower.following:
            logger.info(f'Following {follower.name}')
            follower.follow()

def main():
    api = create_api()
    while True:
        follow_followers(api)
        logger.info('Waiting...')
        time.sleep(60)

if __name__ == '__main__':
    main()