"""
Strategy handle logic for the calculate the arbitrage formula

This module provides arbitrage formula to calculate the choice price isn't have any chance for profit.
"""
class StrategyEngine:
    def __init__(self):
        """
        Initialize the strategy engine and prepare the empty signals list for execution.
        """
        self.signals = []
        self.estimator = CostEstimator()
    
    def find_opportunities(self, orderbook):
        """
        Evaluate if the total cost of all outcomes is less than 1.00 (inclusive of fees) 
        and append profitable opportunities to the signals list.
        @param orderbook: dict, the current order book snapshot from Polymarket.
        """
        for market_id, market_data in orderbook.items():
            total_cost = 0
            is_market_valid = True
            for outcome_name, outcome_info in market_data.items():
                if outcome_name != 'question':
                    ask_price = outcome_info.get('best_ask')
                    if not ask_price:
                        is_market_valid = False
                        break
                    total_cost += ask_price
            
            if not is_market_valid:
                continue
            
            fee = self.estimator.estimated_cost(total_cost)
            if total_cost + fee < 1.00:
                self.signals.append(
                                        {
                                        "market_id": market_id, 
                                        'market_type': market_data['question'], 
                                        'total_cost': total_cost + fee, 
                                        'expected_profit': 1 - (total_cost + fee)
                                        }
                                     )
    
class CostEstimator:
    def __init__(self):
        """
        Initialize the expected taker fee and slippage for Polymarket. 
        Using default hardcoded values for the MVP stage.
        """
        self.default_slippage = 0.005
        self.taker_fee = 0.002

    def estimated_cost(self, total_value):
        """
        Calculate the expected fee and slippage costs for a given trade value.
        @param total_value: float, the total value of the trade.
        @return: float, the total estimated cost (slippage + taker fee).
        """
        slippage_cost = total_value * self.default_slippage
        fee_cost = total_value * self.taker_fee

        return slippage_cost + fee_cost
        