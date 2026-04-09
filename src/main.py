"""
Entry point for the trading bot.
Coordinates the entire execution pipeline, from fetching API data to recording trades.
"""
from src.config import POLYMARKET_REST_URL, POLYMARKET_WS_URL
from src.execution import PaperTrade
from src.ingestion import ApiClient, WsClient
from src.strategy import StrategyEngine
from src.core import OrderBookManager
import asyncio
import datetime

async def main():
    """
    Fetches market data from the Polymarket API, subscribes to WebSocket updates,
    evaluates strategy conditions, and records executed paper trades.
    """
    # API Initialization
    api = ApiClient(POLYMARKET_REST_URL)
    await api.get_market_info()
    asyncio.create_task(ws.ws_connect())

    # WebSocket Initialization
    ws = WsClient(api.market_info, POLYMARKET_WS_URL)

    # OrderBook Initialization
    ob = OrderBookManager(ws.queue, ws.market_info)
    asyncio.create_task(ob.start())

    # Strategy & Paper Trading Setup
    se = StrategyEngine()
    pt = PaperTrade()
    
    while True:
        await asyncio.sleep(5)  # Poll for opportunities every 5 seconds
        now_time = datetime.datetime.now().strftime('%H:%M:%S')  # Print the current execution time
        print(f"[{now_time}] Scanning... Active markets in OrderBook: {len(ob.order_book)}")
        se.find_opportunities(ob.order_book)
        for signal in se.signals:
            pt.execute_arbitrage(signal['market_id'], signal['market_type'],
                                signal['total_cost'], signal['expected_profit'])
        se.signals.clear()

if __name__ == '__main__':
    asyncio.run(main())