from enum import Enum

class EventType(Enum):
    REPLY = "reply"
    TIME = "time"
    REACTION = "reaction"


class ChatType(Enum):
    USER = 'user'
    GROUP = 'group'