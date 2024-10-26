
# Forwarded Message Bot for Discord

The **Forwarded Message Bot** connects directly to Discord’s WebSocket gateway to capture specific events, such as messages being deleted. This bot listens for any message delete events, takes a snapshot of those messages, logs the snapshots into a JSON file, and forwards that file to a specified channel.

## Key Features

- **Real-time Message Capture**: Connects to Discord’s WebSocket gateway to capture `MESSAGE_CREATE` events in real-time.
- **Message Snapshots**: Creates a snapshot of deleted messages, including message type, content, embeds, attachments, timestamps, and more.
- **Automatic File Management**: Saves snapshots to `deleted.json`, sends the file to a specified channel, and then deletes the file locally.

## Setup Instructions

### Prerequisites

- Python 3.8+
- `discord.py` for Discord interactions and `websockets` for direct gateway connections.

### Installation

1. Clone or download this repository.
2. Install the required libraries:
   ```bash
   pip install discord.py websockets
   ```

### Configuration

1. **Bot Token**: Replace `"TOKEN"` in the `connect_to_websocket` method with your actual bot token. For security, you may also store the token in a `.env` file.
2. **Channel ID**: Replace `<channel_id>` in the `send_deleted_file` method with the ID of the channel where you want to receive snapshots.
3. **Permissions**: Ensure your bot has `Manage Messages` permission in the guild to allow it to delete messages.

### Code Explanation

- **MessageSnapshot Class**: Stores the captured data from deleted messages.
- **WebSocket Connection**:
   - Connects directly to Discord’s WebSocket to receive real-time events.
   - Sends an `IDENTIFY` payload to authenticate with the bot token.
   - Listens specifically for the `MESSAGE_CREATE` event.
- **File Management**:
   - **Creating Snapshots**: When a deleted message is captured, the bot writes its data to `deleted.json`.
   - **Sending File**: The bot uploads `deleted.json` to a specified Discord channel.
   - **Cleanup**: After sending, it deletes `deleted.json` to avoid residual data.

### Usage

1. Start the bot:
   ```bash
   python forward_message_bot.py
   ```
2. The bot will connect to the WebSocket, monitor for message delete events, log snapshots, and send the data to your designated channel.

### Example Output

When a deleted message event is captured, an entry like the following will appear in `deleted.json`:
```json
{
    "message_snapshots": [
        {
            "type": 0,
            "content": "This is a sample message",
            "embeds": [],
            "attachments": [],
            "timestamp": "2023-10-01T12:34:56.789Z",
            "flags": 0,
            "stickers": [],
            "components": []
        }
    ]
}
```

---

This bot provides a streamlined way to capture and forward message snapshots, useful for server moderation and data logging.
```
