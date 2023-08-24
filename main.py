#  Deletes posts and/or comments from specified subreddit, or all of reddit

import praw
import json


def delete_content(content_type, subreddit=None):
    with open("credentials.json", "r") as f:
        credentials = json.load(f)

    reddit = praw.Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        username=credentials["username"],
        password=credentials["password"],
        user_agent="delete_content",
    )

    if subreddit == "allposts":
        subreddit = None

    def delete_posts():
        while True:
            posts = list(reddit.user.me().submissions.new(limit=None))
            if not posts:
                break
            for post in posts:
                if subreddit is None or post.subreddit.display_name == subreddit:
                    print(f"Deleting post {post.id}")
                    post.delete()

    def delete_comments():
        while True:
            comments = list(reddit.user.me().comments.new(limit=None))
            if not comments:
                break
            for comment in comments:
                if subreddit is None or comment.subreddit.display_name == subreddit:
                    print(f"Deleting comment {comment.id}")
                    comment.delete()

    if content_type == "posts" or content_type == "both":
        delete_posts()
    if content_type == "comments" or content_type == "both":
        delete_comments()


if __name__ == "__main__":
    while True:
        content_type = input("Enter what you want to delete (posts, comments, both): ")
        if content_type.lower() == "exit":
            print("Program terminated.")
            break
        subreddit = input(
            "Enter the subreddit you want to delete your content from, or 'allposts' to delete all: "
        )
        delete_content(content_type, subreddit)
