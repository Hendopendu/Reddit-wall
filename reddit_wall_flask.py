from flask import Flask, render_template_string
import praw
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Reddit API Configuration - REPLACE THESE
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "reddit_wall_app/1.0"

# Filter Configuration
SUBREDDIT = "kanye"
INCLUDE_KEYWORD = "ye"
EXCLUDE_KEYWORDS = ["V2", "Donda 2", "Vultures"]
POST_LIMIT = 50
DISPLAY_LIMIT = 10

# Global storage for posts
cached_posts = []

def fetch_and_filter_posts():
    """Fetch and filter posts from Reddit"""
    global cached_posts
    
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        
        subreddit = reddit.subreddit(SUBREDDIT)
        filtered = []
        
        for post in subreddit.new(limit=POST_LIMIT):
            text_content = f"{post.title} {post.selftext}".lower()
            
            if INCLUDE_KEYWORD.lower() not in text_content:
                continue
            
            if any(exclude.lower() in text_content for exclude in EXCLUDE_KEYWORDS):
                continue
            
            filtered.append({
                'title': post.title,
                'author': str(post.author),
                'text': post.selftext[:300] + ('...' if len(post.selftext) > 300 else ''),
                'score': post.score,
                'url': f"https://reddit.com{post.permalink}",
                'created': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            })
            
            if len(filtered) >= DISPLAY_LIMIT:
                break
        
        cached_posts = filtered
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetched {len(filtered)} posts")
    
    except Exception as e:
        print(f"Error fetching posts: {e}")

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>r/{{ subreddit }} Wall - "{{ keyword }}"</title>
    <meta http-equiv="refresh" content="300">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #1a1a1b;
            color: #d7dadc;
        }
        h1 {
            color: #ff4500;
            border-bottom: 2px solid #343536;
            padding-bottom: 10px;
        }
        .info {
            color: #818384;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .post {
            background: #1a1a1b;
            border: 1px solid #343536;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .post-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .post-title a {
            color: #d7dadc;
            text-decoration: none;
        }
        .post-title a:hover {
            color: #ff4500;
        }
        .post-meta {
            color: #818384;
            font-size: 13px;
            margin-bottom: 10px;
        }
        .post-text {
            color: #d7dadc;
            line-height: 1.5;
        }
        .score {
            color: #ff4500;
            font-weight: bold;
        }
        .no-posts {
            text-align: center;
            padding: 40px;
            color: #818384;
        }
    </style>
</head>
<body>
    <h1>r/{{ subreddit }} - "{{ keyword }}"</h1>
    <div class="info">
        Showing {{ post_count }} posts | Excluding: {{ excluded }} | Auto-refresh: 5 min | Last update: {{ last_update }}
    </div>
    
    {% if posts %}
        {% for post in posts %}
        <div class="post">
            <div class="post-title">
                <a href="{{ post.url }}" target="_blank">{{ post.title }}</a>
            </div>
            <div class="post-meta">
                u/{{ post.author }} | <span class="score">↑ {{ post.score }}</span> | {{ post.created }}
            </div>
            {% if post.text %}
            <div class="post-text">{{ post.text }}</div>
            {% endif %}
        </div>
        {% endfor %}
    {% else %}
        <div class="no-posts">
            No posts found matching filters. Check back later.
        </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(
        HTML_TEMPLATE,
        subreddit=SUBREDDIT,
        keyword=INCLUDE_KEYWORD,
        excluded=", ".join(EXCLUDE_KEYWORDS),
        posts=cached_posts,
        post_count=len(cached_posts),
        last_update=datetime.now().strftime('%H:%M:%S')
    )

if __name__ == '__main__':
    # Fetch posts immediately on startup
    print("Fetching initial posts...")
    fetch_and_filter_posts()
    
    # Schedule background fetching every 5 minutes
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_and_filter_posts, trigger="interval", minutes=5)
    scheduler.start()
    
    print("Starting Flask app on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    
    try:
        app.run(debug=True, use_reloader=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()