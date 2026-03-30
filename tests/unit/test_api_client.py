"""
Unit tests for the ApiClient data extraction logic.

Test Coverage:
- Happy Path: Valid market events are successfully parsed and stored.
- Closed Markets: Markets marked as 'closed' are ignored.
- Invalid JSON: Malformed JSON strings are caught and gracefully skipped.
- Mismatched Lengths: Events with unequal token arrays are rejected.
"""
from src.ingestion import ApiClient

def test_extract_market_info_success():
    """
    Verifies that valid market events are correctly extracted and stored in the internal state.
    """
    fake = "fake_url"
    api = ApiClient(fake)

    test_info = [
            {
                'markets':[
                    {
                        'closed':False,
                        'id':"market123",
                        'question':"Will BTC hit 100k?",
                        'outcomes':'["Yes", "No"]',
                        'clobTokenIds':'["tokenA", "tokenB"]'
                    }
                ]
            }
    ]
    api.extract_market_info(test_info)
    assert api.market_info['tokenA'] == ['market123', 'Will BTC hit 100k?', 'Yes']
    assert api.market_info['tokenB'] == ['market123', 'Will BTC hit 100k?', 'No']

def test_extract_market_info_closed_market():
    """
    Ensures that markets with the 'closed' flag set to True are ignored.
    """
    fake = "fake_url"
    api = ApiClient(fake)

    test_info = [
            {
                'markets':[
                    {
                        'closed':True,
                        'id':"market123",
                        'question':"Will BTC hit 100k?",
                        'outcomes':'["Yes", "No"]',
                        'clobTokenIds':'["tokenA", "tokenB"]'
                    }
                ]
            }
    ]
    api.extract_market_info(test_info)
    assert api.market_info == {}

def test_extract_market_info_invalid_json():
    """
    Tests that malformed JSON in 'outcomes' or 'clobTokenIds' triggers a graceful skip without crashing the module.
    """
    fake = "fake_url"
    api = ApiClient(fake)

    test_info = [
            {
                'markets':[
                    {
                        'closed':False,
                        'id':"market123",
                        'question':"Will BTC hit 100k?",
                        'outcomes':'[Yes, "No"]',
                        'clobTokenIds':'["tokenA", "tokenB"]'
                    }
                ]
            }
    ]
    api.extract_market_info(test_info)
    assert api.market_info == {}

def test_extract_market_info_mismatched_lengths():
    """
    Validates that if the number of token IDs does not match the number of outcomes, the market is discarded.
    """
    fake = "fake_url"
    api = ApiClient(fake)

    test_info = [
            {
                'markets':[
                    {
                        'closed':False,
                        'id':"market123",
                        'question':"Will BTC hit 100k?",
                        'outcomes':'["Yes", "No", "Maybe"]',
                        'clobTokenIds':'["tokenA", "tokenB"]'
                    }
                ]
            }
    ]
    api.extract_market_info(test_info)
    assert api.market_info == {}