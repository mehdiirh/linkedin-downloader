from telethon import Button
from utils.telegram.tools import Text

import settings

linkedin_url = settings.LINKEDIN["URL"]

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
        [_u('✅ Open My Linkedin', linkedin_url)]
    ]

    fa = [
        [_u('✅ بازکردن لینکدین من', linkedin_url)]
    ]
