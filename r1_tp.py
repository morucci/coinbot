'''
'''

from trading_plan import TradingPlanBase


class TradingPlan(TradingPlanBase):
    def __init__(self, app):
        super().__init__(app, TradingPlan)

    def trade_cmd(self, args):
        if len(args) != 3:
            print('Usage: trade <pair> <stop level> <entry level>')
        else:
            count = 0
            for trade in self.app.trades:
                if trade.status == 'risky':
                    count += 1
            if count < self.app.number:
                pair = args[0]
                stop = args[1]
                entry = round(args[2], 8)
                limit = round(entry + (entry - stop) * 0.09, 6)
                risk = limit - stop
                amount = round(self.app.capital * self.app.risk / risk, 2)
                available_capital = self.app.get_available_capital()
                if (amount * limit > available_capital):
                    print('position too big %s > %s' %
                          (amount * limit, available_capital))
                    return
                else:
                    print(pair, entry, limit, amount, amount * limit)
                try:
                    order = self.app.buy_stop_limit(pair, entry, limit, amount)
                    trade = self.app.new_trade(pair, stop, entry, amount,
                                               order)
                    print(trade)
                except FileNotFoundError as e:
                    print('Unable to place order: %s' % e)

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
