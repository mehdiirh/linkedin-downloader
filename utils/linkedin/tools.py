from utils.database.models import User
from utils.database.redis import Redis
from utils.event_objects import EventDetails
from utils.telegram.texts import LinkedinLinked, MediaCaption

from telethon.sync import TelegramClient


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
                                                  f"_____________\n\n"
                                                  f"{event.text[:4000]} \n\n 👇👇👇👇")

    if images := event.media.images:
        [await bot.send_file(telegram_id, i, caption=caption, reply_to=message) for i in images]

    if videos := event.media.videos:
        [await bot.send_file(telegram_id, i.url, caption=caption, reply_to=message) for i in videos]

    if documents := event.media.documents:
        [await bot.send_file(telegram_id, i, caption=caption, reply_to=message) for i in documents]


async def authenticate(bot: TelegramClient, code: str, linkedin_id: str):
    """
    Authenticate the user with the given linkedin_id and code and sync it with their telegram account

    Args:
        bot (TelegramClient): Telegram client
        code (str): Code received from the user
        linkedin_id (str): LinkedIn ID of the user
    """

    telegram_id, code = code.split(':')

    with User() as db:
        if user := db.fetch(columns='linkedin_id', telegram_id=telegram_id, size=1):
            if user[0]:
                return

    redis = Redis()
    saved_code = redis.server.get(telegram_id)
    if saved_code is not None:
        saved_code = saved_code.decode('utf-8')

    if code == saved_code:
        with User() as db:
            db.update({'linkedin_id': linkedin_id}, filters={'telegram_id': telegram_id})
            lang = db.language(telegram_id)

        await bot.send_message(int(telegram_id), LinkedinLinked.get(lang))
