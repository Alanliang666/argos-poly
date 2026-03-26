"""
"""

import asyncio
import websockets
import json
import certifi
import ssl

class WsClient:
    def __init__(self, market_info, url):
        # get the market info into this function
        self.market_info = market_info
        self.url = url
        self.queue = asyncio.Queue()

    async def ws_connect(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        while True:
            try:
                async with websockets.connect(self.url, ping_interval=10, ping_timeout=10, ssl=ssl_context) as ws:
                    await ws.send(self._build_subscription_payload())
                    while True:
                        message = await ws.recv()
                        await self.queue.put(message)

            except Exception as e:
                # if return error then we stop 5 sencond for next round
                await asyncio.sleep(5)

    def _build_subscription_payload(self):
        send_json = {"assets_ids":list(self.market_info),
                    "type":'market',
                    "initial_dump":True,
                    "level":2,
                    "custom_feature_enabled":True
                    }
        return json.dumps(send_json)