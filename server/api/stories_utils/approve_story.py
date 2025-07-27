import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from user_stories_utils import UserStories

# Remote approval of submissions
user_stories = UserStories()
user_stories.list_pending()
index = int(input("Approve which pending story? "))
try:
    user_stories.approve_story(index)
except IndexError as e:
    print(f"Error: {e}")
