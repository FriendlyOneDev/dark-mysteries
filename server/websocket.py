import asyncio
import websockets
import os
import sys
import json
import uuid
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

MYSTERIES = [
    {
        "situation": "Sarah held a blade to Cillian's throat. Soon after Cillian gave all the money he had to Sarah.",
        "solution": "Sarah was Cillian's barber. She shaved his face and cut his hair. He knew how much it would cost so he brought just the exact amount of money needed to pay Sarah.",
    },
    {
        "situation": "A man walks into a bar and asks for a glass of water. The bartender pulls out a gun. The man says 'Thank you' and leaves.",
        "solution": "The man had hiccups. The bartender scared them away by pulling out the gun.",
    },
    {
        "situation": "A woman lives on the 20th floor. Every morning she takes the elevator down to the ground floor. When she returns, she can only take the elevator to the 15th floor and walks the rest of the way unless it's raining.",
        "solution": "The woman is too short to reach the button for the 20th floor. When it's raining, she uses her umbrella to press the button.",
    },
]


class GameSession:
    def init(self, websocket, situation, solution):
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
        if not self.active:
            return

        try:
            await self.websocket.send(content)
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

response_text = response_text.strip().split(".")[0].strip()
            await self.send_message(
                json.dumps({"role": "Narrator", "content": response_text})
            )

        except Exception as e:
            print(f"Session {self.session_id} AI error: {str(e)}")
            await self.send_message("System error occurred. Please try again.")
            self.active = False


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


# test server
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


def run_server():
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\nServer stopped gracefully")
    except Exception as e:
        print(f"Server error: {str(e)}")


if name == "main":
    run_server()