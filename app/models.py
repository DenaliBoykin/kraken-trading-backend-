from pydantic import BaseModel, field_validator

class OrderRequest(BaseModel):
    pair: str
    side: str
    ordertype: str = "market"
    volume: float

    @field_validator("side")
    @classmethod
    def validate_side(cls, v: str) -> str:
        normalized = v.strip().lower()
        if normalized not in {"buy", "sell"}:
            raise ValueError("side must be 'buy' or 'sell'")
        return normalized

    @field_validator("ordertype")
    @classmethod
    def validate_ordertype(cls, v: str) -> str:
        normalized = v.strip().lower()
        if normalized not in {"market", "limit"}:
            raise ValueError("ordertype must be 'market' or 'limit'")
        return normalized

    @field_validator("volume")
    @classmethod
    def validate_volume(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("volume must be greater than 0")
        return v
