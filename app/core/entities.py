from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PlaceDTO:
    id: int
    name: str
    description: Optional[str]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    category: Optional[str]
