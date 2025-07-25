from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

stories = [
    {"title": "First Story", "content": "This is the first story."},
    {"title": "Second Story", "content": "This is the second story."}
]

#test function
@app.get("/api/hello")
def hello():
    return {'message': 'Hi!'}


#return a list of all stories
@app.get("/api/all_stories")
def get_stories():
    return stories


#return a specific story
@app.get("/api/story")
def get_story(title: str):
    for story in stories:
        if story["title"] == title:
            return story
    raise HTTPException(status_code=404, detail="Story not found")

if __name__ == "__main__":

    port = 3000

    os.environ["APP_PORT"] = str(port)

    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)