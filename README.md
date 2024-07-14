# Twitch Alert Light and Sound System

This project integrates Twitch alerts with a WiZ smart bulb and plays random sounds from a specified directory. When a new follower or subscriber alert is received, the bulb flashes and a random sound is played.

## Prerequisites

- Python 3.7 or higher
- A WiZ smart bulb, I chose the Philips Hue RGB A19 LED Smart Bulb
https://www.amazon.com/Philips-connected-2-Pack-Dimmable-equivalent/dp/B08W5GBCLB
- An active Twitch account with the necessary permissions
- `pygame` library for playing sounds
- `websockets` library for WebSocket communication
- `pywizlight` library for controlling WiZ smart bulbs

## Setup

### Install Required Libraries

```sh
pip install asyncio json websockets pywizlight pygame
```

### Configuration

Edit the `config.json` file in the project directory with the following format:

```json
{
    "auth_token": "YOUR AUTH TOKEN FROM TWITCH",
    "user_id": "USER ID FOR FOLLOWS",
    "bulb_ip": "SMARTBULB IP ADDRESS",
    "sound_dir": "DIRECTORY FOR SOUNDS"
}
```

Replace the placeholder values with your actual `auth_token`, `user_id`, `bulb_ip`, and `sound_dir`.

### Running the Script

Run the script using the following command:

```sh
python twitchflash.py
```

## How It Works

1. **Load Configuration**: The script reads the `auth_token`, `user_id`, `bulb_ip`, and `sound_dir` from the `config.json` file.
2. **Initialize Pygame**: Pygame is initialized to handle playing random sounds.
3. **Connect to Twitch WebSocket**: The script connects to the Twitch WebSocket server to listen for alerts.
4. **Handle Alerts**: When a follower or subscriber alert is received, a random sound from the specified directory is played, and the WiZ smart bulb flashes in a defined pattern.

## Functions

### `play_random_sound()`

- Selects a random `.mp3` file from the `sound_dir` directory and plays it using Pygame.

### `flash_light()`

- Controls the WiZ smart bulb to create a flashing effect. It first flashes to a super bright, cool white, then gradually dims to off, and finally returns to a warm white at 20% brightness.

### `handle_messages(websocket)`

- Handles incoming messages from the Twitch WebSocket. When an alert is received, it prints the alert type and either the follower's or subscriber's display name. It then calls `play_random_sound()` and `flash_light()`.

### `main()`

- Initializes the WiZ smart bulb, sets its initial state, and connects to the Twitch WebSocket server. It keeps trying to reconnect if the connection is lost.

## Error Handling

- The script includes basic error handling for exceptions when controlling the light and connecting to the WebSocket server.

## Notes

- Ensure the WiZ bulb IP address is correct and that the bulb is reachable on the network.
- The sound directory should contain `.mp3` files for the script to play.
- Modify the `config.json` file with the correct values for your setup.
- Defaults to a warm white to help streamers with camera lighting.
## License

This project is licensed under the MIT License.

---

Feel free to modify and enhance this project to suit your needs. If you encounter any issues or have suggestions, please open an issue or submit a pull request. Enjoy!
