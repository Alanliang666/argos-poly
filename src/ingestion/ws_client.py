import asyncio
import websockets
import json

class WsClient:
    def __init__(self, market_info, url):
        # get the market info into this function
        self.market_info = market_info
        self.url = url
        self.book_order["market_id"] = {}
        self.queue = asyncio.Queue()

    async def ws_connect(self):
        async with websockets.connect(self.url) as ws:
            await ws.send(self._build_subscription_payload())

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