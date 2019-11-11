'''
'''

from trading_plan import TradingPlanBase


class TradingPlan(TradingPlanBase):
    def __init__(self, client):
        super().__init__(client, TradingPlan)
        # readline completion
#         self.options = ('trade', 'positions', 'trades', 'orders',
#                         'capital', 'stop', 'close')

    def trade_cmd(self, *args):
        pass

# r1_tp.py ends here
