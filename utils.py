import os
import tweepy

def get_api():
    auth = tweepy.OAuthHandler(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)

def get_users_from_user_ids(user_ids, chunk_size=100):
    num_users = len(user_ids)
    start_idx = 0
    end_idx = chunk_size
    users = []
    keep = True
    while keep:
        if end_idx > num_users:
            end_idx = num_users
            keep = False
        users.extend(api.lookup_users(user_id=user_ids[start_idx:end_idx]))
        start_idx += chunk_size
        end_idx += chunk_size
    return users