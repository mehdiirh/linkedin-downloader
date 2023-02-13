class Text:

    en = ""
    fa = ""

    @classmethod
    def get(cls, lang: str) -> str:
        """
        Get text in specified language. If language is not specified, return text in English.
        Args:
            lang (str): Language code.

        Returns:
            (str): Text in specified language.
        """

        try:
            return getattr(cls, lang)
        except AttributeError:
            return cls.en
