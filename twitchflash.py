import asyncio
import json
import websockets
from pywizlight import wizlight, PilotBuilder
import os
import random
import pygame

# Load configuration from JSON file
with open('CONFIG FILE PATH HERE', 'r') as f:
    config = json.load(f)

AUTH_TOKEN = config["auth_token"]
USER_ID = config["user_id"]
BULB_IP = config["bulb_ip"]
SOUND_DIR = config["sound_dir"]

# We'll create the light object in the main coroutine
light = None

# Initialize pygame mixer
pygame.mixer.init()

def play_random_sound():
    sound_files = [f for f in os.listdir(SOUND_DIR) if f.endswith('.mp3')]
    if sound_files:
        random_sound = random.choice(sound_files)
        sound_path = os.path.join(SOUND_DIR, random_sound)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

async def flash_light():
    try:
        await asyncio.sleep(1)  # 1-second delay before light effect

        # Flash to super bright, cool white (high Kelvin)
        await light.turn_on(PilotBuilder(brightness=255, colortemp=6500))  # 6500K is very cool white
        await asyncio.sleep(0.1)  # Quick flash

        # Slightly dimmer but still very bright
        await light.turn_on(PilotBuilder(brightness=200, colortemp=6500))
        await asyncio.sleep(0.1)

        # Even dimmer
        await light.turn_on(PilotBuilder(brightness=150, colortemp=6500))
        await asyncio.sleep(0.1)

        # Fade to black over 2 seconds (increased from 1 second)
        for brightness in range(150, -4, -15):  # Changed step from -30 to -15
            await light.turn_on(PilotBuilder(brightness=max(0, brightness), colortemp=6500))
            await asyncio.sleep(0.1)  # Increased from 0.05 to 0.1

        # Ensure the light is off at the end
        await light.turn_off()
        
        # Return to 20% brightness with a warm color (2700K is a warm white)
        await light.turn_on(PilotBuilder(brightness=10, colortemp=2700))
    except Exception as e:
        print(f"Error controlling the light: {e}")

async def handle_messages(websocket):
    # Send the LISTEN message
    listen_message = {
        "type": "LISTEN",
        "data": {
            "topics": [f"alert-settings-update.{USER_ID}", f"activity-feed-alerts-v2.{USER_ID}"],
            "auth_token": AUTH_TOKEN
        },
        "nonce": "some_unique_string"
    }
    await websocket.send(json.dumps(listen_message))

    async for message in websocket:
        data = json.loads(message)
        
        if data["type"] == "MESSAGE":
            message_data = json.loads(data["data"]["message"])
            
            if message_data["type"] == "activity_feed_alerts_create":
                alert_data = message_data["data"]
                
                if alert_data["__typename"] == "ActivityFeedFollowAlert":
                    follower = alert_data["follower"]["displayName"]
                    print(f"New follower: {follower}")
                    play_random_sound()  # Play sound immediately
                    asyncio.create_task(flash_light())  # Create a new task for light control
                elif alert_data["__typename"] == "ActivityFeedSubscribeAlert":
                    subscriber = alert_data["subscriber"]["displayName"]
                    print(f"New subscriber: {subscriber}")
                # Add more alert types as needed

async def main():
    global light
    light = wizlight(BULB_IP)  # Initialize the light object

    # Set the light to 20% brightness with a warm color (2700K)
    await light.turn_on(PilotBuilder(brightness=10, colortemp=2700))

    uri = "wss://pubsub-edge.twitch.tv"  # This might need to be changed depending on your service
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                await handle_messages(websocket)
        except Exception as e:
            print(f"Error connecting to websocket: {e}")
        
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
