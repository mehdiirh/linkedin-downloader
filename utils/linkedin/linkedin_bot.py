from linkedin_messaging import ChallengeException, LinkedInMessaging
from linkedin_messaging.api_objects import RealTimeEventStreamEvent

from utils.linkedin import event_handlers
from utils.linkedin.tools import accept_all_invitations
from utils.event_objects import TabBadges

import settings

from pathlib import Path
import asyncio
import logging

cookie_path = Path(__file__).parent.joinpath("cookies.pickle")

config = settings.LINKEDIN
username = config["USER"]
password = config["PASS"]

logging.basicConfig()
logging.getLogger().setLevel(logging.WARNING)


async def start(bot):
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

    async def all_events(event: dict):
        event_payload = event.get("com.linkedin.realtimefrontend.DecoratedEvent", {}).get(
            "payload", {}
        )

        if event_payload.get("tabBadges") is not None:
            await event_handlers.handle_badge_events(TabBadges.from_dict(event_payload))

    async def on_event(event: RealTimeEventStreamEvent):
        await event_handlers.handle_message_events(event, bot)

    messaging.add_event_listener("event", on_event)
    messaging.add_event_listener("ALL_EVENTS", all_events)

    listener_task = asyncio.create_task(messaging.start_listener())
    invite_acceptor_task = asyncio.create_task(accept_all_invitations())

    # wait basically forever
    await asyncio.sleep(2 ** 128)
    await asyncio.gather(listener_task, invite_acceptor_task)
    await messaging.close()
