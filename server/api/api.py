from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import os
import uvicorn
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

stories: List[ Dict[str, str] ] = []


def load_stories(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            stories = json.load(f)
            if isinstance(stories, list):
                return stories
            else:
                raise ValueError("JSON is not a list")
    except FileNotFoundError:
        print(f"File '{path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")
    except Exception as e:
        print(f"Error loading stories: {e}")
    return []

#test function
@app.get("/api/hello")
def hello():
    return {'message': 'Hi!'}


#return a list of all stories
@app.get("/api/all_stories")
def get_story_titles():
    return [{"id": story["id"], "title": story["title"], "emoji": story["emoji"]} for story in stories]


#return a specific story
@app.get("/api/story")
def get_story(title: str):
    for story in stories:
        if story["title"] == title:
            return story
    raise HTTPException(status_code=404, detail="Story not found")

#return a new game session
@app.get("/api/new_session")
def get_new_session(story: Dict[str, str]):
    return ""

if __name__ == "__main__":

    port = 3000

    stories = load_stories('server/stories/stories.json')

    print(stories)

    os.environ["APP_PORT"] = str(port)

    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)