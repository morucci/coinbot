
'''
'''

import inspect


class TradingPlanBase(object):
    def __init__(self, client, cls):
        self.matches = []
        self.options = {x[0][:-4]: x[1]
                        for x in inspect.getmembers(cls, inspect.isfunction)
                        if x[0].endswith('_cmd')}
        print(self.options)

    def completer(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s for s in self.options
                                if s and s[0].startswith(text)]
            else:
                self.matches = self.options[:]
        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

    def process_args(self, args):
        try:
            self.options[args[0]](args[1:])
        except KeyError:
            print('Unknown command %s' % args[0])

# trading_plan.py ends here
