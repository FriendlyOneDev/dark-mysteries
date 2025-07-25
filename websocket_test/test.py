import asyncio
import websockets


async def websocket_handler(websocket):
    # Функція, що обробляє підключення веб-сокету
    while True:
        message = await websocket.recv()
        # Отримання повідомлення від клієнта
        print(f"Отримано повідомлення: {message}")

        response = f"Ви сказали: {message}"
        await websocket.send(response)
        # Надсилання відповіді клієнту


async def main():
    async with websockets.serve(websocket_handler, "localhost", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
