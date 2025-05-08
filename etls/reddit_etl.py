import praw
from praw import Reddit
import sys
from utils.constants import POST_FIELDS
import pandas as pd

def connect_reddit(client_id, client_secret, user_agent: str) -> Reddit:
    try: 
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            read_only=True
        )
        return reddit
    except Exception as e:
        print(e)
        sys.exit(1)
        
def extract_posts(reddit_instance: Reddit, subreddit: str, time_filter: str, limit=None) -> list:
    subreddit = reddit_instance.subreddit(subreddit)
    posts = subreddit.top(time_filter=time_filter, limit=limit)

    post_lists = []

    for post in posts:
        post_dict = vars(post)
        post = {key: post_dict[key] for key in POST_FIELDS}
        post_lists.append(post)

    return post_lists

def transform_data(post_df: pd.DataFrame) -> pd.DataFrame:
    post_df['id'] = post_df['id'].astype(str)
    post_df['subreddit'] = post_df['subreddit'].astype(str)
    post_df['title'] = post_df['title'].astype(str)
    post_df['author'] = post_df['author'].astype(str)
    post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s')
    post_df['score'] = post_df['score'].astype(int)
    post_df['upvote_ratio'] = post_df['upvote_ratio'].astype(int)

    return post_df

def load_data_to_csv(data: pd.DataFrame, path: str):
    data.to_csv(path, index=False)