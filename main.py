"""
Reddit Notification Forwarder

This script is for personal use only.
It will read my own Reddit inbox/notifications and forward
simple text alerts to a private Discord channel.

It does NOT:
- post or comment on Reddit
- upvote, downvote, or perform any automated actions
- store data about other users
"""

import os
import time
from typing import Optional

import praw       # pip install praw
import requests   # pip install requests


def get_reddit_client() -> praw.Reddit:
    """Create and return an authenticated Reddit client."""

    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent="personal-notification-forwarder (script)",
    )


def send_to_discord(message: str) -> None:
    """Send a simple text message to a Discord webhook."""
    webhook_url: Optional[str] = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return  # Webhook not configured yet

    try:
        requests.post(webhook_url, json={"content": message}, timeout=5)
    except Exception:
        # In this simple personal script we just ignore errors for now.
        pass


def check_notifications(reddit: praw.Reddit) -> None:
    """
    Check my own unread inbox items and (eventually) forward
    a short summary to Discord.

    The actual processing logic will be implemented later.
    """
    for item in reddit.inbox.unread(limit=10):
        # TODO: Build a short message (e.g., author, subreddit, link)
        # and call send_to_discord(message)
        #
        # Example placeholder:
        # message = f"New reply from u/{item.author} in r/{item.subreddit}"
        # send_to_discord(message)
        #
        # Mark as read after handling:
        # item.mark_read()
        pass


def main() -> None:
    reddit = get_reddit_client()

    # Simple polling loop. The interval can be adjusted as needed.
    while True:
        check_notifications(reddit)
        time.sleep(60)  # wait 60 seconds between checks


if __name__ == "__main__":
    main()
