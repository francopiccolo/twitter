import tweepy
import logging
from .utils import get_api, get_users_from_user_ids

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def unfollow_not_followers(api):
    followers_ids = [follower_id for follower_id in tweepy.Cursor(api.get_follower_ids).items()]
    logger.info(f'Number of followers {str(len(followers_ids))}')
    friends_ids = [friend_id for friend_id in tweepy.Cursor(api.get_friend_ids).items()]
    logger.info(f'Number of friends {str(len(friends_ids))}')
    threshold = 15000
    user_ids_to_unfollow = [user for user in friends_ids if user not in followers_ids]
    users_to_unfollow = get_users_from_user_ids(user_ids_to_unfollow)
    users_to_unfollow = [user for user in users_to_unfollow if user.followers_count < threshold]
    logger.info(f'Number of friends to unfollow {str(len(users_to_unfollow))}')
    for user in users_to_unfollow:
        logger.info(f'Unfollowing {user.screen_name}')
        api.destroy_friendship(screen_name=user.screen_name)

def main():
    api = get_api()
    unfollow_not_followers(api)

if __name__ == '__main__':
    main()