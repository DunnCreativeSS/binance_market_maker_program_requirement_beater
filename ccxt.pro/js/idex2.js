'use strict';

//  ---------------------------------------------------------------------------

const ccxt = require ('ccxt');
const { InvalidNonce } = require ('ccxt/js/base/errors');
const { ArrayCache, ArrayCacheBySymbolById } = require ('./base/Cache');

//  ---------------------------------------------------------------------------

module.exports = class idex2 extends ccxt.idex2 {
    describe () {
        return this.deepExtend (super.describe (), {
            'has': {
                'ws': true,
                'watchOrderBook': true,
                'watchTrades': true,
                'watchOHLCV': true,
                'watchTicker': true,
                'watchTickers': false, // for now
                'watchOrders': true,
                'watchTransactions': true,
            },
            'urls': {
                'test': {
                    'ws': 'wss://websocket-sandbox.idex.io/v1',
                },
                'api': {},
            },
            'api': {
                'private': {
                    'get': [
                        'wsToken',
                    ],
                },
            },
            'options': {
                'tradesLimit': 1000,
                'ordersLimit': 1000,
                'OHLCVLimit': 1000,
                'watchOrderBookLimit': 1000, // default limit
                'orderBookSubscriptions': {},
                'token': undefined,
                'fetchOrderBookSnapshotMaxAttempts': 3,
            },
        });
    }

    async subscribe (subscribeObject, messageHash, subscription = true) {
        const url = this.urls['test']['ws'];
        const request = {
            'method': 'subscribe',
            'subscriptions': [
                subscribeObject,
            ],
        };
        return await this.watch (url, messageHash, request, messageHash, subscription);
    }

    async subscribePrivate (subscribeObject, messageHash) {
        const token = await this.authenticate ();
        const url = this.urls['test']['ws'];
        const request = {
            'method': 'subscribe',
            'token': token,
            'subscriptions': [
                subscribeObject,
            ],
        };
        return await this.watch (url, messageHash, request, messageHash);
    }

    async watchTicker (symbol, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const name = 'tickers';
        const subscribeObject = {
            'name': name,
            'markets': [ market['id'] ],
        };
        const messageHash = name + ':' + market['id'];
        return await this.subscribe (this.extend (subscribeObject, params), messageHash);
    }

    handleTicker (client, message) {
        // { type: 'tickers',
        //   data:
        //    { m: 'DIL-ETH',
        //      t: 1599213946045,
        //      o: '0.09699020',
        //      h: '0.10301548',
        //      l: '0.09577222',
        //      c: '0.09907311',
        //      Q: '1.32723120',
        //      v: '297.80667468',
        //      q: '29.52142669',
        //      P: '2.14',
        //      n: 197,
        //      a: '0.09912245',
        //      b: '0.09686980',
        //      u: 5870 } }
        const type = this.safeString (message, 'type');
        const data = this.safeValue (message, 'data');
        const marketId = this.safeString (data, 'm');
        let symbol = undefined;
        if (marketId in this.markets_by_id) {
            symbol = this.markets_by_id[marketId]['symbol'];
        }
        const messageHash = type + ':' + marketId;
        const timestamp = this.safeInteger (data, 't');
        const close = this.safeFloat (data, 'c');
        const percentage = this.safeFloat (data, 'P');
        let change = undefined;
        if ((percentage !== undefined) && (close !== undefined)) {
            change = close * percentage;
        }
        const ticker = {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'high': this.safeFloat (data, 'h'),
            'low': this.safeFloat (data, 'l'),
            'bid': this.safeFloat (data, 'b'),
            'bidVolume': undefined,
            'ask': this.safeFloat (data, 'a'),
            'askVolume': undefined,
            'vwap': undefined,
            'open': this.safeFloat (data, 'o'),
            'close': close,
            'last': close,
            'previousClose': undefined,
            'change': change,
            'percentage': percentage,
            'average': undefined,
            'baseVolume': this.safeFloat (data, 'v'),
            'quoteVolume': this.safeFloat (data, 'q'),
            'info': message,
        };
        client.resolve (ticker, messageHash);
    }

    async watchTrades (symbol, since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const name = 'trades';
        const subscribeObject = {
            'name': name,
            'markets': [ market['id'] ],
        };
        const messageHash = name + ':' + market['id'];
        const future = this.subscribe (subscribeObject, messageHash);
        return await this.after (future, this.filterBySinceLimit, since, limit);
    }

    handleTrade (client, message) {
        const type = this.safeString (message, 'type');
        const data = this.safeValue (message, 'data');
        const marketId = this.safeString (data, 'm');
        const messageHash = type + ':' + marketId;
        const trade = this.parseWsTrade (data);
        const keys = Object.keys (this.trades);
        const length = keys.length;
        if (length === 0) {
            const limit = this.safeInteger (this.options, 'tradesLimit');
            this.trades = new ArrayCacheBySymbolById (limit);
        }
        const trades = this.trades;
        trades.append (trade);
        client.resolve (trades, messageHash);
    }

    parseWsTrade (trade) {
        // public trades
        // { m: 'DIL-ETH',
        //   i: '897ecae6-4b75-368a-ac00-be555e6ad65f',
        //   p: '0.09696995',
        //   q: '2.00000000',
        //   Q: '0.19393990',
        //   t: 1599504616247,
        //   s: 'buy',
        //   u: 6620 }
        // private trades
        // { i: 'ee253d78-88be-37ed-a61c-a36395c2ce48',
        //   p: '0.09925382',
        //   q: '0.15000000',
        //   Q: '0.01488807',
        //   t: 1599499129369,
        //   s: 'sell',
        //   u: 6603,
        //   f: '0.00030000',
        //   a: 'DIL',
        //   g: '0.00856110',
        //   l: 'maker',
        //   S: 'pending' }
        const marketId = this.safeString (trade, 'm');
        let symbol = undefined;
        if (marketId in this.markets_by_id) {
            symbol = this.markets_by_id[marketId]['symbol'];
        }
        const id = this.safeString (trade, 'i');
        const price = this.safeFloat (trade, 'p');
        const amount = this.safeFloat (trade, 'q');
        const cost = this.safeFloat (trade, 'Q');
        const timestamp = this.safeInteger (trade, 't');
        const side = this.safeString (trade, 's');
        const fee = {
            'currency': this.safeString (trade, 'a'),
            'cost': this.safeFloat (trade, 'f'),
        };
        const takerOrMarker = this.safeString (trade, 'l');
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'symbol': symbol,
            'id': id,
            'order': undefined,
            'type': undefined,
            'takerOrMaker': takerOrMarker,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        };
    }

    async watchOHLCV (symbol, timeframe = '1m', since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const name = 'candles';
        const interval = this.timeframes[timeframe];
        const subscribeObject = {
            'name': name,
            'markets': [ market['id'] ],
            'interval': interval,
        };
        const messageHash = name + ':' + market['id'];
        const future = this.subscribe (subscribeObject, messageHash);
        return await this.after (future, this.filterBySinceLimit, since, limit);
    }

    handleOHLCV (client, message) {
        // { type: 'candles',
        //   data:
        //    { m: 'DIL-ETH',
        //      t: 1599477340109,
        //      i: '1m',
        //      s: 1599477300000,
        //      e: 1599477360000,
        //      o: '0.09911040',
        //      h: '0.09911040',
        //      l: '0.09911040',
        //      c: '0.09911040',
        //      v: '0.15000000',
        //      n: 1,
        //      u: 6531 } }
        const type = this.safeString (message, 'type');
        const data = this.safeValue (message, 'data');
        const marketId = this.safeString (data, 'm');
        const messageHash = type + ':' + marketId;
        const parsed = [
            this.safeInteger (data, 's'),
            this.safeFloat (data, 'o'),
            this.safeFloat (data, 'h'),
            this.safeFloat (data, 'l'),
            this.safeFloat (data, 'c'),
            this.safeFloat (data, 'v'),
        ];
        let symbol = undefined;
        if (marketId in this.markets_by_id) {
            symbol = this.markets_by_id[marketId][symbol];
        }
        const interval = this.safeString (data, 'i');
        const timeframe = this.findTimeframe (interval);
        // TODO: move to base class
        this.ohlcvs[symbol] = this.safeValue (this.ohlcvs, symbol, {});
        let stored = this.safeValue (this.ohlcvs[symbol], timeframe);
        if (stored === undefined) {
            const limit = this.safeInteger (this.options, 'OHLCVLimit', 1000);
            stored = new ArrayCache (limit);
            this.ohlcvs[symbol][timeframe] = stored;
        }
        const length = stored.length;
        if (length && (parsed[0] === stored[length - 1][0])) {
            stored[length - 1] = parsed;
        } else {
            stored.append (parsed);
        }
        client.resolve (stored, messageHash);
    }

    handleSubscribeMessage (client, message) {
        // {
        //   "type": "subscriptions",
        //   "subscriptions": [
        //     {
        //       "name": "l2orderbook",
        //       "markets": [
        //         "DIL-ETH"
        //       ]
        //     }
        //   ]
        // }
        const subscriptions = this.safeValue (message, 'subscriptions');
        for (let i = 0; i < subscriptions.length; i++) {
            const subscription = subscriptions[i];
            const name = this.safeString (subscription, 'name');
            if (name === 'l2orderbook') {
                const markets = this.safeValue (subscription, 'markets');
                for (let j = 0; j < markets.length; j++) {
                    const marketId = markets[j];
                    const orderBookSubscriptions = this.safeValue (this.options, 'orderBookSubscriptions', {});
                    if (!(marketId in orderBookSubscriptions) && (marketId in this.markets_by_id)) {
                        const symbol = this.markets_by_id[marketId]['symbol'];
                        if (!(symbol in this.orderbooks)) {
                            const orderbook = this.countedOrderBook ({});
                            orderbook.cache = [];
                            this.orderbooks[symbol] = orderbook;
                        }
                        this.spawn (this.fetchOrderBookSnapshot, client, symbol);
                    }
                }
                break;
            }
        }
    }

    async fetchOrderBookSnapshot (client, symbol, params = {}) {
        const orderbook = this.orderbooks[symbol];
        const market = this.market (symbol);
        const messageHash = 'l2orderbook' + ':' + market['id'];
        const subscription = client.subscriptions[messageHash];
        const maxAttempts = this.safeInteger (this.options, 'fetchOrderBookSnapshotMaxAttempts', 3);
        subscription['fetchingOrderBookSnapshot'] = true;
        try {
            const limit = this.safeInteger (subscription, 'limit', 0);
            // 3. Request a level-2 order book snapshot for the market from the REST API Order Books endpoint with limit set to 0.
            const snapshot = await this.fetchOrderBook (symbol, limit);
            const firstBuffered = this.safeValue (orderbook.cache, 0);
            const firstData = this.safeValue (firstBuffered, 'data');
            const firstNonce = this.safeInteger (firstData, 'u');
            const length = orderbook.cache.length;
            const lastBuffered = this.safeValue (orderbook.cache, length - 1);
            const lastData = this.safeValue (lastBuffered, 'data');
            const lastNonce = this.safeInteger (lastData, 'u');
            // ensure the snapshot is inside the range of our cached messages
            const bothExist = (firstNonce !== undefined) && (lastNonce !== undefined);
            if (bothExist && (snapshot['nonce'] > firstNonce) && (snapshot['nonce'] < lastNonce)) {
                orderbook.reset (snapshot);
                for (let i = 0; i < orderbook.cache.length; i++) {
                    const message = orderbook.cache[i];
                    const data = this.safeValue (message, 'data');
                    const u = this.safeInteger (data, 'u');
                    if (u > orderbook['nonce']) {
                        // 5. Discard all order book update messages with sequence numbers less than or equal to the snapshot sequence number.
                        // 6. Apply the remaining buffered order book update messages and any incoming order book update messages to the order book snapshot.
                        this.handleOrderBookMessage (client, message, orderbook);
                    }
                }
                subscription['fetchingOrderBookSnapshot'] = false;
                client.resolve (orderbook, messageHash);
            } else {
                // 4. If the sequence in the order book snapshot is less than the sequence of the
                //    first buffered order book update message, discard the order book snapshot and retry step 3.
                subscription['numAttempts'] = subscription['numAttempts'] + 1;
                if (subscription['numAttempts'] < maxAttempts) {
                    this.delay (this.rateLimit, this.fetchOrderBookSnapshot, client, symbol);
                } else {
                    throw new InvalidNonce (this.id + ' failed to synchronize WebSocket feed with the snapshot for symbol ' + symbol + ' in ' + maxAttempts.toString () + ' attempts');
                }
            }
        } catch (e) {
            subscription['fetchingOrderBookSnapshot'] = false;
            client.reject (e, messageHash);
        }
    }

    async watchOrderBook (symbol, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const name = 'l2orderbook';
        const subscribeObject = {
            'name': name,
            'markets': [ market['id'] ],
        };
        const messageHash = name + ':' + market['id'];
        const subscription = {
            'fetchingOrderBookSnapshot': false,
            'numAttempts': 0,
            'limit': 0,  // get the complete order book snapshot
        };
        // 1. Connect to the WebSocket API endpoint and subscribe to the L2 Order Book for the target market.
        const future = this.subscribe (subscribeObject, messageHash, subscription);
        return await this.after (future, this.limitOrderBook, symbol, limit);
    }

    handleOrderBook (client, message) {
        const data = this.safeValue (message, 'data');
        const marketId = this.safeString (data, 'm');
        let symbol = undefined;
        if (marketId in this.markets_by_id) {
            symbol = this.markets_by_id[marketId]['symbol'];
        }
        const orderbook = this.orderbooks[symbol];
        if (orderbook['nonce'] === undefined) {
            // 2. Buffer the incoming order book update subscription messages.
            orderbook.cache.push (message);
        } else {
            this.handleOrderBookMessage (client, message, orderbook);
        }
    }

    handleOrderBookMessage (client, message, orderbook) {
        // {
        //   "type": "l2orderbook",
        //   "data": {
        //     "m": "DIL-ETH",
        //     "t": 1600197205037,
        //     "u": 94116643,
        //     "b": [
        //       [
        //         "0.09662187",
        //         "0.00000000",
        //         0
        //       ]
        //     ],
        //     "a": []
        //   }
        // }
        const type = this.safeString (message, 'type');
        const data = this.safeValue (message, 'data');
        const marketId = this.safeString (data, 'm');
        const messageHash = type + ':' + marketId;
        const nonce = this.safeInteger (data, 'u');
        const timestamp = this.safeInteger (data, 't');
        const bids = this.safeValue (data, 'b');
        const asks = this.safeValue (data, 'a');
        this.handleDeltas (orderbook['bids'], bids);
        this.handleDeltas (orderbook['asks'], asks);
        orderbook['nonce'] = nonce;
        orderbook['timestamp'] = timestamp;
        orderbook['datetime'] = this.iso8601 (timestamp);
        client.resolve (orderbook, messageHash);
    }

    handleDelta (bookside, delta) {
        const price = this.safeFloat (delta, 0);
        const amount = this.safeFloat (delta, 1);
        const count = this.safeInteger (delta, 2);
        bookside.store (price, amount, count);
    }

    handleDeltas (bookside, deltas) {
        for (let i = 0; i < deltas.length; i++) {
            this.handleDelta (bookside, deltas[i]);
        }
    }

    async authenticate (params = {}) {
        const time = this.seconds ();
        const lastAuthenticatedTime = this.safeInteger (this.options, 'lastAuthenticatedTime', 0);
        if (time - lastAuthenticatedTime > 900) {
            const request = {
                'wallet': this.walletAddress,
                'nonce': this.uuidv1 (),
            };
            const response = await this.privateGetWsToken (this.extend (request, params));
            this.options['lastAuthenticatedTime'] = time;
            this.options['token'] = this.safeString (response, 'token');
        }
        return this.options['token'];
    }

    async watchOrders (symbol = undefined, since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const name = 'orders';
        const subscribeObject = {
            'name': name,
        };
        let messageHash = name;
        if (symbol !== undefined) {
            const marketId = this.marketId (symbol);
            subscribeObject['markets'] = [ marketId ];
            messageHash = name + ':' + marketId;
        }
        const future = this.subscribePrivate (subscribeObject, messageHash);
        return await this.after (future, this.filterBySinceLimit, since, limit);
    }

    handleOrder (client, message) {
        // {
        //   "type": "orders",
        //   "data": {
        //     "m": "DIL-ETH",
        //     "i": "8f75dd30-f12d-11ea-b63c-df3381b4b5b4",
        //     "w": "0x0AB991497116f7F5532a4c2f4f7B1784488628e1",
        //     "t": 1599498857138,
        //     "T": 1599498857092,
        //     "x": "fill",
        //     "X": "filled",
        //     "u": 67695627,
        //     "o": "limit",
        //     "S": "buy",
        //     "q": "0.15000000",
        //     "z": "0.15000000",
        //     "Z": "0.01486286",
        //     "v": "0.09908573",
        //     "p": "1.00000000",
        //     "f": "gtc",
        //     "V": "2",
        //     "F": [
        //       {
        //         "i": "5cdc6d14-bc35-3279-ab5e-40d654ca1523",
        //         "p": "0.09908577",
        //         "q": "0.15000000",
        //         "Q": "0.01486286",
        //         "t": 1599498857092,
        //         "s": "sell",
        //         "u": 6600,
        //         "f": "0.00030000",
        //         "a": "DIL",
        //         "g": "0.00856977",
        //         "l": "maker",
        //         "S": "pending"
        //       }
        //     ]
        //   }
        // }
        const type = this.safeString (message, 'type');
        const order = this.safeValue (message, 'data');
        const marketId = this.safeString (order, 'm');
        const timestamp = this.safeInteger (order, 't');
        const fills = this.safeValue (order, 'F');
        const trades = [];
        for (let i = 0; i < fills.length; i++) {
            trades.push (this.parseWsTrade (fills[i]));
        }
        const id = this.safeString (order, 'i');
        let symbol = undefined;
        const side = this.safeString (order, 's');
        if (marketId in this.markets_by_id) {
            symbol = this.markets_by_id[marketId]['symbol'];
        }
        const orderType = this.safeString (order, 'o');
        const amount = this.safeFloat (order, 'q');
        const filled = this.safeFloat (order, 'z');
        let remaining = undefined;
        if ((amount !== undefined) && (filled !== undefined)) {
            remaining = amount - filled;
        }
        const average = this.safeFloat (order, 'v');
        const price = this.safeFloat (order, 'price', average);  // for market orders
        let cost = undefined;
        if ((amount !== undefined) && (price !== undefined)) {
            cost = amount * price;
        }
        const rawStatus = this.safeString (order, 'X');
        const status = this.parseOrderStatus (rawStatus);
        const fee = {
            'currency': undefined,
            'cost': undefined,
        };
        let lastTrade = undefined;
        for (let i = 0; i < trades.length; i++) {
            lastTrade = trades[i];
            fee['currency'] = lastTrade['fee']['currency'];
            fee['cost'] = this.sum (fee['cost'], lastTrade['fee']['cost']);
        }
        const lastTradeTimestamp = this.safeInteger (lastTrade, 'timestamp');
        const parsedOrder = {
            'info': message,
            'id': id,
            'clientOrderId': undefined,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': orderType,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': trades,
        };
        if (this.orders === undefined) {
            const limit = this.safeInteger (this.options, 'ordersLimit', 1000);
            this.orders = new ArrayCacheBySymbolById (limit);
        }
        const orders = this.orders;
        orders.append (parsedOrder);
        const symbolSpecificMessageHash = type + ':' + marketId;
        client.resolve (orders, symbolSpecificMessageHash);
        client.resolve (orders, type);
    }

    async watchTransactions (code = undefined, since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const name = 'balances';
        const subscribeObject = {
            'name': name,
        };
        let messageHash = name;
        if (code !== undefined) {
            messageHash = name + ':' + code;
        }
        const future = this.subscribePrivate (subscribeObject, messageHash);
        return await this.after (future, this.filterBySinceLimit, since, limit);
    }

    handleTransaction (client, message) {
        // Update Speed: Real time, updates on any deposit or withdrawal of the wallet
        // { type: 'balances',
        //   data:
        //    { w: '0x0AB991497116f7F5532a4c2f4f7B1784488628e1',
        //      a: 'ETH',
        //      q: '0.11198667',
        //      f: '0.11198667',
        //      l: '0.00000000',
        //      d: '0.00' } }
        const type = this.safeString (message, 'type');
        const data = this.safeValue (message, 'data');
        const currencyId = this.safeString (data, 'a');
        const messageHash = type + ':' + currencyId;
        const code = this.safeCurrencyCode (currencyId);
        const address = this.safeString (data, 'w');
        const transaction = {
            'info': message,
            'id': undefined,
            'currency': code,
            'amount': undefined,
            'address': address,
            'addressTo': undefined,
            'addressFrom': undefined,
            'tag': undefined,
            'tagTo': undefined,
            'tagFrom': undefined,
            'status': 'ok',
            'type': undefined,
            'updated': undefined,
            'txid': undefined,
            'timestamp': undefined,
            'datetime': undefined,
            'fee': undefined,
        };
        if (!(code in this.transactions)) {
            const limit = this.safeInteger (this.options, 'transactionsLimit', 1000);
            this.transactions[code] = new ArrayCache (limit);
        }
        const transactions = this.transactions[code];
        transactions.append (transaction);
        client.resolve (transactions, messageHash);
        client.resolve (transactions, type);
    }

    handleMessage (client, message) {
        const type = this.safeString (message, 'type');
        const methods = {
            'tickers': this.handleTicker,
            'trades': this.handleTrade,
            'subscriptions': this.handleSubscribeMessage,
            'candles': this.handleOHLCV,
            'l2orderbook': this.handleOrderBook,
            'balances': this.handleTransaction,
            'orders': this.handleOrder,
        };
        if (type in methods) {
            const method = methods[type];
            method.call (this, client, message);
        }
    }
};
