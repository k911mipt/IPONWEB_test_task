import dataclasses
from typing import Optional

PriceType = int
IdType = str
CountryType = str

@dataclasses.dataclass
class Creative:
    price: int
    advertiser_id: str
    country: Optional[str] = None

