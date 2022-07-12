
class Text:

    en = ''
    fa = ''

    @classmethod
    def get(cls, lang):
        return getattr(cls, lang, 'en')

