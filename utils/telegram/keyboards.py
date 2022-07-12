from telethon import Button
from utils.telegram.tools import Text

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
        [_u('Open My Linkedin', 'https://linkedin.com/in/mrdownloader/')]
    ]

    fa = [
        [_u('بازکردن لینکدین من', 'https://linkedin.com/in/mrdownloader/')]
    ]
