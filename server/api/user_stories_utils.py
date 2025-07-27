import json
import os
from collections import OrderedDict


class UserStories:
    def __init__(
        self,
        stories_file="server/stories/stories.json",
        pending_stories_file="server/stories/pending_stories.json",
    ):
        self.stories_file = stories_file
        self.pending_stories_file = pending_stories_file
        self._initialize_json()
        print("UserStories initialized at", self.pending_stories_file)

    def _initialize_json(self):
        if not os.path.exists(self.pending_stories_file):
            with open(self.pending_stories_file, "w") as f:
                json.dump([], f)

    def _get_highest_id(self):
        with open(self.stories_file, "r") as f:
            stories = json.load(f)
            if not stories:
                return 0
            return max(story.get("id", -1) for story in stories)

    @staticmethod
    def reorder_story(story):
        keys = ["id", "emoji", "title", "puzzle", "solution", "author"]
        return OrderedDict((k, story.get(k)) for k in keys if k in story)

    def submit_story(self, story: dict):
        """
        input: {'emoji': '🗿', 'title': 'Title of the story', 'puzzle': 'Puzzle description. Why?', 'solution': 'Solution', 'author': 'testuser'}
        """
        with open(self.pending_stories_file, "r+") as f:
            try:
                pending = json.load(f)
            except json.JSONDecodeError:
                pending = []

            pending.append(story)
            f.seek(0)
            json.dump(pending, f, ensure_ascii=False)
            f.truncate()
        print(f"Story submitted: {story}")
        return {"message": "Story submitted for approval", "story": story}

    def approve_story(self, index):
        with open(self.pending_stories_file, "r+", encoding="utf-8") as pf:
            pending = json.load(pf)

            if index < 0 or index >= len(pending):
                raise IndexError("Invalid pending story index")

            story = pending.pop(index)

            pf.seek(0)
            json.dump(pending, pf, indent=2, ensure_ascii=False)
            pf.truncate()

        new_id = self._get_highest_id() + 1
        story["id"] = new_id
        story = self.reorder_story(story)

        if not os.path.exists(self.stories_file):
            approved = []
        else:
            with open(self.stories_file, "r", encoding="utf-8") as sf:
                approved = json.load(sf)

        approved.append(story)
        with open(self.stories_file, "w", encoding="utf-8") as sf:
            json.dump(approved, sf, indent=2, ensure_ascii=False)

        print(f"Story with id {new_id} approved and saved.")
        print(f"Story: {story}")
        print(f"Pending stories remaining: {len(pending)}")

    def delete_pending_story(self, index):
        with open(self.pending_stories_file, "r+", encoding="utf-8") as pf:
            try:
                pending = json.load(pf)
            except json.JSONDecodeError:
                raise ValueError("Pending stories file is corrupted or empty.")

            if index < 0 or index >= len(pending):
                raise IndexError("Invalid pending story index")

            removed_story = pending.pop(index)

            pf.seek(0)
            json.dump(pending, pf, indent=2, ensure_ascii=False)
            pf.truncate()

        print(f"Deleted pending story at index {index}: {removed_story['title']}")
        print(f"Pending stories remaining: {len(pending)}")

    def list_pending(self):
        with open(self.pending_stories_file, "r", encoding="utf-8") as f:
            pending = json.load(f)
            if not pending:
                print("No pending stories.")
                return []

            for i, story in enumerate(pending):
                print("-" * 40)
                print(
                    f"[{i}] {story.get('emoji', '')} {story.get('title', '')} by {story.get('author', 'Unknown')}"
                )
                print(f"Puzzle: {story.get('puzzle')}")
                print(f"Solution: {story.get('solution')}")

            print("-" * 40)
        return pending


if __name__ == "__main__":

    user_stories = UserStories()

    """
    # Submit
    user_stories.submit_story(
        {
            "emoji": "🗿",
            "title": "Title of the story",
            "puzzle": "Puzzle description. Why?",
            "solution": "Solution",
            "author": "testuser",
        }
    )

    user_stories.submit_story(
        {
            "emoji": "👀",
            "title": "Title of the second story",
            "puzzle": "Puzzle description. Why?",
            "solution": "Solution",
            "author": "testuser",
        }
    )

    user_stories.submit_story(
        {
            "emoji": "🗣️",
            "title": "Title of third story",
            "puzzle": "Puzzle description. Why?",
            "solution": "Solution",
            "author": "testuser",
        }
    )

    user_stories.list_pending()

    # Approve the second story in the pending list
    print(user_stories.approve_story(1))
    """

    # Remote approval of stories
    user_stories.list_pending()
    index = int(input("Approve which pending story? "))
    try:
        user_stories.approve_story(index)
    except IndexError as e:
        print(f"Error: {e}")
