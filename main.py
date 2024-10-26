import discord
import json
import websockets
import asyncio
import os

class MessageSnapshot:
    """Represents a message snapshot for forwarded messages."""

    def __init__(self, data):
        self.type = data.get('type')
        self.content = data.get('content')
        self.embeds = data.get('embeds', [])
        self.attachments = data.get('attachments', [])
        self.created_at = data.get('timestamp')
        self.flags = data.get('flags')
        self.stickers = data.get('stickers', [])
        self.components = data.get('components', [])

    def __repr__(self):
        return f"<MessageSnapshot type={self.type!r} created_at={self.created_at!r} content={self.content!r}>"

class ForwardedMessageBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as Forwards admin')
        asyncio.create_task(self.connect_to_websocket())

    async def connect_to_websocket(self):
        # Connect directly to the Discord WebSocket
        async with websockets.connect('wss://gateway.discord.gg/?v=10&encoding=json') as ws:
            # Identify with the WebSocket using your bot token
            await ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": "TOKEN",
                    "intents": 32767,
                    "properties": {
                        "$os": "linux",
                        "$browser": "disco",
                        "$device": "disco"
                    }
                }
            }))

            while True:
                message = await ws.recv()
                data = json.loads(message)
                
                # Look for MESSAGE_CREATE event
                if data['t'] == "MESSAGE_CREATE":
                    message_data = data['d']
                    
                    # Ensure message is from a guild, not a DM
                    if 'guild_id' in message_data and 'message_snapshots' in message_data:
                        snapshots = message_data['message_snapshots']
                        file_content = json.dumps({"message_snapshots": snapshots}, indent=4)
                        
                        # Write JSON to file
                        with open("deleted.json", "w") as f:
                            f.write(file_content)

                        # Send file to specified channel
                        await self.send_deleted_file()

                        # Delete the message
                        await self.delete_message(message_data['channel_id'], message_data['id'])

    async def send_deleted_file(self):
        # Send `deleted.json` to the specific channel
        channel = self.get_channel(<channel_id>)
        if channel:
            await channel.send(file=discord.File("deleted.json"))
            os.remove("deleted.json")  # Clean up file after sending

    async def delete_message(self, channel_id, message_id):
        channel = await self.fetch_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.delete()

client = ForwardedMessageBot(intents=discord.Intents.all())
client.run(TOKEN)
