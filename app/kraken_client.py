import base64
import hashlib
import hmac
import time
import urllib.parse
import requests

from app.config import KRAKEN_API_KEY, KRAKEN_API_SECRET

BASE_URL = "https://api.kraken.com"

class KrakenClient:
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret

    def _signature(self, url_path: str, data: dict) -> str:
        """
        Kraken private endpoint signing.
        """
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data["nonce"]) + postdata).encode()
        message = url_path.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(
            base64.b64decode(self.api_secret),
            message,
            hashlib.sha512,
        )
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def private_post(self, url_path: str, data: dict) -> dict:
        if not self.api_key or not self.api_secret:
            raise RuntimeError("Missing Kraken API credentials")

        headers = {
            "API-Key": self.api_key,
            "API-Sign": self._signature(url_path, data),
        }

        response = requests.post(
            BASE_URL + url_path,
            headers=headers,
            data=data,
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    def get_balance(self) -> dict:
        data = {"nonce": int(time.time() * 1000)}
        return self.private_post("/0/private/Balance", data)

    def add_order(
        self,
        pair: str,
        side: str,
        ordertype: str,
        volume: float,
    ) -> dict:
        data = {
            "nonce": int(time.time() * 1000),
            "pair": pair,
            "type": side,
            "ordertype": ordertype,
            "volume": str(volume),
        }
        return self.private_post("/0/private/AddOrder", data)


kraken_client = KrakenClient(
    api_key=KRAKEN_API_KEY,
    api_secret=KRAKEN_API_SECRET,
)
