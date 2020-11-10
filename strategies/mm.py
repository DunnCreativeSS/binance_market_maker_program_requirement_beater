

class Place_Orders( object ):
    def __init__( self, pprint, firstkey, lev, bm, client, multiprocessing, brokerKey, qty_div, orderRateLimit, max_skew_mult, get_precision, math, TP, SL, asyncio, sleep, threading, PrintException, ticksize_floor, ticksize_ceil, pairs, fifteens, tens, fives, threes, con_size, get_spot, equity_btc, positions, get_ticksize, vols, get_bbo, openorders, equity_usd, randomword, logger, PCT_LIM_LONG, PCT_LIM_SHORT, DECAY_POS_LIM, MIN_ORDER_SIZE, CONTRACT_SIZE, MAX_LAYERS, BTC_SYMBOL, RISK_CHARGE_VOL, BP ):
        self.BP = BP
        self.TP = TP
        self.SL = SL
        self.pprint = pprint
        self.lbo = {}
        self.lao = {}
        self.ask_ords = {}
        self.bid_ords = {}
        self.lev = lev
        self.firstkey = firstkey
        self.multiprocessing = multiprocessing
        self.brokerKey = brokerKey
        self.qty_div = qty_div
        self.get_precision = get_precision
        self.math = math
        self.pairs = pairs
        self.max_skew_mult = max_skew_mult
        self.creates = {}
        self.edits = {}
        self.cancels = {}
        self.goforit = True
        self.goforit2 = True
        self.slBlock = {}
        self.tradeBlock = {}
        for fut in self.pairs:
            self.cancels[fut] = False
            self.creates[fut] = False
            self.edits[fut] = False
            self.slBlock[fut] = False
            self.tradeBlock[fut] = False
            self.lbo[fut] = 0
            self.lao[fut] = 0
            self.ask_ords[fut] = []
            self.bid_ords[fut] = []
        self.sleep = sleep
        self.trades = {}
        self.asyncio = asyncio
        self.threading = threading
        self.start_threads = None
        self.num_threads = 0
        self.PrintException = PrintException
        self.ticksize_ceil = ticksize_ceil
        self.ticksize_floor = ticksize_floor
        self.PCT_LIM_LONG = PCT_LIM_LONG
        self.PCT_LIM_SHORT = PCT_LIM_SHORT
        self.DECAY_POS_LIM = DECAY_POS_LIM
        self.MIN_ORDER_SIZE = MIN_ORDER_SIZE
        self.CONTRACT_SIZE = CONTRACT_SIZE
        self.MAX_LAYERS = MAX_LAYERS
        self.BTC_SYMBOL = BTC_SYMBOL
        self.RISK_CHARGE_VOL = RISK_CHARGE_VOL

        self.fifteens = fifteens
        self.tens = tens
        self.fives = fives
        self.threes = threes
        self.con_size = con_size
        self.get_spot = get_spot
        self.client = client
        print('placekey: ' + self.client.apiKey)
        self.get_ticksize = get_ticksize
        self.get_bbo = get_bbo
        self.randomword = randomword
        self.logger = logger

        self.orderRateLimit = orderRateLimit
        self.openorders = openorders
        self.vols = vols
        self.equity_btc = equity_btc
        self.equity_usd = equity_usd
        self.positions = positions
        
        #conn_key = bm.start_multiplex_socket(['!ticker@arr'], self.process_m_message)
        self.bm = bm

        
        # then start the socket manager
        #self.bm.start()
    
        
    def start_user_thread(self):
        while True:
            try:
                self.bm.start_user_socket(self.process_message)
            except:
                self.PrintException(self.client.apiKey)
                self.sleep(5)

    def process_message(self, msg):
        try: 
            try:
                if 'data' in msg:
                    data = msg['data']
                else:
                    data = msg
            except:
                data = msg
            if data['e'] == 'ORDER_TRADE_UPDATE':
                fut = data['o']['s'].replace('USDT', '/USDT')
                #if 'BAT' in fut:
                #    self.pprint(fut)
                side = (data['o']["S"])
                qty = float(data['o']["q"])
                if side == 'SELL':
                    qty = qty * -1
                type = data['o']['x']
                price = float(data['o']["p"])
                try:
                    
                    ords        = [ o['id'] for o in self.openorders[fut] ]#if o['side'] == 'SELL' and o['type'] == 'NEW' ] 
                    if data['o']['i'] not in ords:
                        self.openorders[fut].append({'id':data['o']['i'], 'type': type, 'datetime': data['o']['T'], 'price': price, 'qty': qty, 'side': side})
                except:
                    self.openorders[fut] = []
                    ords        = [ o['id'] for o in self.openorders[fut] ]#if o['side'] == 'SELL' and o['type'] == 'NEW' ] 
                    if data['o']['i'] not in ords:
                        self.openorders[fut].append({'id':data['o']['i'], 'type': type, 'datetime': data['o']['T'], 'price': price, 'qty': qty, 'side': side})
                if type != 'NEW':
                    #self.pprint(type)
                    if fut in self.openorders:
                        for o in self.openorders[fut]:
                            if o['id'] == data['o']['i']:
                                self.openorders[fut].remove(o)
                #else:
                    
                    
                ask_ords        = [ o for o in self.openorders[fut] if o['side'] == 'SELL' and o['type'] == 'NEW' ] 
                bid_ords        = [ o for o in self.openorders[fut] if o['side'] == 'BUY' and o['type'] == 'NEW' ]
                #if 'BAT' in fut:
                #    for o in self.openorders[fut]:
                #        self.pprint(o)
                self.ask_ords[fut] = ask_ords
                self.bid_ords[fut] = bid_ords
                self.lbo[fut] = len(bid_ords)
                self.lao[fut] = len(ask_ords)
                cancel_oids = []
                if 3 < len( bid_ords ):
                    cancel_oids += [ o['id'] for o in bid_ords[ 3 : ]]
                if 3 < len( ask_ords ):
                    cancel_oids += [ o['id'] for o in ask_ords[ 3 : ]]
                if self.cancels[fut] == False:
                    self.cancels[fut] = True
                    if len(cancel_oids) > 0:#self.firstkey == self.client.apiKey and 
                        self.pprint(self.client.apiKey + ': cancel '  + fut + ': from ' + str(len(bid_ords)) + ' bid_ords and ' + str(len(ask_ords)) + ' asks, cancelling: ' + str(len(cancel_oids)))
                
                    for oid in cancel_oids:
                        
                        t = self.threading.Thread(target=self.cancel_them, args=(oid, fut,))
                        t.daemon = True
                        t.start()
                if 'BAT' in fut:# and self.firstkey == self.client.apiKey:
                    bat = len(self.bid_ords['BAT/USDT']) + len(self.ask_ords['BAT/USDT'])
                    if len(self.bid_ords['BAT/USDT']) > 2 or len(self.ask_ords['BAT/USDT']) > 2:
                        self.pprint(self.client.apiKey + ': lenorders BAT ' + str(bat))
                        #self.pprint(self.client.apiKey + ': lenaskorders BAT ' + str(len(self.ask_ords['BAT/USDT'])))
                if type == 'TRADE':
                    try:
                        self.trades[fut].append({'id':data['o']['i'], 'type': type, 'datetime': data['o']['T'], 'price': price, 'qty': qty, 'side': side})
                    except:
                        self.trades[fut] = []
                        self.trades[fut].append({'id':data['o']['i'], 'type': type, 'datetime': data['o']['T'], 'price': price, 'qty': qty, 'side': side})
                    try:
                        self.tradeBlock[fut] = True
                        t = self.threading.Thread(target=self.tradeUnblock, args=(fut,))
                        t.daemon = True
                        t.start()
                    except:
                        self.PrintException(self.client.apiKey)
            elif data['e'] == 'ACCOUNT_UPDATE':
                for bal in data['a']['B']:
                    if bal["a"] == 'USDT':
                        self.equity_usd = float(bal["wb"])

                        self.equity_btc = self.equity_usd / self.get_spot('BTC/USDT')
                        

                for pos in data['a']['P']:
                    pos['symbol'] = pos['s'].replace('USDT', '/USDT')
                    pos['entryPrice'] = pos['ep']
                    pos['unRealizedProfit'] = pos['up']
                    pos['positionAmt'] = pos['pa']
                    if pos['symbol'].split('USDT')[0] + '/USDT' in self.pairs:
                        pos['positionAmt'] = float(pos['positionAmt'])
                        pos['entryPrice'] = float(pos['entryPrice'])
                        pos['unRealizedProfit'] = float(pos['unRealizedProfit'])
                        pos['leverage'] = float(self.lev)
                        notional = self.math.fabs(pos['positionAmt']) * pos['entryPrice']
                        fee = self.feeRate * notional
                        notional = notional - fee
                        if notional > 0:
                            notionalplus = notional + pos['unRealizedProfit']
                            percent = ((notionalplus / notional) -1) * 100

                            pos['ROE'] = percent * pos['leverage']
                        else:
                            pos['ROE'] = 0

                        self.positions[client.apiKey][ pos['symbol'].split('USDT')[0] + '/USDT'] = pos

            else:
                self.pprint(data['e'])
        except:
            self.PrintException(self.client.apiKey)
    def run( self ):
        while  True:
            try:
                t = self.threading.Thread(target=self.start_user_thread, args=())
                t.daemon = True
                self.num_threads = self.num_threads + 1
                t.start()
                t = self.threading.Thread(target=self.failSafeReset, args=())
                t.daemon = True
                self.num_threads = self.num_threads + 1
                t.start()
                
            except:
                self.PrintException(self.client.apiKey)
            while True:
                try:
                    self.start_threads = self.threading.active_count() 
                    if self.client.apiKey == self.firstkey:
                        self.pprint(self.client.apiKey + ': start thread place_orders: ' + str(self.start_threads))
                    for fut in self.pairs:
                        try:
                            t = self.threading.Thread(target=self.place_orders, args=(fut,))
                            t.daemon = True
                            
                            t.start()
                        except:
                            self.PrintException(self.client.apiKey)
                    done = False
                    while done == False:
                        num_threads = self.threading.active_count()  - self.num_threads
                        if self.client.apiKey == self.firstkey:
                            abc=123#self.pprint('num thread place_orders: ' + str(num_threads) + ' and self.num_threads: ' + str(self.num_threads))
                        if num_threads < self.start_threads + len(self.pairs) / 3:
                            done = True
                            abc=123#self.pprint('restart threads...')
                            self.sleep(5)
                        else:
                            self.sleep(5)
                except:
                    self.PrintException(self.client.apiKey)
    def failSafeReset( self ):
        while True:
            try:
                t = self.threading.Timer(5, self.resetGoforit)
                t.daemon = True
                self.num_threads = self.num_threads + 1
                t.start()
                self.sleep(5)
            except:
                self.PrintException(self.client.apiKey)
                self.sleep(5)
        proc = self.threading.Thread(target=self.failSafeReset, args=())
        abc=123#self.pprint('4 proc')
        proc.start()
        proc.terminate() 
        sleep(5) 
    def resetGoforit2( self ):
        try:
            self.goforit2 = True
            self.pprint(self.client.apiKey + ': self.goforit2')
            self.num_threads = self.num_threads - 1

            return
        except:
            proc = self.threading.Thread(target=self.resetGoforit2, args=())
            self.PrintException(self.client.apiKey)
            
    def resetGoforit( self ):
        try:
            self.goforit = True
            #self.pprint(self.goforit)
            self.num_threads = self.num_threads - 1

            return
        except:
            proc = self.threading.Thread(target=self.resetGoforit, args=())
            abc=123#self.pprint('6 proc')
            proc.start()
            proc.terminate() 
            sleep(5)
    def tradeUnblock( self, fut ):
        self.sleep(2)
        #self.pprint('unblock trade ' + fut)
        self.tradeBlock[fut] = False
    def slUnblock( self, fut ):
        self.sleep(60 * 60)
        self.pprint(self.client.apiKey + ': unblock sl ' + fut)
        self.slBlock[fut] = False
    def place_orders( self, fut ):

        
        
        con_sz  = self.con_size        
        
        
        while True:
            
            try:
                try:
                    #self.pprint(fut + ': ' + str(self.positions[fut]['ROE']))
                    if self.positions[fut]['ROE'] > self.TP and self.positions[fut]['ROE'] != 0:
                        
                        #sleep(10)
                        direction = 'sell'
                        if self.positions[fut]['positionAmt'] < 0:
                            direction = 'buy'
                        qty = self.math.fabs(self.positions[fut]['positionAmt'])
                        self.creates[fut] = True
                        if self.client.apiKey == self.firstkey:
                            abc=123#self.pprint(str(qty) + ' ' + fut)
                        try:
                            self.create_order(  fut, "Market", direction, qty, None, {"newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)})
                        except Exception as e:
                            self.pprint(e)
                        if self.client.apiKey == self.firstkey:
                            self.pprint(self.client.apiKey + ': ' + fut + ' takeprofit! ' + str(self.positions[fut]['ROE']) + ' dir: ' + direction + ' qty ' + str(qty))
                        self.positions[fut]['ROE'] = 0
                    if self.positions[fut]['ROE'] < self.SL and self.positions[fut]['ROE'] != 0:
                        
                        direction = 'sell'
                        if self.positions[fut]['positionAmt'] < 0:
                            direction = 'buy'
                        qty = self.math.fabs(self.positions[fut]['positionAmt'])
                        self.creates[fut] = True
                        if self.client.apiKey == self.firstkey:
                            abc=123#self.pprint(str(qty) + ' ' + fut)
                        if self.client.apiKey == self.firstkey:
                            self.pprint(self.client.apiKey + ': ' + fut + ' stoploss! ' + str(self.positions[fut]['ROE']) + ' dir: ' + direction + ' qty ' + str(qty))
                        self.slBlock[fut] = True
                        t = self.threading.Thread(target=self.slUnblock, args=(fut,))
                        t.daemon = True
                        t.start()
                        try:
                            self.create_order(  fut, "Market", direction, qty, None, {"newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)})
                        except Exception as e:
                            self.pprint(e)
                        self.positions[fut]['ROE'] = 0
                except:
                    self.PrintException(self.client.apiKey)
                spot            = self.get_spot(fut)
                bal_btc         = self.equity_btc
                pos             = float(self.positions[ fut ][ 'positionAmt' ])
                pos_lim_long    = bal_btc * self.PCT_LIM_LONG * 20 #/ len(self.futures)
                pos_lim_short   = bal_btc * self.PCT_LIM_SHORT * 20 #/ len(self.futures)
                #self.pprint(pos_lim_long)
                #expi            = self.futures[ fut ][ 'expi_dt' ]
                #tte             = max( 0, ( expi - datetime.utcnow()).total_seconds() / SECONDS_IN_DAY )
                pos_decay       = 1.0 - self.math.exp( -self.DECAY_POS_LIM * 8035200 )
                pos_lim_long   *= pos_decay
                pos_lim_short  *= pos_decay
                pos_lim_long   -= pos
                pos_lim_short  += pos
                pos_lim_long    = max( 0, pos_lim_long  )
                pos_lim_short   = max( 0, pos_lim_short )
                
                min_order_size_btc = (self.MIN_ORDER_SIZE * self.CONTRACT_SIZE) / spot
                #self.pprint(min_order_size_btc) #0.0006833471711135484 0.08546200188472201
                qtybtc  = 1 / spot #(bal_btc * 20 / 500) / len(pairs)

                nbids   = self.MAX_LAYERS#min( self.math.trunc( pos_lim_long  / qtybtc ), self.MAX_LAYERS )
                nasks   = self.MAX_LAYERS #min( self.math.trunc( pos_lim_short / qtybtc ), self.MAX_LAYERS )
                
                place_bids = nbids > 0
                place_asks = nasks > 0
                
                if not place_bids and not place_asks:
                    abc=123#self.pprint( 'No bid no offer for %s' % fut, min_order_size_btc )
                    continue
                    
                
                #self.pprint(fut)
                #self.pprint('asks')
                #self.pprint(ask_mkt)
                #self.pprint(asks)
                #self.pprint('bids')
                #self.pprint(bid_mkt)
                #self.pprint(bids)
                for i in range( max( nbids, nasks )):
                    # BIDS
                    tsz = float(self.get_ticksize( fut ))            
                    # Perform pricing
                    vol = max( self.vols[ self.BTC_SYMBOL ], self.vols[ fut ] )

                    eps         = self.BP * vol * self.RISK_CHARGE_VOL
                    riskfac     = self.math.exp( eps )

                    bbo     = self.get_bbo( fut )
                    bid_mkt = bbo[ 'bid' ]
                    ask_mkt = bbo[ 'ask' ]
                    if 'XLM' in fut and self.client.apiKey == self.firstkey:
                        abc=123#self.pprint(bbo)
                    if bid_mkt is None and ask_mkt is None:
                        bid_mkt = ask_mkt = spot
                    elif bid_mkt is None:
                        bid_mkt = min( spot, ask_mkt )
                    elif ask_mkt is None:
                        ask_mkt = max( spot, bid_mkt )
                    mid_mkt = 0.5 * ( bid_mkt + ask_mkt )
                    try:
                        ords        = self.openorders[fut]
                    except:
                        ords = []
                    cancel_oids = []
                    bid_ords    = ask_ords = []
                    
                    if place_bids:
                        
                        bid_ords        = [ o for o in ords if o['side'] == 'BUY'  ]
                        #self.pprint(len(bid_ords))
                        len_bid_ords    = ( len( bid_ords ))
                        bid0            = bid_mkt#mid_mkt * math.exp( -MKT_IMPACT )
                        
                        bids    = [ bid0 * 1 + (.0001 * -i) for i in range( 0, nbids + 0 ) ]

                        bids[ 0 ]   = self.ticksize_floor( bids[ 0 ], tsz )
                        
                    if place_asks:
                        
                        ask_ords        = [ o for o in ords if o['side'] == 'SELL' ]    
                        #self.pprint(len(ask_ords))
                        len_ask_ords    = ( len( ask_ords ) )
                        ask0            = ask_mkt#mid_mkt * math.exp(  MKT_IMPACT )
                        
                        asks    = [ ask0 * 1 + (.0001 * i) for i in range( 0, nasks + 0 ) ]
                        
                        asks[ 0 ]   = self.ticksize_ceil( asks[ 0 ], tsz  )
                    
                    bprices = []
                    aprices = []
                    for bid in bid_ords:
                        bprices.append(float(bid['price']))
                    for ask in ask_ords:
                        aprices.append(float(ask['price']))
                    if place_bids and i < nbids:

                        if i > 0:
                            prc = self.ticksize_floor( min( bids[ i ], bids[ i - 1 ] - tsz ), tsz )
                        else:
                            prc = bids[ 0 ]

                        qty = (self.equity_usd / self.qty_div) / prc#round( prc * qtybtc )   / spot                     
                        max_skew = qty * self.max_skew_mult
                        if i < len_bid_ords:    

                            oid = bid_ords[ i ]['id']
                            #self.pprint(oid)
                            try:
                                if prc not in bprices and self.edits[fut] == False and self.slBlock[fut] == False:
                                    self.edits[fut] = True
                                    self.edit_order( oid, fut, "Limit", "buy", qty, prc, {"timeInForce": "GTX", "newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)} )
                                #else:
                                    #self.pprint(str(prc) + ' in bprices!')
                            
                            except Exception as e:
                                self.PrintException(self.client.apiKey)     
                        else:
                            #self.pprint(qty * prc)
                            try:
                                
                                
                                if self.positions[fut]['positionAmt'] <= qty * self.max_skew_mult and self.creates[fut] == False and self.slBlock[fut] == False and self.tradeBlock[fut] == False and self.lbo[fut] <= 2:
                                    
                                    self.creates[fut] = True
                                    self.create_order(  fut, "Limit", 'buy', qty, prc, {"timeInForce": "GTX", "newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)})
                                #if self.lbo[fut] > 2 and i > 2:
                                #    t = self.threading.Thread(target=self.cancel_them, args=(self.bid_ords[fut][ i - 1 ]['id'], fut,))
                                #    t.daemon = True
                                #    t.start()
                                #else:
                                    #self.pprint('not buyi    ng maxskew, pos: ' + str(self.positions[fut]['positionAmt']) + ' mod: ' + str(qty * 2.1))
                            
                            except Exception as e:
                                self.PrintException(self.client.apiKey)
                                #self.logger.warn( 'Bid order failed: %s bid for %s'
                                #                    % ( prc, qty ))

                    # OFFERS

                    if place_asks and i < nasks:

                        if i > 0:
                            prc = self.ticksize_ceil( max( asks[ i ], asks[ i - 1 ] + tsz ), tsz )
                        else:
                            prc = asks[ 0 ]
                            
                        qty = (self.equity_usd / self.qty_div) / prc#round( prc * qtybtc ) / spot
                        
                        if i < len_ask_ords:
                            oid = ask_ords[ i ]['id']
                            #self.pprint(oid)
                            try:
                                if prc not in aprices and self.edits[fut] == False and self.slBlock[fut] == False:
                                    
                                    self.edits[fut] = True
                                    self.edit_order( oid, fut, "Limit", "sell", qty, prc, {"timeInForce": "GTX", "newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)} )
                                    
                                #else:
                                    #self.pprint(str(prc) + ' in aprices!')
                            
                            except Exception as e:
                                self.PrintException(self.client.apiKey)

                        else:
                            try: #-5 > -2
                                
                                if self.positions[fut]['positionAmt'] >= qty * self.max_skew_mult * -1 and self.creates[fut] == False and self.slBlock[fut] == False and self.tradeBlock[fut] == False and self.lao[fut] <= 2:    
                                    
                                    self.creates[fut] = True
                                    self.create_order(  fut, "Limit", 'sell', qty, prc, {"timeInForce": "GTX", "newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)} )
                                #if self.lao[fut] > 2 and i > 2:
                                #    t = self.threading.Thread(target=self.cancel_them, args=(self.ask_ords[fut][ i - 1 ]['id'], fut,))
                                #    t.daemon = True
                                #    t.start()
                                #else:
                                    #self.pprint('not selling maxskew, pos: ' + str(self.positions[fut]['positionAmt']) + ' mod: ' + str(qty * 2.1 * -1))

                            
                            except Exception as e:
                                self.PrintException(self.client.apiKey)
                                #self.logger.warn( 'Offer order failed: %s at %s'
                                #                    % ( qty, prc ))

                
            except:
                self.PrintException(self.client.apiKey)
        proc = self.threading.Thread(target=self.place_orders, args=(fut,))
        abc=123#self.pprint('5 proc')
        proc.start()
        proc.terminate() 
        sleep(5)

    def edit_order( self, oid, fut, type, dir, qty, prc, params ):
        done = False
        while done == False:
            try:
                if self.goforit == True and self.goforit2 == True:
                    #self.pprint('edit ' + fut)
                    self.goforit = False
                    self.num_threads = self.num_threads + 1
                    t = self.threading.Timer(self.orderRateLimit / 1000, self.resetGoforit)
                    t.daemon = True
                    t.start()
                    #await self.asyncio.sleep(self.orderRateLimit / 1000)
                    self.client.editOrder( oid, fut, type, dir, qty, prc, params  )
                    if 'XLM' in fut  and self.client.apiKey == self.firstkey:
                        abc=123#self.pprint(fut + ' edited!')
                    done = True
                    self.edits[fut] = False
                else:
                    #if 'XLM' in fut:
                        #self.pprint(fut + ' edit blocked!')
                    self.sleep(self.orderRateLimit / 1000 * len(self.pairs) / 2)
            except Exception as e:
                if 'Unknown order sent' not in str(e):
                    self.PrintException(self.client.apiKey)

                if 'XLM' in fut  and self.client.apiKey == self.firstkey:
                    abc=123#self.pprint(fut + ' edit exception!')
                self.edits[fut] = False
                done = True
                self.sleep(self.orderRateLimit / 1000)
    def create_order( self, fut, type, dir, qty, prc, params ):
        
        done = False
        while done == False:
            try:
                if self.goforit == True and self.goforit2 == True:
                    #self.pprint('create ' + fut)
                    self.goforit = False
                    self.num_threads = self.num_threads + 1
                    t = self.threading.Timer(self.orderRateLimit / 1000, self.resetGoforit)
                    t.daemon = True
                    t.start()
                    #await self.asyncio.sleep(self.orderRateLimit / 1000)

                    self.client.createOrder(fut, type, dir, qty, prc, params )
                    if 'XLM' in fut and self.client.apiKey == self.firstkey:
                        abc=123#self.pprint(fut + ' ordered!')
                    done = True
                    
                    self.creates[fut] = False
                else:
                    #if 'XLM' in fut:
                        #self.pprint(fut + ' order blocked!')
                    self.sleep(self.orderRateLimit / 1000 * len(self.pairs) / 2)
                            
            except:
                if 'XLM' in fut and self.client.apiKey == self.firstkey:
                    abc=123#self.pprint(fut + ' order exception!')
                done = True
                self.PrintException(self.client.apiKey)
                self.creates[fut] = False
                self.sleep(self.orderRateLimit / 1000)
    def cancel_them( self, oid, fut ):
        done = False
        
        while done == False:
            try:
                #await self.asyncio.sleep(self.orderRateLimit / 1000)
                if self.goforit == True and self.goforit2 == True:
                    self.goforit = False
                    self.num_threads = self.num_threads + 1
                    t = self.threading.Timer(self.orderRateLimit / 1000, self.resetGoforit)
                    t.daemon = True
                    t.start()
                    self.client.cancelOrder( oid , fut )
                    done = True
                    self.cancels[fut] = False
                else:
                    

                    self.sleep(self.orderRateLimit / 1000* len(self.pairs) / 2)
                    
            except Exception as e:
                done = True
                self.cancels[fut] = False
                if 'Unknown order sent' not in str(e):
                    self.PrintException(self.client.apiKey)
                    self.sleep(self.orderRateLimit / 1000)
                    if self.client.apiKey == self.firstkey:
                        abc=123#self.pprint(fut + ' cancel exception!')
                else:
                    orders = [ o for o in self.openorders[fut] ]
                    for order in orders:
                        if oid == order['id']:
                            self.openorders[fut].remove(order)
                            #self.pprint('removing ' + fut)
                #self.PrintException(self.client.apiKey)
                
                #self.logger.warn( 'Order cancellations failed: %s' % oid )x