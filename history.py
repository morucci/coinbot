from binance.client import Client


class HistoryCrawler(object):
    def __init__(self, client):
        self.client = client
        self.get_pairs_list()
        self.kpairs = {}

    def _transform_klines(self, klines):
        # https://python-binance.readthedocs.io/en/latest/binance.html#binance.client.Client.get_klines
        candles = {}
        for tick in klines:
            candles.update({
                tick[0]: {
                    'open_time': tick[0],
                    'open': tick[1],
                    'high': tick[2],
                    'low': tick[3],
                    'close': tick[4],
                    'volume': tick[5],
                    'close_time': tick[6],
                    'quote_asset_volume': tick[7],
                    'number_of_trades': tick[8],
                }
            })
        return candles

    def get_pairs_list(self):
        self.pairs = [
            pair['symbol'] for pair in self.client.get_all_tickers() if
            'BTC' in pair['symbol']]

    def get_pair_klines(self, pair='NEOBTC', since="1 Nov, 2019", limit=31):
        klines = client.get_historical_klines(
            pair, self.client.KLINE_INTERVAL_1DAY, since, limit=limit)
        pair_candles = self._transform_klines(klines)
        self.kpairs.setdefault(pair, {})
        self.kpairs[pair].update(pair_candles)

    def get_all_pair_klines(self, since="1 Nov, 2019", limit=31):
        for pair in self.pairs[:2]:
            print("Getting klines for %s" % pair)
            self.get_pair_klines(pair)


if __name__ == "__main__":
    (key, secret) = [line.rstrip("\n") for line in open("binance.txt")]
    client = Client(key, secret)
    hc = HistoryCrawler(client)
    # hc.get_pair_klines('NEOBTC')
    hc.get_all_pair_klines()
    print(hc.kpairs)
