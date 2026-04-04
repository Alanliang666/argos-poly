"""
Unit tests for the OrderBookManager core logic and async background processing.

Test Coverage:
- Message Handle: Validates that incoming WebSocket messages are correctly parsed and stored into the order book structure.
- Invalid Asset ID: Ensures that price updates for unknown asset IDs are safely ignored.
- Async Processing: Verifies that the async start loop correctly consumes items from the queue.
- Fault Tolerance: Confirms the loop survives malformed JSON payloads and successfully processes subsequent valid data.
"""

from src.core import OrderBookManager
from mock import patch, AsyncMock
import json
import pytest
import asyncio

def test_handle_message_success():
    """
    Tests that valid market updates are properly mapped and stored in the order book hierarchy.
    """
    
    test_info = {
        "tokenA": ["market123", "Will BTC hit 100k?", "Yes"],
        "tokenB": ["market123", "Will BTC hit 100k?", "No"]
        }

    test_queue = []

    test_dict = {
        'event_type':'price_change',
        'price_changes':[
            {
            'asset_id':'tokenA',
            'best_bid':'0.45',
            'best_ask':'0.55'
            },
            {
            'asset_id':'tokenB',
            'best_bid':'0.32',
            'best_ask':'0.11'  
            }
        ]
    }

    orderbook = OrderBookManager(test_queue, test_info)

    orderbook._handle_message(test_dict)

    assert orderbook.order_book['market123'] == {
                    'question':'Will BTC hit 100k?', 
                    'Yes':{'best_bid':'0.45', 'best_ask':'0.55'},
                    'No':{'best_bid':'0.32', 'best_ask':'0.11'}
                }


def test_handle_message_invalid_asset_id():
    """
    Tests that price updates for missing or unrecognised asset IDs are ignored and do not mutate the order book.
    """
    
    test_info = {
        "tokenA": ["market123", "Will BTC hit 100k?", "Yes"],
        "tokenB": ["market123", "Will BTC hit 100k?", "No"]
        }

    test_queue = []

    test_dict = {
        'event_type':'price_change',
        'price_changes':[
            {
            'asset_id':'FakeToken',
            'best_bid':'9.99',
            'best_ask':'0.01'  
            }
        ]
    }

    orderbook = OrderBookManager(test_queue, test_info)

    orderbook._handle_message(test_dict)

    assert orderbook.order_book == {}


@pytest.mark.asyncio
async def test_start_success():
    """
    Tests that the async background task successfully consumes and processes valid messages from the queue.
    """
    
    test_queue = asyncio.Queue()

    test_info = {
        "tokenA": ["market123", "Will BTC hit 100k?", "Yes"],
        "tokenB": ["market123", "Will BTC hit 100k?", "No"]
        }

    test_dict = {
        'event_type':'price_change',
        'price_changes':[
            {
            'asset_id':'tokenA',
            'best_bid':'0.45',
            'best_ask':'0.55'
            },
            {
            'asset_id':'tokenB',
            'best_bid':'0.32',
            'best_ask':'0.11'  
            }
        ]
    }

    orderbook = OrderBookManager(test_queue, test_info)

    await test_queue.put(json.dumps(test_dict))

    task = asyncio.create_task(orderbook.start())

    await asyncio.sleep(0.1)

    assert orderbook.order_book['market123']['question'] == 'Will BTC hit 100k?'

    task.cancel()


@pytest.mark.asyncio
async def test_start_survives_invalid_json():
    """
    Tests that the consumer loop catches JSONDecodeError, ignores malformed payloads, and successfully continues to process subsequent messages.
    """
    
    test_queue = asyncio.Queue()

    test_info = {
        "tokenA": ["market123", "Will BTC hit 100k?", "Yes"],
        "tokenB": ["market123", "Will BTC hit 100k?", "No"]
        }

    test_dict = {
        'event_type':'price_change',
        'price_changes':[
            {
            'asset_id':'tokenA',
            'best_bid':'0.45',
            'best_ask':'0.55'
            },
            {
            'asset_id':'tokenB',
            'best_bid':'0.32',
            'best_ask':'0.11'  
            }
        ]
    }

    orderbook = OrderBookManager(test_queue, test_info)

    await test_queue.put('This is not a JSON')
    await test_queue.put(json.dumps(test_dict))

    task = asyncio.create_task(orderbook.start())

    await asyncio.sleep(0.1)

    assert orderbook.order_book['market123']['question'] == 'Will BTC hit 100k?'

    task.cancel()