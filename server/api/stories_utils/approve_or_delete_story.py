import sys
import os
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from user_stories_utils import UserStories

user_stories = UserStories()
pending = user_stories.list_pending()

if not pending:
    print("No pending stories.")
    sys.exit(0)

parser = argparse.ArgumentParser(description="Approve or delete a pending story.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--delete", action="store_true", help="Delete a pending story")
group.add_argument("--approve", action="store_true", help="Approve a pending story")

args = parser.parse_args()

try:
    index = int(input("Which story index? "))
    if args.delete:
        user_stories.delete_pending_story(index)
    elif args.approve:
        user_stories.approve_story(index)
except (ValueError, IndexError) as e:
    print(f"Error: {e}")
