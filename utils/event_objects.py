from dataclasses import dataclass
from dataclasses_json import LetterCase, Undefined, dataclass_json
from typing import Optional


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.EXCLUDE)
@dataclass
class Video:
    url: str = ""
    format: str = ""


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.EXCLUDE)
@dataclass
class Media:
    images: list[str] = None
    videos: list[Video] = None
    documents: list[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.EXCLUDE)
@dataclass
class EventDetails:
    text: str = ""
    sender: str = ""
    author: str = ""
    media: Optional[Media] = None

