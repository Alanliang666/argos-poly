"""
WebSocket client for connecting to Polymarket and streaming real-time market data.
"""
from src.config import WS_PING_INTERVAL, WS_PING_TIMEOUT
import asyncio
import websockets
import json
import certifi
import ssl

class WsClient:
    def __init__(self, market_info, url):
        """
        Initializes the WebSocket client.
        @param market_info: dict, mapping of asset IDs to market details.
        @param url: str, the Polymarket WebSocket endpoint URL.
        """
        self.market_info = market_info
        self.url = url
        self.queue = asyncio.Queue()

    async def ws_connect(self):
        """
        Maintains a persistent WebSocket connection and routes incoming messages to the queue.
        """
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        while True:
            try:
                async with websockets.connect(self.url, ping_interval=WS_PING_INTERVAL, ping_timeout=WS_PING_TIMEOUT, ssl=ssl_context, max_size=None) as ws:
                    await ws.send(self._build_subscription_payload())
                    while True:
                        message = await ws.recv()
                        await self.queue.put(message)

            except asyncio.CancelledError:
                raise
    
            except Exception as e:
                # Wait before attempting to reconnect
                await asyncio.sleep(5)

    def _build_subscription_payload(self):
        """
        Builds the payload structure required to subscribe to the market data feed.
        @return: str, a JSON-formatted string representing the subscription payload.
        """
        send_json = {"assets_ids":list(self.market_info), # Market info from the API data
                    "type":'market',
                    "initial_dump":True,
                    "level":2,
                    "custom_feature_enabled":True
                    }
        return json.dumps(send_json)