import os

API_KEY = os.environ('API_KEY')
API_SECRET = os.environ('API_SECRET')

CLIENT_ID = os.environ('CLIENT_ID')
CLIENT_SECRET = os.environ('CLIENT_SECRET')
USER_AGENT = 'script:reddit_etl:v1.0 (by u/Bubbly-Camera3338)'

POST_FIELDS = (
    'id',
    'subreddit',
    'title',
    'author',
    'created_utc',
    'score',
    'upvote_ratio'
)