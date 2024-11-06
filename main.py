import discord
import json
import aiohttp
import os

intents = discord.Intents.all()
client = discord.Client(intents=intents)

TOKEN =
GUILD_ID_1 = 
GUILD_ID_2 = 
CHANNEL_ID_GUILD_2 = 
CHANNEL_ID_TO_SEND = 

@client.event
async def on_ready():
    print("Bot is ready and logged in as Forwards admin")

@client.event
async def on_message(message):
    # Ignore messages from the bot itself, other bots, and webhooks
    if message.author.bot or message.webhook_id:
        return

    # Check if message is from the specified servers and channel
    if (message.guild.id == GUILD_ID_1) or (message.guild.id == GUILD_ID_2 and message.channel.id == CHANNEL_ID_GUILD_2):
        # Define API endpoint to get the last 5 messages in the channel
        url = f'https://discord.com/api/v9/channels/{message.channel.id}/messages?limit=5'
        headers = {
            'Authorization': f'Bot {TOKEN}',
            'Content-Type': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    # Find the specific message by ID and check for 'message_snapshots'
                    target_message = next((msg for msg in data if msg['id'] == str(message.id)), None)
                    if target_message and 'message_snapshots' in target_message:
                        snapshots = target_message['message_snapshots']
                        file_content = json.dumps({"message_snapshots": snapshots}, indent=4)

                        # Save the snapshot data to a file
                        with open("deleted.json", "w") as f:
                            f.write(file_content)

                        # Send the file to the specified channel
                        send_channel = client.get_channel(CHANNEL_ID_TO_SEND)
                        if send_channel:
                            await send_channel.send(file=discord.File("deleted.json"))
                            os.remove("deleted.json")  # Clean up the file after sending

                        # Delete the original message
                        message_to_delete = await message.channel.fetch_message(target_message['id'])
                        await message_to_delete.delete()
                else:
                    print(f"Failed to fetch messages. Status: {response.status}")

client.run(TOKEN)
