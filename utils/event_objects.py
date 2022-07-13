from dataclasses import dataclass, field
from dataclasses_json import LetterCase, Undefined, dataclass_json
from linkedin_messaging.api_objects import MiniProfile

from typing import Optional


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class Badge:
    count: int = ""
    tab: str = ""


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class TabBadges:
    tab_badges: list[Badge] = field(default_factory=list)


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class Invite:
    sent_time: int = -1
    invitation_type: str = ""
    shared_secret: str = ""
    entity_urn: str = ""
    to_member_id: str = ""
    unseen: bool = False
    from_member: Optional[MiniProfile] = None
    to_member: Optional[MiniProfile] = None


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
