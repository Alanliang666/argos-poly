"""
Unit tests for the StrategyEngine and CostEstimator logic.
Test Coverage:
- Estimate Cost Correct: Validates that the estimated cost is calculated correctly.
- Opportunities Check: Validates that profitable opportunities are correctly identified and stored as signals.
- No Opportunities: Verifies that no signals are generated if the total cost is 1.00 or higher.
- Multiple Choice: Validates that markets with multiple choices (3 or more outcomes) are calculated correctly.
- Empty Orderbook: Ensures that an empty orderbook is handled gracefully without generating signals.
- Multiple Market: Verifies that the engine correctly processes multiple markets and only stores the profitable ones.
- Missing Liquidity: Ensures that markets with missing liquidity (best_ask is 0 or None) are completely skipped.
"""
from src.strategy import StrategyEngine, CostEstimator
import pytest

def test_estimate_correct():
    """
    Tests the happy path for calculating the estimated cost.
    """
    cost_calculate = CostEstimator()

    total_cost = cost_calculate.estimated_cost(100)

    assert total_cost == pytest.approx(0.7)

def test_opportunities_exist():
    """
    Tests that valid arbitrage opportunities are correctly identified from the orderbook.
    """

    opportunities = StrategyEngine()

    fake_orderbook = {
                        'market_123':{
                            'question':'Will BTC hit 100k?',
                            'Yes':{'best_ask':0.5, 'best_bid':0.49},
                            'No':{'best_ask':0.35, 'best_bid':0.34}
                        }
                    }
    
    opportunities.find_opportunities(fake_orderbook)

    assert len(opportunities.signals) == 1
    assert opportunities.signals[0]['total_cost'] == pytest.approx(0.85595)
    assert opportunities.signals[0]['expected_profit'] == pytest.approx(0.14405)

def test_no_opportunities_when_cost_high():
    """
    Tests that no signal is generated when the total cost is 1.00 or higher.
    """
    opportunities = StrategyEngine()

    fake_orderbook = {
                        'market_123':{
                            'question':'Will BTC hit 100k?',
                            'Yes':{'best_ask':0.8, 'best_bid':0.49},
                            'No':{'best_ask':0.6, 'best_bid':0.34}
                        }
                    }
    
    opportunities.find_opportunities(fake_orderbook)

    assert len(opportunities.signals) == 0

def test_multiple_choice():
    """
    Tests the engine's ability to correctly calculate costs for a market with more than two outcomes.
    """
    opportunities = StrategyEngine()

    fake_orderbook = {
                        'market_123':{
                            'question':'Will BTC hit 100k?',
                            'teamA':{'best_ask':0.1, 'best_bid':0.49},
                            'teamB':{'best_ask':0.2, 'best_bid':0.34},
                            'teamC':{'best_ask':0.3, 'best_bid':0.34},
                        }
                    }
    
    opportunities.find_opportunities(fake_orderbook)

    assert len(opportunities.signals) == 1
    assert opportunities.signals[0]['total_cost'] == pytest.approx(0.6042)
    assert opportunities.signals[0]['expected_profit'] == pytest.approx(1-0.6042)

def test_empty_orderbook():
    """
    Tests that an empty orderbook does not generate any signals or errors.
    """
    opportunities = StrategyEngine()

    fake_orderbook = {}
    
    opportunities.find_opportunities(fake_orderbook)

    assert len(opportunities.signals) == 0

def test_multiple_market():
    """
    Tests the engine's ability to iterate over multiple markets and exclusively identify profitable ones.
    """
    opportunities = StrategyEngine()

    fake_orderbook = {
                        'market_123':{
                            'question':'Will BTC hit 100k?',
                            'teamA':{'best_ask':0.1, 'best_bid':0.49},
                            'teamB':{'best_ask':0.2, 'best_bid':0.34},
                            'teamC':{'best_ask':0.3, 'best_bid':0.34},
                        },
                        'market_456':{
                            'question':'Will BTC hit 100k?',
                            'Yes':{'best_ask':0.99, 'best_bid':0.49},
                            'No':{'best_ask':0.77, 'best_bid':0.34}
                        }
                    }
    
    opportunities.find_opportunities(fake_orderbook)

    assert len(opportunities.signals) == 1
    assert opportunities.signals[0]['total_cost'] == pytest.approx(0.6042)
    assert opportunities.signals[0]['expected_profit'] == pytest.approx(1-0.6042)

def test_missing_liquidity():
    """
    Tests that markets with missing liquidity (best_ask is 0 or None) are completely skipped.
    """
    opportunities = StrategyEngine()

    fake_orderbook = {
                        'market_123':{
                            'question':'Will BTC hit 100k?',
                            'teamA':{'best_ask':0, 'best_bid':0.49},
                            'teamB':{'best_ask':0.2, 'best_bid':0.34}
                        }
                    }
    
    opportunities.find_opportunities(fake_orderbook)

    assert len(opportunities.signals) == 0