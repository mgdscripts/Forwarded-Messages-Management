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
