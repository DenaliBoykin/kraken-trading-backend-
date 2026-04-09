from fastapi import HTTPException
from app.config import ALLOWED_PAIRS, MAX_ORDER_SIZE

def validate_order_rules(pair: str, volume: float) -> None:
    if pair not in ALLOWED_PAIRS:
        raise HTTPException(
            status_code=400,
            detail=f"Pair '{pair}' is not allowed. Allowed pairs: {ALLOWED_PAIRS}"
        )

    if volume > MAX_ORDER_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Order volume {volume} exceeds MAX_ORDER_SIZE={MAX_ORDER_SIZE}"
        )
