'''
'''

from trading_plan import TradingPlanBase


class NotEnoughCapitalError(Exception):
    pass


class TradingPlan(TradingPlanBase):
    def __init__(self, app):
        super().__init__(app, TradingPlan)
        self.reconcile()

    def reconcile(self):
        "Do the magic between the local data, active orders and positions"
        print('%f BTC' % self.app.capital)
        for t in self.app.trades:
            print(t)
            orders = self.app.get_orders(t.pair)
            print(orders)
            position = self.app.get_position(t.pair[:-3])
            print('%.2f %s' % (position, t.pair[:-3]))
            if t.status == 'entry' and len(orders) == 0:
                if position == 0:
                    self.buy(t.pair, t.stop, t.entry)
                else:
                    t.status = 'risky'
                    if self.reconcile_amount(position, t):
                        self.sell_risky(t)
            elif t.status == 'risky' and len(orders) == 0:
                if self.reconcile_amount(position, t):
                    self.sell_risky(t)
            elif t.status == 'trendy' and len(orders) == 0:
                self.sell_trendy(t)

    def reconcile_amount(self, position, trade):
        if position >= (trade.amount * 0.9) and position <= trade.amount:
            trade.amount = position
            return True
        else:
            print('Unable to reconcile amount %s from position %s for %s' %
                  (trade.amount, position, trade.pair))
            return False

    def buy(self, pair, stop, entry):
        count = 0
        for trade in self.app.trades:
            if trade.status == 'risky':
                count += 1
        if count < self.app.number:
            entry = round(entry, 8)
            limit = entry + (entry - stop) * 0.09
            risk = limit - stop
            amount = round(self.app.capital * self.app.risk / risk, 2)
            available_capital = self.app.get_available_capital()
            if (amount * limit > available_capital):
                print('position too big %s > %s' %
                      (amount * limit, available_capital))
                raise NotEnoughCapitalError
            else:
                print(pair, entry, limit, amount, amount * limit)
            try:
                order = self.app.buy_stop_limit(pair, entry, limit, amount)
                return (pair, stop, entry, amount, order)
            except Exception as e:
                print('Unable to place order: %s' % e)
                raise e
        else:
            print("Maximum risky positions reached.")

    def sell_risky(self, trade):
        "Sell 50% of the position at R1 or sell 100% at the STOP levvel"
        size = trade.amount / 2
        limit = trade.entry + (trade.entry - trade.stop)
        # We need 2 orders as we cannot have a different size for the
        # stop and limit orders in an OCO order.
        trade.order = self.app.sell_oco(trade.pair, trade.stop, limit, size)
        trade.stop_order = self.app.sell_stop(trade.pair, trade.stop, size)

    def trade_cmd(self, args):
        if len(args) != 3:
            print('Usage: trade <pair> <stop level> <entry level>')
        else:
            try:
                (pair, stop, entry, amount, order) = self.buy(args[0],
                                                              args[1],
                                                              args[2])
                if order:
                    trade = self.app.new_trade(pair, stop, entry, amount,
                                               order)
                    print(trade)
            except Exception:
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
