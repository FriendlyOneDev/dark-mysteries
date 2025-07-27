from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional, Any
import os
import uvicorn
import json
from websocket import GameSession
from auth import AuthService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# class to store stories
class Stories:
    def __init__(self):
        self.stories: List[Dict[str, Any]] = []

    def load_stories(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
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


@app.on_event("startup")
def startup_event():
    print("Loading stories...")
    all_stories.load_stories("server/stories/stories.json")


# test function
@app.get("/api/hello")
def hello():
    return {"message": "Hi!"}


# return a list of all stories
@app.get("/api/all_stories")
def get_story_titles():
    return all_stories.get_all_stories()


#return a specific story
@app.get("/api/story/{id}")
def get_story(id: int):
    story = all_stories.find_story("id", id)
    if story == None:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


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
