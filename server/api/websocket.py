import asyncio
import websockets
import os
import sys
import json
import uuid
from fastapi import WebSocket
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


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

    async def handle_message(self, user_input):
        if not self.active:
            return

        user_input = user_input.strip()
        if not user_input:
            return

        if user_input.lower() == "quit":
            await self.send_message("Ending session. Goodbye!")
            self.active = False
            return

        print(f"Session {self.session_id} received: {user_input}")
        self.messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=self.messages,
                temperature=0.1,
            )
            response_text = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": response_text})

            if "CORRECT!" in response_text:
                await self.send_message("\n" + response_text)
                await self.send_message("\nCongratulations! You solved the mystery!")
                await self.send_message(f"The solution was: {self.solution}")
                print(f"Session {self.session_id} solved correctly!")
                self.active = False
                return

            trimmed = response_text.strip().split(".")[0].strip()
            await self.send_message(
                json.dumps({"role": "Narrator", "content": trimmed})
            )

        except Exception as e:
            print(f"Session {self.session_id} AI error: {str(e)}")
            await self.send_message("System error occurred. Please try again.")
            self.active = False


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
    {
        "id": 3,
        "emoji": "🏙️",
        "title": "The Rainy Day",
        "situation": "Mr. Smith lives on the 30th floor of his apartment building. Every day he takes the elevator down from his apartment to the lobby. After work, he takes the elevator from the lobby to the 15th floor and walks up the stairs the rest of the way. On rainy days he takes the elevator all the way from the lobby to the 30th floor. Why?",
        "solution": " Mr. Smith is a short. He can`t usually reach the button to the 30th floor. On rainy days he has his umbrella with him and pushes the button with it.",
    },
    {
        "id": 4,
        "emoji": "🎩",
        "title": "A Shouting Man`s Despair",
        "situation": "A car stops in front of a hotel. A man turns to his wife and shouts 'I`m ruined!' Why?",
        "solution": "The man and his wife were playing monopoly, and the man`s piece landed on a property with a hotel on it.",
    },
    {
        "id": 5,
        "emoji": "🏔️",
        "title": "27 Silent Souls",
        "situation": "There are 27 people in a cabin on a mountain. The windows and doors are all locked, but everyone inside is dead. What happened?",
        "solution": "The cabin is an airplane cabin that crashed on a mountain.",
    },
    {
        "id": 6,
        "emoji": "🕊️",
        "title": "The Deadly Sighting",
        "situation": "An avid birdwatcher sees an unexpected bird. Soon he`s dead. What happened?",
        "solution": "The birdwatcher was flying in a plane. The bird got stuck in the plane`s engine and made the plane crash.",
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
