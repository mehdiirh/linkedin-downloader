from telethon import Button
from utils.telegram.tools import Text

from pathlib import Path
import json

config_path = Path(__file__).resolve().parent.parent.parent / 'config.json'
linkedin_url = json.load(open(config_path, 'r'))["LINKEDIN"]["URL"]

_i = Button.inline
_t = Button.text
_u = Button.url

SET_LANG = [
    [_i('🇺🇸 English', 'set_lang::en'), _i('🇮🇷 فارسی', 'set_lang::fa')]
]

SET_LANG_CONVERSATION = [
    [_i('🇺🇸 English', 'set_lang_conv::en'), _i('🇮🇷 فارسی', 'set_lang_conv::fa')]
]


class OpenMyLinkedin(Text):

    en = [
        [_u('Open My Linkedin', linkedin_url)]
    ]

    fa = [
        [_u('بازکردن لینکدین من', linkedin_url)]
    ]
