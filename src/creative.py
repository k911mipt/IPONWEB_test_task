import dataclasses
from typing import Optional


@dataclasses.dataclass
class Creative:
    price: int
    advertiser_id: str
    country_to_serve: Optional[str] = None

