from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
import os
import uvicorn
import json
from websocket import GameSession
from auth import AuthService
from user_stories_utils import UserStories

app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), "../static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../static/assets")),
    name="assets",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# User submission stuff
user_stories = UserStories()


# Auth stuff
auth_service = AuthService()
app.include_router(auth_service.get_router())


# class to store stories
class Stories:
    def __init__(self):
        self.stories: List[Dict[str, Any]] = []

    def load_stories(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON is not a list")
                if not data:
                    print("Warning: stories.json is empty!")
                self.stories = data
                print(f"Successfully loaded {len(data)} stories")
        except Exception as e:
            print(f"Error loading stories: {e}")

    def get_all_stories(self) -> List[Dict[str, Any]]:
        print(self.stories)
        return [
            {"id": story["id"], "title": story["title"], "emoji": story["emoji"]}
            for story in self.stories
        ]

    def find_story(self, key: str, value: Any) -> Dict[str, Any] | None:
        for story in self.stories:
            if story.get(key) == value:
                return story
        return None


all_stories = Stories()

sessions: Dict[str, GameSession] = {}


@app.get("/")
async def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "../static/index.html"))


@app.on_event("startup")
def startup_event():
    try:
        print("Loading stories...")
        all_stories.load_stories("server/stories/stories.json")
        if not all_stories.stories:
            print("Warning: No stories loaded!")
    except Exception as e:
        print(f"Failed to load stories: {e}")


# test function
@app.get("/api/hello")
def hello():
    return {"message": "Hi!"}


# return a list of all stories
@app.get("/api/all_stories")
def get_story_titles():
    return all_stories.get_all_stories()


# return a specific story
@app.get("/api/story/{id}")
def get_story(id: int):
    story = all_stories.find_story("id", id)
    if story == None:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


# Story submission model
class StorySubmission(BaseModel):
    emoji: str
    title: str
    puzzle: str
    solution: str
    author: str


# sunmit a new story
@app.post("/api/submit_story")
def submit_story(submission: StorySubmission):
    story = submission.dict()
    result = user_stories.submit_story(story)
    return result


# return a new game session
@app.websocket("/ws/{story_id}")
async def websocket_endpoint(websocket: WebSocket, story_id: int):
    await websocket.accept()

    story = all_stories.find_story("id", story_id)
    if story is None:
        await websocket.close(code=1008, reason="Story not found")
        return

    session = GameSession(websocket, story["puzzle"], story["solution"])
    sessions[session.session_id] = session

    try:
        await websocket.send_text(f"Situation: {session.situation}")
        await websocket.send_text("Ask yes/no questions to solve the mystery.")

        while session.active:
            data = await websocket.receive_text()
            await session.handle_message(data)

    except WebSocketDisconnect:
        print(f"Client disconnected from session {session.session_id}")
    except Exception as e:
        print(f"Error in WebSocket: {str(e)}")
    finally:
        if session.session_id in sessions:
            del sessions[session.session_id]
        await websocket.close()


if __name__ == "__main__":
    port = 3000
    os.environ["APP_PORT"] = str(port)
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)
