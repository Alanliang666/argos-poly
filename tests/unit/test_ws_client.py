"""
Unit tests for the WsClient.

Test Coverage:
- Payload valid: Validates the payload format with normal market info.
- Empty payload: Validates payload generation when market info is empty.
- Connect success: Tests successful WebSocket connections and message queueing.
- Sleep state: Tests the reconnection logic upon disconnection.
"""
from src.ingestion import WsClient
from mock import patch, AsyncMock
import json
import pytest
import asyncio

def test_build_payload_valid():
    """
    Validates that the subscription payload is built correctly with valid market info.
    """
    url = 'fake_url'

    test_info = {
        "tokenA": ["market123", "Will BTC hit 100k?", "Yes"],
        "tokenB": ["market123", "Will BTC hit 100k?", "No"]
    }

    ws_client = WsClient(test_info, url)
    test_json = ws_client._build_subscription_payload()
    test_json = json.loads(test_json)
    
    assert test_json['assets_ids'] == ['tokenA', 'tokenB']
    assert test_json['type'] == 'market'
    assert test_json['initial_dump'] == True
    assert test_json['level'] == 2
    assert test_json['custom_feature_enabled'] == True

def test_build_payload_empty_market_info():
    """
    Validates that an empty market_info results in an empty 'assets_ids' list in the payload.
    """
    
    url = 'fake_url'

    test_info = {}

    ws_client = WsClient(test_info, url)
    test_json = ws_client._build_subscription_payload()
    test_json = json.loads(test_json)
    
    assert test_json['assets_ids'] == []
    assert test_json['type'] == 'market'
    assert test_json['initial_dump'] == True
    assert test_json['level'] == 2
    assert test_json['custom_feature_enabled'] == True


@pytest.mark.asyncio 
@patch('src.ingestion.ws_client.websockets.connect')
async def test_ws_connect_success(mock_connect):
    """
    Tests the successful WebSocket connection and validates that received data is pushed to the queue.
    """
    url = 'fake_url'
    
    test_info = {
        "tokenA": ["market123", "Will BTC hit 100k?", "Yes"],
        "tokenB": ["market123", "Will BTC hit 100k?", "No"]
    }

    mock_ws = AsyncMock()
    
    mock_ws.recv.side_effect = ['{"price":100}',Exception("Broken connect")]

    mock_connect.return_value.__aenter__.return_value = mock_ws
    ws_client = WsClient(test_info, url)
    
    try:
        await asyncio.wait_for(ws_client.ws_connect(), timeout=0.1)
    
    except asyncio.TimeoutError:
        pass
    
    mock_ws.send.assert_called_once()
    assert ws_client.queue.qsize() > 0

@pytest.mark.asyncio
@patch('src.ingestion.ws_client.websockets.connect')
@patch('src.ingestion.ws_client.asyncio.sleep')
async def test_ws_sleep_success(mock_sleep, mock_connect):
    """
    Tests the reconnection mechanism by mocking a disconnection and verifying the sleep timeout.
    """
    url = 'fake_url'
    
    test_info = {
        "tokenA": ["market123", "Will BTC hit 100k?", "Yes"],
        "tokenB": ["market123", "Will BTC hit 100k?", "No"]
    }

    mock_ws = AsyncMock()

    ws_client = WsClient(test_info, url)

    mock_ws.recv.side_effect = Exception('Broken connect')

    mock_sleep.side_effect = asyncio.CancelledError()

    mock_connect.return_value.__aenter__.return_value = mock_ws

    try:
        await ws_client.ws_connect()

    except asyncio.CancelledError:
        pass

    mock_sleep.assert_called_with(5)