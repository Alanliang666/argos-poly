class StrategyEngine():
    def __init__(self, orderbook):
        self.orderbook = orderbook
        self.signals = []
        self.estimator = CostEstimator()
    
    def arbitrage_formula(self):
        for market_id, market_data in self.orderbook.items():
            total_cost = 0
            for outcome_name, outcome_info in market_data.items():
                if outcome_name != 'question':
                    total_cost += outcome_info['best_ask']
            fee = self.estimator.calculate_estimated_cost(total_cost)
            if total_cost + fee < 1.00:
                self.signals.append(
                                {"market_id": market_id, 
                                'market_type': market_data['question'], 
                                'total_cost': total_cost + fee, 
                                'expected_profit': 1 - (total_cost + fee)
                            }
                        )
    
class CostEstimator():
    def __init__(self):
        self.default_slippage = 0.005
        self.taker_fee = 0.002

    def calculate_estimated_cost(self, total_size):
        slippage_cost = total_size * self.default_slippage
        fee_cost = total_size * self.taker_fee

        return slippage_cost + fee_cost
        