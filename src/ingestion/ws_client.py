"""
TO DO: 
- [Data Layer] Update `self.book_order` to maintain the latest Best Bid/Offer (BBO) as a real-time state shadow.
- [Bridge] Use `self.queue.put_nowait(market_id)` to dispatch non-blocking update signals.
- [Execute Layer] Create an independent async consumer loop (`await queue.get()`) to evaluate strategy rules purely against the freshest `self.book_order` state, bypassing stale ticks, and execute trades instantly.
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
        self.book_order = {}
        self.book_order["market_id"] = {}
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

    def _handle_message(self, message_dict):
        if message_dict.get("event_type") == "price_change":
            for change in message_dict.get("price_changes", []):
                asset_id = change.get("asset_id")
                if asset_id in self.market_info:
                    market_id, question, outcome = self.market_info[asset_id]
                    print(f"Event {question} -> {outcome} ask update -> {change.get('best_bid')}") 


# test case for develope
# async def main():
#     dummy_market_info = {
#         "1234567890": ("MockMarket", "Will BTC reach 100k?", "Yes"),
#         "0987654321": ("MockMarket", "Will BTC reach 100k?", "No")
#     }
#     client = WsClient(dummy_market_info,'wss://ws-subscriptions-clob.polymarket.com/ws/market')
#     asyncio.create_task(client.ws_connect())
#     while True: 
#         print(await client.queue.get())

# if __name__ == "__main__":
#     asyncio.run(main())