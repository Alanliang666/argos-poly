"""
TO DO: 
- [Bridge] Use `self.queue.put_nowait(market_id)` to dispatch non-blocking update signals.
- [Execute Layer] Create an independent async consumer loop (`await queue.get()`) to evaluate strategy rules purely against the freshest `self.book_order` state, bypassing stale ticks, and execute trades instantly.
"""

import json
import traceback

class OrderBookManager:
    def __init__(self, queue, market_info):
        self.order_book = {}
        self.queue = queue
        self.market_info = market_info

    async def start(self):
        while True:
            message = await self.queue.get()
            try:
                message_dict = json.loads(message)
                self._handle_message(message_dict)
            
            except json.JSONDecodeError:
                print(f"Invalid JSON received, ignoring: {message}")
                continue
            
            except Exception as e:
                print(f"Unexpected error during orderbook update: {e}")
                
                traceback.print_exc()
                continue

    def _handle_message(self, message_dict):
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
                    return market_id