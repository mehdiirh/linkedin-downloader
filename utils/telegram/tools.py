from utils.event_objects import EventDetails
from utils.database.models import Database, User


class Text:

    en = ''
    fa = ''

    @classmethod
    def get(cls, lang):
        return getattr(cls, lang, 'en')

