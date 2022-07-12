from telethon.sync import TelegramClient
from telethon.sessions import MemorySession

from pathlib import Path
import json

config_path = Path(__file__).resolve().parent.parent.parent / 'config.json'
config = json.load(open(config_path, 'r'))["TG"]

api_id = config["API_ID"]
api_hash = config["API_HASH"]
TOKEN = config["TOKEN"]


def get_bot() -> TelegramClient:
    bot = TelegramClient(MemorySession(), api_id, api_hash)
    return bot.start(bot_token=TOKEN)


async def get_bot_async(loop=None) -> TelegramClient:
    bot = TelegramClient(MemorySession(), api_id, api_hash, loop=loop)
    bot = await bot.start(bot_token=TOKEN)
    return bot
