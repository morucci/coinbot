# CoinBot

CoinBot is a set of tools to automate multi crypto currencies
trading. It is based on 3 tools:

1. `fetcher` to get historical data from the exchange
2. `decider` to process historical data to find new trades or update
   existing ones
3. `trader` to manage the trades (trading plan) and the capital (money
   management)

The first trading strategy is a daily trend following strategy that
starts on bollinger bands breakout when the coin has already its EMA20
on top of the EMA50.

The trend is followed according to an ATR stop loss and 50% profit is
taken when 1R is reached to allow the system to continue to have
capital to invest. R = entry - initial stop.

The sizing of the position is done according to the maximum risk
allowed per trade. For example if we allow only 1% risk on our
capital, the position size will be: (capital * 1%) / R.

The number of positions at risk will be a parameter of the `trader`
tool. For example, if we go with 5 positions at risk, we have a
permanent 5% risk for the whole portfolio.

As soon as a position reaches 1R, the stop loss is put at the entry
level and the position is no more considered at risk and we can take
a new one at risk.

We'll implement the `trader` tool first and then the `fetcher` and
`decider`.

## fetcher

TBD

## decider

TBD

## trader

`trader` is using the Binance exchange to take advantage of the OCO
orders and the good liquidity of this exchange. If volunteers want to
support other exchanges, PR are welcome.

`trader` is a daemon program (running all the time). We interact with
it through interactive commands:

* `trade BNBBTC 0.0022066 0.00233` to create a trade on the BNB/BTC
  pair as soon as the price is above 0.00233 BTC with an initial stop
  loss at 0.0022066 BTC.
* `positions` lists current positions.
* `trades` lists current trades.
* `orders` lists current orders.
* `capital` displays current realized capital. Or set the allocated
  capital if an argument is passed.
* `risk` displays current risk and global allowed risk.
* `stop BNBBTC 0.0025` chnage the stop loss level for a trade. If the
  trade is already an active position, the stop loss is chnaged on the
  exchange. If the trade isn't a position, the position size is
  recomputed according to the new stop loss and the current realized
  capital.
* `close BNBBTC` closes a trade on the BNB/BTC pair by canceling all
  the open orders and issuing a market order if the trade is an open
  position else it just cancels the trade.
* `save` the current state of the trades.
* `exit` without saving. To exit and save, just issue a `Ctrl-D`.

A trade can have the following states:

* `entry` waiting for the trade to become a position by having the
  entry order executed (1 buy stop-limit). That's the initial state
  when a `trade` command has been issued.
* `suspended` waiting for a new available position when the maximum
  number of risky positions are at risk.
* `risky` when the position is between the stop loss and the R1 level
  (entry + 1R). It means there are 2 orders for this state: one OCO
  for 50% of the position (limit at R1 and stop) and the other 50%
  with a stop.
* `trendy` when the position has already reached the R1 level so there
  is only 50% remaining of the initial position size. There is only
  one stop order in this state and it is at the minimum on the entry
  level.
* `exited` when there is no more position and no more orders on the
  market. It can happen after a `close` command or a stop level has
  been reached.

`trader` manages the capital allocated to the trading. If there is
more on the account, it manages only the part that has been
allocated. When there are gains or losses, the capital is adjusted
automatically to benefit from compound interests.

## Current restrictions

* hardcoded BTC as the base crypto.
* can have only one trade per pair on the account. If you trade
  manually on the same pair and the same account, there will be
  troubles.
* hardcoded risk per trade at 1%.
* hardcoded 5 trades max at risk.
