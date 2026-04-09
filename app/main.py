from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.config import DRY_RUN, ALLOWED_PAIRS, MAX_ORDER_SIZE
from app.kraken_client import kraken_client
from app.models import OrderRequest
from app.safety import validate_order_rules

app = FastAPI(
    title="Kraken Trading Backend",
    version="0.1.0",
    description="Small beginner-friendly backend for Kraken trading"
)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "dry_run": DRY_RUN,
        "allowed_pairs": ALLOWED_PAIRS,
        "max_order_size": MAX_ORDER_SIZE,
    }


@app.get("/balance")
def balance() -> JSONResponse:
    try:
        result = kraken_client.get_balance()
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/order")
def place_order(order: OrderRequest) -> JSONResponse:
    validate_order_rules(order.pair, order.volume)

    if DRY_RUN:
        return JSONResponse(
            content={
                "dry_run": True,
                "message": "Order was validated but not sent because DRY_RUN=true",
                "order": {
                    "pair": order.pair,
                    "side": order.side,
                    "ordertype": order.ordertype,
                    "volume": order.volume,
                },
            }
        )

    try:
        result = kraken_client.add_order(
            pair=order.pair,
            side=order.side,
            ordertype=order.ordertype,
            volume=order.volume,
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
