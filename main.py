import asyncio
import websockets
import json

players = {}  # websocket: role

async def handler(websocket):
    global players

    # ---- Assign Role ----
    if len(players) >= 2:
        await websocket.send(json.dumps({"type": "full"}))
        await websocket.close()
        return

    role = "A" if "A" not in players.values() else "B"
    players[websocket] = role

    await websocket.send(json.dumps({
        "type": "role",
        "role": role
    }))

    # If 2 players connected -> ready
    if len(players) == 2:
        for ws in players:
            await ws.send(json.dumps({"type": "ready"}))

    print(f"Player {role} connected")

    try:
        async for message in websocket:
            data = json.loads(message)

            # ---- Movement Sync ----
            if data["type"] == "move":
                # Broadcast to other player
                for ws in players:
                    if ws != websocket:
                        await ws.send(json.dumps({
                            "type": "move",
                            "player": players[websocket],
                            "x": data["x"]
                        }))

    except websockets.exceptions.ConnectionClosed:
        pass

    # ---- Remove player on disconnect ----
    print(f"Player {players[websocket]} disconnected")
    del players[websocket]

    # Notify remaining player
    for ws in players:
        await ws.send(json.dumps({"type": "opponent_left"}))


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Server running on ws://localhost:8765")
        await asyncio.Future()  # run forever


asyncio.run(main())