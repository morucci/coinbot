#!/usr/bin/env python

'''
'''


import importlib
import re
import readline
import sys

from binance.client import Client


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


def input_loop(ib, executor_cls):
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode emacs')
    # Use the tab key for completion
    readline.parse_and_bind('tab: complete')

    try:
        readline.read_history_file('.trader_history')
    except Exception:
        pass

    executor = executor_cls(ib)
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

    readline.write_history_file('.trader_history')


def load_trading_plan(module_name):
    if module_name[-3:] == '.py':
        module_name = module_name[:-3]
        print("Loding module %s" % module_name)
    module = importlib.import_module(module_name)
    return module.TradingPlan


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: %s <trading plan>' % sys.argv[0])
        sys.exit(1)
    (key, secret) = [line.rstrip("\n") for line in open("binance.txt")]
    client = Client(key, secret)
    trading_plan = load_trading_plan(sys.argv[1])
    input_loop(client, trading_plan)

# trader.py ends here
