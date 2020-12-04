This is the README for the binance_market_maker_program_requirement_beater repo, which has been made private. If you'd like access, click the 'sponsors' button near the top and follow the directions :)

# What is it

This bot automates making markets on Binance.

Where other market making bots fail (ie. BitMex, Deribit, other attempts I’ve made in the past) is by counting on the market to not be volatile. Where this bot wins is by finding markets where we can soak up profits in the volatility by taking those profits from the spread itself, where on BitMex and Deribit these spreads ar 0.25$ of a BTC, some smaller markets on Binance have 1%.. 2%… 5% spreads, and greater-than-average volumes.

You’ll want to have about $20 per market pair it’s looking to trade, in the base asset (BTC, BNB, ETH, etc…). It will look to trade more markets if the targetSpread, targetVolDiv, targetVolMult are higher. The more total funds in a particular base asset there are, the higher value the orders will have.

If for whatever reason a market pair leaves the universe scope of considered pairs, it will continue selling that asset with the same sell logic (on the quoteAsset+BNB market, or BTC then ETH if BNB isn’t available), while pausing buying it.

I don’t have enough personal funds available to run the bot, but I can get a good amount of income if I share it and people use my ref link. targetOrderSizeMult exists so that people can compete using the same bot on the same markets without it just outbidding the other bot constantly, as you can set a % of your order size to ignore when there’s a bid or ask better than yours. When the volume that beats your price is higher than the -

order size * this multiplier,

it’ll re-enter the market.

‘At the current time Binance rate limits are: 1200 requests per minute. 10 orders per second. 100,000 orders per 24hrs.’

There are no limits for unfilled orders, and at most it’ll make about 6x20 or so pairs x 2 orders, 1 cancel and 1 re-post a minute, along with checking balance and getting order books so a total of about ~500 a minute — not close to 1200 :)

On that note I’ve only been trading one pair, averaging 42 orders an hour or ~1000 per day, again by about 20 pairs would be 20 000 orders per day — a bit shy of 100k.

## To use:

1. (please do) sign up for Binance using my ref link: https://www.binance.com/?ref=27039658

2. Place your Binance API key and secret in binance.js

3. Optionally change the targetSpread, targetVolDiv, targetVolMult, targetOrderSizeMult

4. Install NPM and Node

5. Clone this repo, cd into directory

6. Run npm i binance-api-node

7. Run node binance.js

## API Rate Limiting?

The first FUD someone might say is that this will lock your API for too many unfilled orders or too many interactions.

‘At the current time Binance rate limits are: 1200 requests per minute. 10 orders per second. 100,000 orders per 24hrs.’

There are no limits for unfilled orders, and at most it’ll make about 6x 20 or so pairs x 2 orders, 1 cancel and 1 re-post a minute, along with checking balance and getting order books so a total of about ~500 a minute — not close to 1200 :)

On that note I’ve only been trading three or so pairs at a time, averaging 42 orders an hour or ~1000 per day, again by about 20 pairs would be 20 000 orders per day — a bit shy of 100k.

# Conclusion

I was originally trading GNTBNB almost exclusively for testing, the first trade is screenshotted. I’ve since opened it up to trade anything it noticed it could trade, made the required spread lower, and let it run overnight. It’s lost a bit of value but it’s also held eth for awhile while not doing anything with it (due to the required spread % not being enough), but over 45 orders (excluding cancelled) with 0.00568192 balance (or so) I have 0.03090300 in volume — meaning that while it lost ~3% BTC and ~4% USD it traded the original 0.00568192 back and forth for 22–23 round trips @ 0.2% fees, beating the 4.5% fees it endured… with more careful settings it should perform better or at least act on less orders and capitalize higher spreads.

If you’re looking to start building your volume on Binance, the easiest way would be to put this bot to work and choose some safer settings to automate the spreads of a few pairs — after trading a few hours with 0.00568192 balance (or so) I have 0.03090300 in volume. While this strategy might not automate profits (at least out of the box), it does trade a whole heck of a lot. If you check Binance’s fee schedule, you’ll see that as you graduate levels of volume and hold BNB then you’ll be treated to lesser and lesser maker/taker fees, which might prove healthy should you have other strategies (especially high-frequency-trading) that would benefit from lesser fees — although the BNB requirements might be high, given the current value of a BNB has exploded. Again, should you use my invite code 27039658 or invite link I’ll get a tiny slice of the rewards, too!

Join Telegram for interactive support and a community!

Jarett Dunn, [21.03.19 15:35]
ok going to start a new set of conditions for a strategy using the bot, mark @ benchmark 2 Estimated Value： 0.00569181 BTC / $22.57

Jarett Dunn, [21.03.19 15:35]
note it held Eth during a major Eth crash

Jarett Dunn, [21.03.19 15:35]

Note: I’m available to re-write the bot for other exchanges, to build your volumes elsewhere.

