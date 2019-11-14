import os
import sys

from binance.client import Client
from binance.websockets import BinanceSocketManager


class HistoryCrawler(object):
    def __init__(self, client):
        self.client = client
        self.bm = BinanceSocketManager(
            self.client, user_timeout=60)
        self.kpairs = {}
        self.get_pairs_list()

    def _transform_klines(self, klines):
        # https://python-binance.readthedocs.io/en/latest/binance.html#binance.client.Client.get_klines
        candles = {}
        for tick in klines:
            candles.update({
                int(tick[0] / 1000): {
                    'open_time': int(tick[0] / 1000),
                    'open': tick[1],
                    'high': tick[2],
                    'low': tick[3],
                    'close': tick[4],
                    'volume': tick[5],
                    'close_time': int(tick[6] / 1000),
                    'quote_asset_volume': tick[7],
                    'number_of_trades': tick[8],
                }
            })
        return candles

    def get_pairs_list(self):
        self.pairs = [
            pair['symbol'] for pair in self.client.get_all_tickers() if
            'BTC' in pair['symbol']]
        # Reduce pairs amount for testing purpose
        self.pairs = self.pairs[:5]
        print('Discover BTC pairs: %s' % self.pairs)

    def get_pair_klines(self, pair='NEOBTC', since="1 Nov, 2019", limit=31):
        klines = client.get_historical_klines(
            pair, self.client.KLINE_INTERVAL_1DAY, since, limit=31)
        pair_candles = self._transform_klines(klines)
        self.kpairs.setdefault(pair, {})
        self.kpairs[pair].update(pair_candles)

    def get_all_pair_klines(self, since="1 Nov, 2019", limit=31):
        for pair in self.pairs:
            print("Getting klines for %s" % pair)
            self.get_pair_klines(pair, since, limit)

    def _process_websocket_message(self, msg):
        # We receive candle update every second so keep
        # the last update.
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams
        # print("stream: {} data: {}".format(msg['stream'], msg['data']))
        pair = msg['stream'].upper().split('@')[0]
        pld = msg['data']['k']
        candle = {
            int(pld['t'] / 1000): {
                'open_time': int(pld['t'] / 1000),
                'open': pld['o'],
                'high': pld['h'],
                'low': pld['l'],
                'close': pld['c'],
                'volume': pld['v'],
                'close_time': int(pld['T'] / 1000),
                'quote_asset_volume': pld['q'],
                'number_of_trades': pld['n'],
            }
        }
        ret = {pair: candle}
        print(ret)

    def start_kline_websockets(self):
        print('Starting websocket listener ...')
        self.ms = self.bm.start_multiplex_socket(
            ['%s@kline_1d' % pair.lower() for pair in self.pairs],
            self._process_websocket_message)


if __name__ == "__main__":
    creds_path = sys.argv[1]
    (key, secret) = [line.rstrip("\n") for
                     line in open(os.path.expanduser(creds_path))]
    client = Client(key, secret)
    hc = HistoryCrawler(client)
    hc.get_all_pair_klines(limit=31)
    hc.start_kline_websockets()
    hc.bm.start()
