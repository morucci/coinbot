#!/usr/bin/env python

'''
'''


import importlib
import json
import re
import readline
import sys

from binance.client import Client

ENTRY = 'entry'
SUSPENDED = 'suspended'
RISKY = 'risky'
TRENDY = 'trendy'
EXITED = 'exited'


def convert(arg):
    try:
        return int(arg)
    except ValueError:
        try:
            return float(arg)
        except ValueError:
            return arg


def parse_line(line):
    args = re.split(r'\s+', line)
    return [convert(arg) for arg in args]


def input_loop(app, executor_cls):
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode emacs')
    # Use the tab key for completion
    readline.parse_and_bind('tab: complete')

    try:
        readline.read_history_file('.trader_history')
    except Exception:
        pass

    executor = executor_cls(app)
    readline.set_completer(executor.completer)

    while True:
        try:
            line = input('$ ')
            if line != '':
                executor.process_args(parse_line(line))
        except KeyboardInterrupt:
            print('\nInterrupted')
        except EOFError:
            print()
            break

    app.save_data()
    readline.write_history_file('.trader_history')


def load_trading_plan(module_name):
    if module_name[-3:] == '.py':
        module_name = module_name[:-3]
        print("Loding module %s" % module_name)
    module = importlib.import_module(module_name)
    return module.TradingPlan


class Trade(object):
    def __init__(self, pair=None, entry=None, stop=None, order=None,
                 stop_order=None, amount=None, capital=None, status=None,
                 data=None):
        if data:
            self.__dict__ = data
        else:
            self.pair = pair
            self.entry = entry
            self.stop = stop
            self.order = order
            self.stop_order = stop_order
            self.amount = amount
            self.capital = capital
            self.status = status

    def validate_order(self, client):
        if self.order is None:
            orders = client.get_open_orders(symbol=self.pair)
            if len(orders) > 0:
                self.order = orders[0]
                if len(orders) > 1:
                    print('Warning: %d orders for %s' %
                          (len(orders, self.pair)))
        print(self.order)
        return self

    def __str__(self):
        return ('%s amount=%s stop=%s entry=%s [%s] order=%s' %
                (self.pair, self.amount, self.stop,
                 self.entry,
                 self.status, '%s(%s)' % (self.order['type'],
                                          self.order['orderId'])
                 if self.order else 'NONE'))


class TraderApp(object):
    def __init__(self, key, secret):
        self.client = Client(key, secret)
        self.load_data()

    def load_data(self, fname="trading-data.json"):
        try:
            with open(fname) as f:
                data = json.load(f)
            self.trades = [Trade(data=d).validate_order(self.client)
                           for d in data['trades']]
            self.capital = data['capital']
        except FileNotFoundError:
            self.trades = []
            self.capital = 0

    def save_data(self, fname="trading-data.json"):
        data = {'trades': [t.__dict__ for t in self.trades],
                'capital': self.capital,
                }
        with open(fname, 'w') as f:
            json.dump(data, f)

    def get_capital(self):
        btc_asset = self.client.get_asset_balance('BTC')
        return float(btc_asset['free']) + float(btc_asset['locked'])

    def new_trade(self, pair, stop, entry, amount):
        self.trades.append(Trade(pair=pair, stop=stop, entry=entry,
                                 amount=amount, status=ENTRY))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: %s <trading plan>' % sys.argv[0])
        sys.exit(1)
    (key, secret) = [line.rstrip("\n") for line in open("binance.txt")]
    app = TraderApp(key, secret)
    trading_plan_class = load_trading_plan(sys.argv[1])
    input_loop(app, trading_plan_class)

# trader.py ends here
