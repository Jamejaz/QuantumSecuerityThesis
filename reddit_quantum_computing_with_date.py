import praw
import csv
import time
from datetime import datetime, UTC  # ✅ Use timezone-aware UTC

# Reddit API credentials
CLIENT_ID = 'Hr81PmH7-4AM3eTJh0M8qA'  # Replace with your client_id
CLIENT_SECRET = 'dQiP1eT233qqi9bKM_EurtXrkZVeLw'  # Replace with your client_secret
USER_AGENT = 'yowindows:DataMiner:v1.0 (by u/This_Hawk_6906)'  # Replace with your user_agent

# PRAW instance
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Subreddit and scrape settings
SUBREDDIT = "Qiskit"  # Ensure correct format
LIMIT = 5000  # Maximum posts to retrieve
COMMENTS_LIMIT = 2  # Max number of comments per post

def convert_utc_to_datetime(utc_timestamp):
    """
    Convert UTC timestamp to a human-readable datetime string using timezone-aware objects.
    """
    return datetime.fromtimestamp(utc_timestamp, UTC).strftime('%Y-%m-%d %H:%M:%S UTC')  # ✅ Fixed

def scrape_reddit():
    """
    Scrapes the Reddit subreddit and retrieves post data, including comments and question text.
    """
    try:
        subreddit = reddit.subreddit(SUBREDDIT)
        posts = []
        
        # Fetching newest posts up to LIMIT
        for submission in subreddit.new(limit=LIMIT):  
            # Fetch the top-level comments
            submission.comments.replace_more(limit=0)  # Load all top-level comments
            top_comments = []
            for comment in submission.comments.list()[:COMMENTS_LIMIT]:  # Limit to top N comments
                top_comments.append(comment.body)
            
            # Combine comments into a single string, separated by "|"
            comments_text = " | ".join(top_comments)

            # Convert post time from UTC to readable format
            post_time = convert_utc_to_datetime(submission.created_utc)

            post_data = {
                "title": submission.title,
                "text": submission.selftext,  # Add post text
                "score": submission.score,
                "num_comments": submission.num_comments,
                "time": post_time,  # ✅ Add post time
                "url": submission.url,
                "comments": comments_text  # Store comments in a single field
            }
            posts.append(post_data)
        
        print(f"Total posts scraped: {len(posts)}")  # Debugging: check number of posts
        return posts
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def export_data():
    """
    Scrapes Reddit and exports data to a CSV file, including comments and question text.
    """
    data = scrape_reddit()
    if not data:
        print("No data scraped.")
        return

    print("Sample data:", data[:5])  # Debugging: Print sample of scraped data

    with open("reddit_quantum_computing_with_date_1.csv", "w", newline='', encoding='utf-8') as data_file:
        fieldnames = ["title", "text", "score", "num_comments", "time", "url", "comments"]  # ✅ Updated fieldnames
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)
    
    print("Data saved successfully to reddit_quantum_computing_final.csv")

if __name__ == "__main__":
    export_data()
