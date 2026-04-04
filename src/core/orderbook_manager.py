"""
Handle the bid/ask data from the WebSocket
"""
import json
import traceback

class OrderBookManager:
    def __init__(self, queue, market_info):
        """
        Initializes the order book state.
        @param queue: asyncio.Queue, receives messages from the WebSocket.
        @param market_info: dict, mapping of asset IDs to market details.
        """
        self.order_book = {}
        self.queue = queue
        self.market_info = market_info

    async def start(self):
        """
        Starts the consumer loop to process incoming WebSocket messages and update the order book.
        """
        while True:
            message = await self.queue.get()
            try:
                message_dict = json.loads(message)
                if isinstance(message_dict, list):  # Polymarket may batch multiple events into a single JSON array
                    for msg in message_dict:
                        self._handle_message(msg)
                else:
                    self._handle_message(message_dict)
            
            except json.JSONDecodeError:
                print(f"Invalid JSON received, ignoring: {message}")
                continue
            
            except Exception as e:
                print(f"Unexpected error during orderbook update: {e}")
                
                traceback.print_exc()
                continue

    def _handle_message(self, message_dict):
        """
        Parses the incoming message and updates the local order book state.
        @param message_dict: dict, the newest data payload from the WebSocket.
        """
        if message_dict.get("event_type") == "price_change":
            for change in message_dict.get("price_changes", []):
                asset_id = change.get("asset_id")
                if asset_id in self.market_info:
                    market_id, question, outcome = self.market_info[asset_id]
                    if market_id not in self.order_book:
                        self.order_book[market_id] = {
                            "question":question,
                        }
                    self.order_book[market_id][outcome] = {
                        "best_bid":change.get("best_bid"),
                        "best_ask":change.get("best_ask")
                    }