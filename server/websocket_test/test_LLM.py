import asyncio
import websockets
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

situation = "Sarah held a blade to Cillian's throat. Soon after Cillian gave all the money he had to Sarah."
solution = "Sarah was Cillian's barber. She shaved his face and cut his hair. He knew how much it would cost so he brought just the exact amount of money needed to pay Sarah."

system_prompt = f"""
ROLE: You are the narrator for a mystery game.
RULES:
1. Players only know this situation: {situation}
2. You know this solution: {solution}
3. Players will ask yes/no questions to guess the solution
4. You must ONLY respond with:
   - "Yes" (if the answer is definitively yes)
   - "No" (if the answer is definitively no)
   - "Not relevant" (if the question doesn't help solve the mystery, or is not related to the situation at all)
   - "Bad question" (if the question is not a yes/no question)
5. If the player's question demonstrates they've correctly guessed the solution:
   - Respond with: "CORRECT!"
6. NEVER reveal the solution unless rule #5 is triggered
7. NEVER explain your answers

Current game session begins NOW.
"""


async def handle_chat(websocket):
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "assistant",
            "content": "Understood. I will follow all rules strictly.",
        },
    ]

    try:
        await websocket.send(f"Situation: {situation}")
        await websocket.send(
            "Ask yes/no questions to solve the mystery. Send 'quit' to exit."
        )

        while True:
            try:
                user_input = (await websocket.recv()).strip()

                if not user_input:
                    continue

                messages.append({"role": "user", "content": user_input})

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.1,
                )

                response_text = response.choices[0].message.content
                messages.append({"role": "assistant", "content": response_text})

                if "CORRECT!" in response_text:
                    await websocket.send("\n" + response_text)
                    await websocket.send("\nCongratulations! You solved the mystery!")
                    await websocket.send(f"The solution was: {solution}")
                    break

                await websocket.send(response_text.strip().split(".")[0].strip())

            except websockets.exceptions.ConnectionClosed:
                print("Client disconnected unexpectedly")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                await websocket.send(f"Error occurred: {str(e)}")
                break

    except Exception as e:
        print(f"Connection error: {str(e)}")
    finally:
        print("Client session ended")


async def websocket_handler(websocket):
    await handle_chat(websocket)


async def start_server():
    async with websockets.serve(websocket_handler, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()  # Run forever


def run_server():
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\nServer stopped by user")


if __name__ == "__main__":
    run_server()
