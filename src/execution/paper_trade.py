"""
Paper Trade Logging for the strategy layer.

This module provides trade history logging and converts execution signals into a formatted local store.
"""
import logging

class PaperTrade:
    def __init__(self):
        """
        Initializes the paper trade environment and sets up the logger.
        """
        self.trade_history = []
        self.logger = logging.getLogger('PaperTrade')
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            ch = logging.StreamHandler()

            formatter = logging.Formatter('[%(asctime)s] | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def execute_arbitrage(self, market_id: str, market_type: str, total_cost: float, expected_profit: float):
        """
        Executes a paper trade based on an arbitrage signal and logs the trade history.

        @param market_id: The Polymarket event ID (used as the token ID).
        @param market_type: The type of market from Polymarket (e.g., an election event).
        @param total_cost: The total expected cost to execute the trade.
        @param expected_profit: The expected risk-free profit from this execution.
        @Raises ValueError: If total_cost is negative.
        """
        trade_record = {
            'Market': market_id,
            'Type': market_type,
            'Cost': total_cost,
            'Expected Profit': expected_profit,
        }

        if total_cost < 0:  # Edge case: process error if strategy gives a negative price
            raise ValueError(f"Invalid total_cost: {total_cost}. Cost cannot be negative.")

        self.trade_history.append(trade_record)

        log_message = f"Market: {market_id} | Type: {market_type} | Cost: ${total_cost:.2f} | Expected Profit: ${expected_profit:.2f}"
        
        self.logger.info(log_message)