#!./venv/bin/python

from utils.telegram.login import get_bot
from utils.telegram import keyboards, texts
from utils.telegram.types import *

from utils.linkedin import linkedin_bot

from utils.tools import now, generate_unique_id

from utils.database.models import User
from utils.database.redis import Redis

from telethon.sync import events
from telethon.tl.types import User as UserType

import logging
import asyncio
import datetime

# =================  CONFIGURE  ================= #
tz = datetime.timezone.utc
bot = get_bot()
logging.basicConfig(
    filename='log.log',
    filemode='a',
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d - %H:%M:%S',
    level=logging.WARNING)

print('TELEGRAM BOT STARTED')


# =================  CONFIGURE  ================= #


@bot.on(events.NewMessage(incoming=True))
async def validate_user(message: Message):

    sender_id = message.sender_id

    with User() as db:
        if db.fetch(telegram_id=sender_id, size=1):
            db.update({'last_activity': now()}, {'telegram_id': sender_id})

        else:
            db.create(sender_id)


@bot.on(events.NewMessage(incoming=True, pattern=r'^/language$'))
async def set_language(message: Message):

    await message.respond(
        f'Please select your preferred language 👇:',
        buttons=keyboards.SET_LANG
    )

    raise events.StopPropagation


@bot.on(events.NewMessage(incoming=True))
async def check_language(message: Message):

    sender: UserType = await message.get_sender()

    with User() as db:
        if not db.language(sender.id):
            await message.respond(
                f'Hello {sender.first_name} !\n'
                f'Welcome to Downloadin Bot.\n\n'
                f'Please select your preferred language 👇:',

                buttons=keyboards.SET_LANG
            )

            conv: Conversation
            async with bot.conversation(sender, timeout=None) as conv:
                while True:
                    call: CallbackQuery = await conv.wait_event(events.CallbackQuery())
                    if call.sender_id == sender.id:
                        data: str = call.data.decode('utf-8')
                        action, value = data.split('::')
                        if action == 'set_lang':
                            await asyncio.sleep(0.5)
                            break


@bot.on(events.NewMessage(incoming=True))
async def link_linkedin(message: Message):

    sender: UserType = await message.get_sender()

    with User() as db:
        lang = db.language(sender.id)

        if not (linkedin := db.fetch(columns='linkedin_id', telegram_id=sender.id, size=1)) or not linkedin[0]:
            redis = Redis()
            code = redis.server.get(str(sender.id))

            if not code:
                code = generate_unique_id(24)
                redis.server.set(str(sender.id), code, ex=1800)
            else:
                code = code.decode('utf-8')

            text = texts.LinkYourLinkedIn().get(lang).replace('%code%', f"{sender.id}:{code}")

            await message.respond(
                text,
                buttons=keyboards.OpenMyLinkedin().get(lang)
            )
            raise events.StopPropagation

        else:
            await message.respond(
                texts.LinkedinAlreadyLinked().get(lang),
                buttons=keyboards.OpenMyLinkedin().get(lang)
            )
            raise events.StopPropagation


@bot.on(events.CallbackQuery())
async def callback_handler(call: CallbackQuery):
    message: Message = await call.get_message()
    sender: UserType = await call.get_sender()
    data: str = call.data.decode('utf-8')

    action, value = data.split('::')

    if action == 'set_lang':
        with User() as db:
            db.update({'language': value}, filters={'telegram_id': sender.id})
            await message.delete()
            await message.respond(texts.LanguageIsSet.get(value))


# run the LinkedIn bot
bot.loop.run_until_complete(linkedin_bot.start(bot))
