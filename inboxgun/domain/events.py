from dataclasses import dataclass
from typing import Optional

class Event:
    pass

@dataclass
class CustomerOptIn(Event):
    customer_id: str
    customer_list: str
    reason: Optional[str]


@dataclass
class CustomerRemoveFromList(Event):
    customer_id: str
    customer_list: str
    reason: Optional[str]
