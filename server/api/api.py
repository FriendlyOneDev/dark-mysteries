from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional, Any
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



#class to store stories
class Stories:
    def __init__(self):
        self.stories: List[ Dict[str, Any] ] = []

    def load_stories(self, path: str):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.stories = data
                else:
                    raise ValueError("JSON is not a list")
        except FileNotFoundError:
            print(f"File '{path}' not found.")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON format: {e}")
        except Exception as e:
            print(f"Error loading stories: {e}")
        
    
    def get_all_stories(self) -> List[Dict[str, Any]]:
        print(self.stories)
        return [{"id": story["id"], "title": story["title"], "emoji": story["emoji"]} for story in self.stories]

    def find_story(self, key: str, value: Any) -> Dict[str, Any] | None:
        for story in self.stories:
            if story.get(key) == value:
                return story
        return None

all_stories = None

#test function
@app.get("/api/hello")
def hello():
    return {'message': 'Hi!'}

@app.on_event("startup")
def startup_event():
    global all_stories
    print("Loading stories...")
    all_stories = Stories()
    all_stories.load_stories("server/stories/stories.json")

#return a list of all stories
@app.get("/api/all_stories")
def get_story_titles():
    return all_stories.get_all_stories()


#return a specific story
@app.get("/api/story")
def get_story(id: int):
    story = all_stories.find_story("id", id)
    if story == None:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

#return a new game session
@app.get("/api/new_session")
def get_new_session(story: Dict[str, str]):
    return ""

if __name__ == "__main__":

    port = 3000

    os.environ["APP_PORT"] = str(port)

    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)