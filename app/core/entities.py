from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDTO:
    id: Optional[int]
    username: Optional[str]
    first_seen: Optional[datetime]