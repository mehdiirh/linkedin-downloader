from linkedin_messaging import ChallengeException, LinkedInMessaging
from linkedin_messaging.api_objects import RealTimeEventStreamEvent

from utils.linkedin import event_handlers

from pathlib import Path
import asyncio
import logging
import json

cookie_path = Path(__file__).parent.joinpath("cookies.pickle")
config_path = Path(__file__).resolve().parent.parent.parent / 'config.json'

config = json.load(open(config_path, 'r'))["LINKEDIN"]
username = config["USER"]
password = config["PASS"]

logging.basicConfig()
logging.getLogger().setLevel(logging.WARNING)


async def listen(bot):
    """
    Listen to events from the LinkedIn direct messages

    Args:
        bot (telethon.TelegramClient): Telegram client
    """

    print('Start listening to linkedin messages...')

    messaging = LinkedInMessaging()

    if cookie_path.exists():
        with open(cookie_path, "rb") as cf:
            messaging = LinkedInMessaging.from_pickle(cf.read())

    if not await messaging.logged_in():
        try:
            await messaging.login(username, password)
        except ChallengeException:
            await messaging.enter_2fa(input("Enter 2FA Code: "))

        with open(cookie_path, "wb+") as cf:
            cf.write(messaging.to_pickle())

    async def on_event(event: RealTimeEventStreamEvent):
        await event_handlers.handle_message_events(event, bot)

    messaging.add_event_listener("event", on_event)
    task = asyncio.create_task(messaging.start_listener())

    # wait basically forever
    await asyncio.sleep(2 ** 128)
    await asyncio.gather(task)
    await messaging.close()
