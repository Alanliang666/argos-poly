"""
Unit tests for the PaperTrade execution module.

Test Coverage:
- Info Correction: Validates the trade information is correctly formatted and stored.
- Multiple Trades: Validates that multiple trades are stored successfully in the trade history.
- Negative Cost: Tests that a negative cost raises an error and is not saved.
- Log Format: Tests that the physical log output matches the specification.
"""
from src.execution import PaperTrade
import pytest
import logging

def test_paper_trade_correct_info():
    """
    Tests that a single paper trade is correctly appended to the trade history.
    """
    pt = PaperTrade()
    pt.execute_arbitrage(
        market_id="0x1234...abcd",
        market_type="Presidential Election",
        total_cost=0.95,
        expected_profit=0.05
    )
    assert len(pt.trade_history) == 1
    assert pt.trade_history[0]['Market'] == "0x1234...abcd"
    assert pt.trade_history[0]['Expected Profit'] == 0.05

def test_multiple_trades():
    """
    Tests that multiple paper trades are successfully stored without overwriting each other.
    """
    pt = PaperTrade()
    pt.execute_arbitrage("M_1", "Type A", 0.9, 0.1)
    pt.execute_arbitrage("M_2", "Type B", 0.95, 0.05)

    assert len(pt.trade_history) == 2
    assert pt.trade_history[0]['Market'] == 'M_1'
    assert pt.trade_history[1]['Market'] == 'M_2'

def test_negative_cost():
    """
    Tests that a negative cost raises a ValueError and is not stored in the history.
    """
    pt = PaperTrade()

    with pytest.raises(ValueError):  # Expected ValueError will trigger
        pt.execute_arbitrage("M_1", "Type A", -0.5, 0.1)

    assert len(pt.trade_history) == 0

def test_log_format(caplog):
    """
    Tests that the generated execution log matches the required string format.
    """
    pt = PaperTrade()

    with caplog.at_level(logging.INFO):
        pt.execute_arbitrage("M_999", "Election", 0.8, 0.2)
    
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "INFO"
    assert "Market: M_999" in caplog.text
    assert "Cost: $ 0.80" in caplog.text
    assert "Expected Profit: $ 0.20" in caplog.text