import tweepy
from utils.twitter import get_api as get_twitter_api
from utils.twitter import get_users_from_user_ids
from utils.gs import get_client as get_gs_client

if __name__ == '__main__':
    gs_client = get_gs_client()
    twitter_api = get_twitter_api()

    spreadsheet = gs_client.open('Twitter bot')
    accounts = spreadsheet.worksheet('accounts').col_values(1)[1:]
    friends_sheet = spreadsheet.worksheet('friends')
    stored_friends_ids = [[friend_id] for friend_id in friends_sheet.col_values(1)][1:]
    
    all_friend_ids = []
    for account in accounts:
        all_friend_ids.extend([friend_id for friend_id in tweepy.Cursor(twitter_api.get_friend_ids, screen_name='janehk').items()])

    friends = get_users_from_user_ids(all_friend_ids)
    friends_rows = [[friend.id, friend.screen_name] for friend in friends]
    friends_sheet.append_rows(friends_rows)