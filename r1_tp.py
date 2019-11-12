'''
'''

from trading_plan import TradingPlanBase


class TradingPlan(TradingPlanBase):
    def __init__(self, app):
        super().__init__(app, TradingPlan)

    def trade_cmd(self, args):
        pass

    def positions_cmd(self, args):
        pass

    def trades_cmd(self, args):
        for trade in self.app.trades:
            print(trade)

    def orders_cmd(self, args):
        pass

    def capital_cmd(self, args):
        if len(args) > 0:
            self.app.set_capital(args[0])
        print('Capital: %f BTC' % self.app.get_capital())

    def risk_cmd(self, args):
        print('Global risk: %.2f%%' % (self.app.risk * self.app.number * 100))
        print('Current risk: %.2f%%' %
              (self.get_engaged_capital() / self.app.get_capital() * 100))

    def stop_cmd(self, args):
        pass

    def close_cmd(self, args):
        pass

# r1_tp.py ends here
