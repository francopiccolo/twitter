import os
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import tweepy

def get_api():
    auth = tweepy.OAuthHandler(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)

def get_users_from_user_ids(user_ids, chunk_size=100):
    api = get_api()
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

def iterate_over_cursors(function, screen_name):
    cursor = -1
    data = []
    while cursor:
        partial_data, cursors = function(screen_name=screen_name, cursor=cursor)
        data.extend(partial_data)
        cursor = cursors[1]
    return data

def make_users_df(users, source_screen_name):
    important_attributes = ['screen_name', 'location', 'followers_count', 'friends_count', 'created_at', 'favourites_count', 'statuses_count']
    data = {k:[] for k in important_attributes}
    data['last_status'] = []
    for user in users:
        attributes = user._json
        for attribute in important_attributes:
            data[attribute].append(attributes[attribute])
        last_status = np.nan
        if 'status' in attributes:
            last_status = user.status.created_at
        
        data['last_status'].append(last_status)

    users_df = pd.DataFrame(data)
    users_df['friends_followers_ratio'] = users_df['friends_count'] / users_df['followers_count']
    users_df['time_processed'] = datetime.now(timezone.utc)
    users_df['days_since_last_status'] = (users_df['time_processed'] - users_df['last_status']).dt.days
    users_df['source_screen_name'] = source_screen_name
    return users_df