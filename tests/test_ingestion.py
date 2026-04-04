"""
Integration tests for the data ingestion pipeline.
Verifies the end-to-end data flow from the API and WebSocket down to the order book state.
"""
from src.ingestion import ApiClient
from src.ingestion import WsClient
from src.core import OrderBookManager
import asyncio

async def test_ingestion():
    """
    Fetches market info from the REST API, uses the token IDs to subscribe to the WebSocket market data,
    and stores the live bid/ask quotes into the order book in preparation for the execution layer.
    """
    api_client = ApiClient('https://gamma-api.polymarket.com/events')
    api_client.OFFSET = 50
    await api_client.get_market_info()
    
    ws_client = WsClient(api_client.market_info,'wss://ws-subscriptions-clob.polymarket.com/ws/market')
    task_ws = asyncio.create_task(ws_client.ws_connect())

    order_book = OrderBookManager(ws_client.queue, ws_client.market_info)
    task_ob = asyncio.create_task(order_book.start())

    await asyncio.sleep(30)
    print(order_book.order_book)

    task_ws.cancel()
    task_ob.cancel()

if __name__ == '__main__':
    asyncio.run(test_ingestion())
