from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

stories: List[ Dict[str, str] ] = [
    {"emoji": "👀", "title": "First Story", "puzzle": "This is the first story.", "solution": "This is the first solution"},
    {"emoji": "🔥","title": "Second Story", "puzzle": "This is the second story.", "solution": "This is the second solution" }
]

#test function
@app.get("/api/hello")
def hello():
    return {'message': 'Hi!'}


#return a list of all stories
@app.get("/api/all_stories")
def get_story_titles():
    return [{"title": story["title"], "emoji": story["emoji"]} for story in stories]


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

if __name__ == "main":

    port = 3000

    os.environ["APP_PORT"] = str(port)

    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)