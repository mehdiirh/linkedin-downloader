from linkedin_api import Linkedin
from telethon.sync import TelegramClient

from utils.database.models import User
from utils.database.redis import Redis
from utils.event_objects import EventDetails, Invite
from utils.telegram.texts import LinkedinLinked, MediaCaption

import settings

import re
import asyncio
import random


async def extract_media(bot: TelegramClient, event: EventDetails):
    """
    Extract media from the event and send it to the user as a message

    Args:
        bot (TelegramClient): Telegram client
        event (EventDetails): Event details
    """

    with User() as db:
        if not (user := db.fetch(columns=['language', 'telegram_id'], linkedin_id=event.sender, size=1)):
            return

    lang = user[0] or 'en'
    telegram_id = user[1]

    caption = MediaCaption.get(lang).replace('%author%', event.author)

    message = await bot.send_message(telegram_id, f"{caption}"
                                                  f"\n-------------\n\n"
                                                  f"{event.text[:4000]} \n\n 👇👇👇👇")

    if images := event.media.images:
        [await bot.send_file(telegram_id, i, caption=caption, reply_to=message) for i in images]

    if videos := event.media.videos:
        [await bot.send_file(telegram_id, i.url, caption=caption, reply_to=message) for i in videos]

    if documents := event.media.documents:
        [await bot.send_file(telegram_id, i, caption=caption, reply_to=message) for i in documents]


async def authenticate(bot: TelegramClient, message: str, linkedin_id: str):
    """
    Authenticate the user with the given linkedin_id and code and sync it with their telegram account

    Args:
        bot (TelegramClient): Telegram client
        message (str): Message received from the user
        linkedin_id (str): LinkedIn ID of the user
    """

    if not re.match(r'^\d+:\w+$', message):
        return

    telegram_id, code = message.split(':')

    with User() as db:
        if user := db.fetch(columns='linkedin_id', telegram_id=telegram_id, size=1):
            if user[0]:
                return

        # if the LinkedIn account is already linked to another telegram account, unlink it
        if user := db.fetch(columns='telegram_id', linkedin_id=linkedin_id, size=1):
            if user[0]:
                db.update({'linkedin_id': None}, {'telegram_id': user[0]})

    redis = Redis()
    saved_code = redis.server.get(telegram_id)
    if saved_code is not None:
        saved_code = saved_code.decode('utf-8')

    if code == saved_code:
        with User() as db:
            db.update({'linkedin_id': linkedin_id}, filters={'telegram_id': telegram_id})
            lang = db.language(telegram_id)

        await bot.send_message(int(telegram_id), LinkedinLinked.get(lang))


async def accept_all_invitations():
    print('Invite acceptor started')

    api = Linkedin(
        settings.LINKEDIN['USER'],
        settings.LINKEDIN['PASS']
    )
    redis = Redis()
    invites_redis_key = 'linkedin:INV'

    while True:

        invite_count = 0
        if invitations := redis.server.get(invites_redis_key):
            invite_count = int(invitations.decode('utf8'))

        if not invite_count:
            # if no invitations exists in redis, sleep 1 minute, then check again
            await asyncio.sleep(60)
            continue

        # reset invite counts
        redis.server.set(invites_redis_key, 0)

        while True:
            invites = api.get_invitations(limit=10)

            if not invites:
                break  # exit if there's no more invitations

            for invite in invites:
                invite = Invite.from_dict(invite)

                if invite.invitation_type != 'PENDING':
                    continue

                api.reply_invitation(invite.entity_urn, invite.shared_secret, action='accept')

                # sleep 3 to 10 seconds between each invite accept
                await asyncio.sleep(
                    random.randint(3, 10)
                )

        await asyncio.sleep(15 * 60)  # sleep 15 minutes after accepting invitations
