import asyncio
import websockets
import os
import sys
import json
import uuid
import re
from fastapi import WebSocket
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), timeout=10)


class GameSession:
    def __init__(self, websocket, situation, solution):
        self.websocket = websocket
        self.session_id = str(uuid.uuid4())[:8]
        self.situation = situation
        self.solution = solution
        self.active = True

        self.system_prompt = f"""
ROLE: You are the narrator for a mystery game.
RULES:
1. Players only know this situation: {self.situation}
2. You know this solution: {self.solution}
3. Players will ask yes/no questions to guess the solution
4. You must ONLY respond with:
   - "Yes" (if the answer is definitively yes)
   - "No" (if the answer is definitively no)
   - "Bad question" (if the question is not a yes/no question)
5. If the player's question demonstrates they've correctly guessed the solution:
   - Respond with: "CORRECT!"
6. NEVER reveal the solution unless rule #5 is triggered
7. NEVER explain your answers

Current game session begins NOW.
"""

        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "assistant",
                "content": "Understood. I will follow all rules strictly.",
            },
        ]

        print(
            f"Session {self.session_id} started - Situation: {self.situation[:50]}..."
        )

    async def send_message(self, content):
        print(f"Session {self.session_id} sending: {content}")
        if not self.active:
            return

        try:
            if not isinstance(content, str):
                raise TypeError(f"send_message expected str, got {type(content)}")
            await self.websocket.send_text(content)
        except Exception as e:
            print(f"Session {self.session_id} send error: {str(e)}")
            self.active = False

    @staticmethod
    def parse_answer(response_text):
        match = re.search(r"\b(Yes|No|Bad question)\b", response_text, re.IGNORECASE)
        if match:
            answer_raw = match.group(1).lower()
            if "bad" in answer_raw:
                return "bad"
            return answer_raw
        return "bad"

    @staticmethod
    def parse_solved(response_text):
        return "CORRECT!" in response_text

    async def handle_message(self, user_input):
        if not self.active:
            return

        user_input = user_input.strip()
        if not user_input.endswith("?"):
            user_input += "?"
        if not user_input:
            return

        self.messages.append({"role": "user", "content": user_input})

        try:
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=self.messages,
                    temperature=0.1,
                )
            except Exception as e:
                print(
                    f"Session {self.session_id} inner AI error:  {type(e).__name__}:{str(e)}",
                    flush=True,
                )

            response_text = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": response_text})

            answer = self.parse_answer(response_text)
            solved = self.parse_solved(response_text)

            result = {"answer": answer, "solved": solved}

            await self.send_message(json.dumps(result))

            if solved:
                print(f"Session {self.session_id} solved correctly!")
                self.active = False

        except Exception as e:
            print(f"Session {self.session_id} outer AI error: {str(e)}", flush=True)
            await self.send_message(json.dumps({"answer": "error", "solved": False}))
            self.active = False


#### Everything below this line is for testing purposes

# For testing purposes
MYSTERIES = [
    {
        "id": 0,
        "emoji": "💔",
        "title": "Tragic Duo",
        "situation": "Jack and Judy were lying on the floor dead. There was a puddle of water and broken glass on the floor. How did they die?",
        "solution": "Jack and Judy were goldfish. They died because their bowl broke.",
    },
    {
        "id": 1,
        "emoji": "❄️",
        "title": "A Cold Drink",
        "situation": "Two men walk into a restaurant. The waiter brings them both beverages. The beverages are the same. One man drinks his glass down right away, and nothing bad happens to him. The other man takes his time and drinks slowly. He dies. Why?",
        "solution": "There was poison in ice cubes. The first man drank it down before the ice had a chance to melt.",
    },
    {
        "id": 2,
        "emoji": "🔫",
        "title": "The Polite Gunman",
        "situation": "A man walks into a restaurant and orders a glass of water. The waiter pulls a gun out and points it at the man. The man thanks the waiter and walks out of the restaurant.",
        "solution": "The man had the hiccups, and waiter saw it and scared them out of him.",
    },
]


# For testing purposes
async def handle_client(websocket):  # Currently selects random
    import random

    mystery = random.choice(MYSTERIES)

    session = GameSession(websocket, mystery["situation"], mystery["solution"])

    try:
        await session.send_message(f"Situation: {session.situation}")
        await session.send_message(
            "Ask yes/no questions to solve the mystery. Send 'quit' to exit."
        )

        async for message in websocket:
            await session.handle_message(message)
            if not session.active:
                break

    except websockets.exceptions.ConnectionClosed:
        print(f"Session {session.session_id} disconnected")
    except Exception as e:
        print(f"Session {session.session_id} error: {str(e)}")
    finally:
        session.active = False
        print(f"Session {session.session_id} ended")


# For testing purposes
async def start_server():
    async with websockets.serve(
        handle_client,
        "localhost",
        8765,
        max_size=2**20,
        ping_interval=20,
        ping_timeout=60,
    ):
        print("WebSocket server started at ws://localhost:8765")
        print(f"Loaded {len(MYSTERIES)} mysteries")
        await asyncio.Future()


# For testing purposes
def run_server():
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\nServer stopped gracefully")
    except Exception as e:
        print(f"Server error: {str(e)}")


# For testing purposes
if __name__ == "__main__":
    run_server()
