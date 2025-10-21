# Reddit Wall

A simple web application that displays filtered posts from Reddit subreddits in a real-time wall format.

## What This Does

Fetches posts from specified Reddit subreddits, filters them by keywords, and displays them on a clean web interface. Built as a learning project to understand API integration, web scraping basics, and Flask development.

## Disclaimer

This is a personal learning project. It uses Reddit's official API within their terms of service and rate limits. No data is stored permanently, manipulated, or used for any commercial purpose. All displayed content remains property of the original Reddit posters.

## Features

- Monitors specific subreddits (currently configured for r/kanye)
- Filters posts by include/exclude keywords
- Auto-refreshes every 5 minutes
- Clean, Reddit-themed dark UI
- Text-only display (no media)

## Tech Stack

- Python 3.8+
- Flask (web framework)
- PRAW (Reddit API wrapper)
- APScheduler (background task scheduling)

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
   pip install praw flask apscheduler python-dotenv
```
4. Create a Reddit app at https://reddit.com/prefs/apps
   - Choose "script" type
   - Note your client_id and client_secret

5. Create a `.env` file in the project root:
```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=reddit_wall_app/1.0
```

6. Run the application:
```bash
   python reddit_wall_flask.py
```

7. Open browser to `http://127.0.0.1:5000`

## Configuration

Edit the following variables in `reddit_wall_flask.py`:

- `SUBREDDIT`: Which subreddit to monitor
- `INCLUDE_KEYWORD`: Posts must contain this phrase
- `EXCLUDE_KEYWORDS`: Posts containing these are filtered out
- `DISPLAY_LIMIT`: Number of posts to show

## Learning Outcomes

Built this to learn:
- REST API integration with proper authentication
- Environment variable management for sensitive data
- Background task scheduling in web apps
- Basic Flask routing and templating
- Virtual environment best practices

## Notes

- Rate limited to Reddit's free tier restrictions (100 requests/minute)
- Not intended for production use
- Educational project only
- Respects Reddit's API terms of service

## License

MIT - Feel free to learn from this, but use responsibly.