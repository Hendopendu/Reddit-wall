import praw
import json
from datetime import datetime
import os
from dotenv import load_dotenv







load_dotenv()


# Reddit API Configuration
# Get these from: https://reddit.com/prefs/apps
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "reddit_wall_app/1.0"

# Filter Configuration
SUBREDDIT = "kanye"
INCLUDE_KEYWORD = "drive slow"  # Must contain this
EXCLUDE_KEYWORDS = ["V2", "Donda 2", "Vultures"]  # Must NOT contain these
POST_LIMIT = 50  # Fetch this many, then filter down
DISPLAY_LIMIT = 10  # Show this many after filtering

def fetch_and_filter_posts():
    """Fetch posts from r/kanye and filter by keywords"""
    
    # Initialize Reddit API
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    
    subreddit = reddit.subreddit(SUBREDDIT)
    filtered_posts = []
    
    # Fetch recent posts
    for post in subreddit.new(limit=POST_LIMIT):
        # Combine title and selftext for searching
        text_content = f"{post.title} {post.selftext}".lower()
        
        # Check if includes required keyword
        if INCLUDE_KEYWORD.lower() not in text_content:
            continue
        
        # Check if contains excluded keywords
        if any(exclude.lower() in text_content for exclude in EXCLUDE_KEYWORDS):
            continue
        
        # Post passed filters
        filtered_posts.append({
            'title': post.title,
            'author': str(post.author),
            'text': post.selftext,
            'score': post.score,
            'url': f"https://reddit.com{post.permalink}",
            'created': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Stop if we have enough
        if len(filtered_posts) >= DISPLAY_LIMIT:
            break
    
    return filtered_posts

if __name__ == "__main__":
    # Test the fetcher
    posts = fetch_and_filter_posts()
    print(f"Found {len(posts)} filtered posts:")
    for post in posts:
        print(f"\n- {post['title']}")
        print(f"  by u/{post['author']} | Score: {post['score']}")