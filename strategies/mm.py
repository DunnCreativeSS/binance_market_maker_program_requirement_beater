

class Place_Orders( object ):
	def __init__( self, client, multiprocessing, brokerKey, qty_div, orderRateLimit, max_skew_mult, get_precision, math, TP, SL, asyncio, sleep, threading, PrintException, ticksize_floor, ticksize_ceil, pairs, fifteens, tens, fives, threes, con_size, get_spot, equity_btc, positions, get_ticksize, vols, get_bbo, openorders, equity_usd, randomword, logger, PCT_LIM_LONG, PCT_LIM_SHORT, DECAY_POS_LIM, MIN_ORDER_SIZE, CONTRACT_SIZE, MAX_LAYERS, BTC_SYMBOL, RISK_CHARGE_VOL, BP ):
		self.BP = BP
		self.TP = TP
		self.SL = SL
		self.multiprocessing = multiprocessing
		self.brokerKey = brokerKey
		self.qty_div = qty_div
		self.get_precision = get_precision
		self.math = math
		self.pairs = pairs
		self.max_skew_mult = max_skew_mult
		self.creates = {}
		self.edits = {}
		self.goforit = True
		for fut in self.pairs:
			self.creates[fut] = False
			self.edits[fut] = False
		self.sleep = sleep
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

	def run( self ):
		while  True:
			try:
				t = self.threading.Thread(target=self.failSafeReset, args=())
				t.daemon = True
				self.num_threads = self.num_threads + 1
				t.start()
				
			except:
				self.PrintException()
			while True:
				try:
					self.start_threads = self.threading.active_count() 
					print('start thread place_orders: ' + str(self.start_threads))
					for fut in self.pairs:
						try:
							t = self.threading.Thread(target=self.place_orders, args=(fut,))
							t.daemon = True
							
							t.start()
						except:
							self.PrintException()
					done = False
					while done == False:
						num_threads = self.threading.active_count()  - self.num_threads
						print('num thread place_orders: ' + str(num_threads) + ' / ' + str(self.start_threads + len(self.pairs) / 3) + ' and self.num_threads: ' + str(self.num_threads))
						if num_threads < self.start_threads + len(self.pairs) / 3:
							done = True
							print('restart threads...')
							self.sleep(5)
						else:
							self.sleep(5)
				except:
					self.PrintException()
	def failSafeReset( self ):
		while True:
			try:
				t = self.threading.Timer(5, self.resetGoforit)
				t.daemon = True
				self.num_threads = self.num_threads + 1
				t.start()
				self.sleep(5)
			except:
				self.PrintException()
				self.sleep(5)
		proc = self.threading.Thread(target=self.failSafeReset, args=())
		print('4 proc')
		proc.start()
		proc.terminate() 
		sleep(5)		
	def resetGoforit( self ):
		try:
			self.goforit = True
			#print(self.goforit)
			self.num_threads = self.num_threads - 1

			return
		except:
			proc = self.threading.Thread(target=self.resetGoforit, args=())
			print('6 proc')
			proc.start()
			proc.terminate() 
			sleep(5)
		
	def place_orders( self, fut ):

		
		
		con_sz  = self.con_size		
		
		
		while True:
			
			try:
				try:
					#print(fut + ': ' + str(self.positions[fut]['ROE']))
					if self.positions[fut]['ROE'] > self.TP and self.positions[fut]['ROE'] != 0:
						print(fut + ' takeprofit! ' + str(self.positions[fut]['ROE']))
						#sleep(10)
						direction = 'sell'
						if self.positions[fut]['positionAmt'] < 0:
							direction = 'buy'
						qty = self.math.fabs(self.positions[fut]['positionAmt'])
						self.creates[fut] = True
						print(str(qty) + ' ' + fut)
						self.create_order(  fut, "Market", direction, qty, None, {"newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)})
						self.positions[fut]['ROE'] = 0
					if self.positions[fut]['ROE'] < self.SL and self.positions[fut]['ROE'] != 0:
						print(fut + ' stoploss! ' + str(self.positions[fut]['ROE']))
						direction = 'sell'
						if self.positions[fut]['positionAmt'] < 0:
							direction = 'buy'
						qty = self.math.fabs(self.positions[fut]['positionAmt'])
						self.creates[fut] = True
						print(str(qty) + ' ' + fut)
						self.create_order(  fut, "Market", direction, qty, None, {"newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)})
					
						self.positions[fut]['ROE'] = 0
				except:
					self.PrintException()
				spot			= self.get_spot(fut)
				bal_btc		 = self.equity_btc
				pos			 = float(self.positions[ fut ][ 'positionAmt' ])
				pos_lim_long	= bal_btc * self.PCT_LIM_LONG * 20 #/ len(self.futures)
				pos_lim_short   = bal_btc * self.PCT_LIM_SHORT * 20 #/ len(self.futures)
				#print(pos_lim_long)
				#expi			= self.futures[ fut ][ 'expi_dt' ]
				#tte			 = max( 0, ( expi - datetime.utcnow()).total_seconds() / SECONDS_IN_DAY )
				pos_decay	   = 1.0 - self.math.exp( -self.DECAY_POS_LIM * 8035200 )
				pos_lim_long   *= pos_decay
				pos_lim_short  *= pos_decay
				pos_lim_long   -= pos
				pos_lim_short  += pos
				pos_lim_long	= max( 0, pos_lim_long  )
				pos_lim_short   = max( 0, pos_lim_short )
				
				min_order_size_btc = (self.MIN_ORDER_SIZE * self.CONTRACT_SIZE) / spot
				#print(min_order_size_btc) #0.0006833471711135484 0.08546200188472201
				qtybtc  = 1 / spot #(bal_btc * 20 / 500) / len(pairs)

				nbids   = self.MAX_LAYERS#min( self.math.trunc( pos_lim_long  / qtybtc ), self.MAX_LAYERS )
				nasks   = self.MAX_LAYERS #min( self.math.trunc( pos_lim_short / qtybtc ), self.MAX_LAYERS )
				
				place_bids = nbids > 0
				place_asks = nasks > 0
				
				if not place_bids and not place_asks:
					print( 'No bid no offer for %s' % fut, min_order_size_btc )
					continue
					
				
				#print(fut)
				#print('asks')
				#print(ask_mkt)
				#print(asks)
				#print('bids')
				#print(bid_mkt)
				#print(bids)
				for i in range( max( nbids, nasks )):
					# BIDS
					tsz = float(self.get_ticksize( fut ))			
					# Perform pricing
					vol = max( self.vols[ self.BTC_SYMBOL ], self.vols[ fut ] )

					eps		 = self.BP * vol * self.RISK_CHARGE_VOL
					riskfac	 = self.math.exp( eps )

					bbo	 = self.get_bbo( fut )
					bid_mkt = bbo[ 'bid' ]
					ask_mkt = bbo[ 'ask' ]
					if 'XLM' in fut:
						print(bbo)
					if bid_mkt is None and ask_mkt is None:
						bid_mkt = ask_mkt = spot
					elif bid_mkt is None:
						bid_mkt = min( spot, ask_mkt )
					elif ask_mkt is None:
						ask_mkt = max( spot, bid_mkt )
					mid_mkt = 0.5 * ( bid_mkt + ask_mkt )
					try:
						ords		= self.openorders[fut]
					except:
						ords = []
					cancel_oids = []
					bid_ords	= ask_ords = []
					
					if place_bids:
						
						bid_ords		= [ o for o in ords if o['info']['side'] == 'BUY'  ]
						#print(len(bid_ords))
						len_bid_ords	= ( len( bid_ords ))
						bid0			= bid_mkt#mid_mkt * math.exp( -MKT_IMPACT )
						
						bids	= [ bid0 * 1 + (.0001 * -i) for i in range( 0, nbids + 0 ) ]

						bids[ 0 ]   = self.ticksize_floor( bids[ 0 ], tsz )
						
					if place_asks:
						
						ask_ords		= [ o for o in ords if o['info']['side'] == 'SELL' ]	
						#print(len(ask_ords))
						len_ask_ords	= ( len( ask_ords ) )
						ask0			= ask_mkt#mid_mkt * math.exp(  MKT_IMPACT )
						
						asks	= [ ask0 * 1 + (.0001 * i) for i in range( 0, nasks + 0 ) ]
						
						asks[ 0 ]   = self.ticksize_ceil( asks[ 0 ], tsz  )
					bprices = []
					aprices = []
					for bid in bid_ords:
						bprices.append(float(bid['info']['price']))
					for ask in ask_ords:
						aprices.append(float(ask['info']['price']))
					if place_bids and i < nbids:

						if i > 0:
							prc = self.ticksize_floor( min( bids[ i ], bids[ i - 1 ] - tsz ), tsz )
						else:
							prc = bids[ 0 ]

						qty = (self.equity_usd / self.qty_div) / prc#round( prc * qtybtc )   / spot					 
						max_skew = qty * self.max_skew_mult
						if i < len_bid_ords:	

							oid = bid_ords[ i ]['info']['orderId']
							#print(oid)
							try:
								if prc not in bprices and self.edits[fut] == False:
									self.edits[fut] = True
									self.edit_order( oid, fut, "Limit", "buy", qty, prc, {"timeInForce": "GTX", "newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)} )
								#else:
									#print(str(prc) + ' in bprices!')
							except (SystemExit, KeyboardInterrupt):
								raise
							except Exception as e:
								self.PrintException()	 
						else:
							#print(qty * prc)
							try:
								precision = self.get_precision(fut)
								
								precision = 1 / (10 ** precision)
								
								if self.positions[fut]['positionAmt'] <= qty * self.max_skew_mult and self.creates[fut] == False:
									
									self.creates[fut] = True
									self.create_order(  fut, "Limit", 'buy', qty, prc, {"timeInForce": "GTX", "newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)})
								#else:
									#print('not buying maxskew, pos: ' + str(self.positions[fut]['positionAmt']) + ' mod: ' + str(qty * 2.1))
							except (SystemExit, KeyboardInterrupt):
								raise
							except Exception as e:
								self.PrintException()
								#self.logger.warn( 'Bid order failed: %s bid for %s'
								#					% ( prc, qty ))

					# OFFERS

					if place_asks and i < nasks:

						if i > 0:
							prc = self.ticksize_ceil( max( asks[ i ], asks[ i - 1 ] + tsz ), tsz )
						else:
							prc = asks[ 0 ]
							
						qty = (self.equity_usd / self.qty_div) / prc#round( prc * qtybtc ) / spot
						
						if i < len_ask_ords:
							oid = ask_ords[ i ]['info']['orderId']
							#print(oid)
							try:
								if prc not in aprices and self.edits[fut] == False:
									
									self.edits[fut] = True
									self.edit_order( oid, fut, "Limit", "sell", qty, prc, {"timeInForce": "GTX", "newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)} )
									
								#else:
									#print(str(prc) + ' in aprices!')
							except (SystemExit, KeyboardInterrupt):
								raise
							except Exception as e:
								self.PrintException()

						else:
							try: #-5 > -2
								precision = self.get_precision(fut)
								#print(fut + ' precision ' + str(precision))
								precision = 1 / (10 ** precision)
								#print(fut + ' precision ' + str(precision))
								#print(qty)
								#print(qty > precision)
								if self.positions[fut]['positionAmt'] >= qty * self.max_skew_mult * -1 and self.creates[fut] == False:
									
									self.creates[fut] = True
									self.create_order(  fut, "Limit", 'sell', qty, prc, {"timeInForce": "GTX", "newClientOrderId": "x-" + self.brokerKey + "-" + self.randomword(20)} )
								#else:
									#print('not selling maxskew, pos: ' + str(self.positions[fut]['positionAmt']) + ' mod: ' + str(qty * 2.1 * -1))

							except (SystemExit, KeyboardInterrupt):
								raise
							except Exception as e:
								self.PrintException()
								#self.logger.warn( 'Offer order failed: %s at %s'
								#					% ( qty, prc ))

				if nbids < len( bid_ords ):
					cancel_oids += [ o['info']['orderId'] for o in bid_ords[ nbids : ]]
				if nasks < len( ask_ords ):
					cancel_oids += [ o['info']['orderId'] for o in ask_ords[ nasks : ]]
				for oid in cancel_oids:
					self.cancel_them(oid, fut)
			except:
				self.PrintException()
		proc = self.threading.Thread(target=self.place_orders, args=(fut,))
		print('5 proc')
		proc.start()
		proc.terminate() 
		sleep(5)

	def edit_order( self, oid, fut, type, dir, qty, prc, params ):
		done = False
		while done == False:
			try:
				if self.goforit == True:
					self.goforit = False
					self.num_threads = self.num_threads + 1
					t = self.threading.Timer(self.orderRateLimit / 1000, self.resetGoforit)
					t.daemon = True
					t.start()
					#await self.asyncio.sleep(self.orderRateLimit / 1000)
					self.client.editOrder( oid, fut, type, dir, qty, prc, params  )
					if 'XLM' in fut:
						print(fut + ' edited!')
					done = True
					self.edits[fut] = False
				else:
					#if 'XLM' in fut:
						#print(fut + ' edit blocked!')
					self.sleep(self.orderRateLimit / 1000 * len(self.pairs) / 2)
			except Exception as e:
				if 'Unknown order sent' not in str(e):
					self.PrintException()

				if 'XLM' in fut:
					print(fut + ' edit exception!')
				self.edits[fut] = False
				done = True
				self.sleep(self.orderRateLimit / 1000)
	def create_order( self, fut, type, dir, qty, prc, params ):

		done = False
		while done == False:
			try:
				if self.goforit == True:
					self.goforit = False
					self.num_threads = self.num_threads + 1
					t = self.threading.Timer(self.orderRateLimit / 1000, self.resetGoforit)
					t.daemon = True
					t.start()
					#await self.asyncio.sleep(self.orderRateLimit / 1000)

					self.client.createOrder(fut, type, dir, qty, prc, params )
					if 'XLM' in fut:
						print(fut + ' ordered!')
					done = True
					
					self.creates[fut] = False
				else:
					#if 'XLM' in fut:
						#print(fut + ' order blocked!')
					self.sleep(self.orderRateLimit / 1000 * len(self.pairs) / 2)
							
			except:
				if 'XLM' in fut:
					print(fut + ' order exception!')
				done = True
				self.PrintException()
				self.creates[fut] = False
				self.sleep(self.orderRateLimit / 1000)
	def cancel_them( self, oid, fut ):
		done = False
		while done == False:
			try:
				#await self.asyncio.sleep(self.orderRateLimit / 1000)
				if self.goforit == True:
					self.goforit = False
					self.num_threads = self.num_threads + 1
					t = self.threading.Timer(self.orderRateLimit / 1000, self.resetGoforit)
					t.daemon = True
					t.start()
					self.client.cancelOrder( oid , fut )
					done = True
				else:
					

					self.sleep(self.orderRateLimit / 1000* len(self.pairs) / 2)
					
			except:
				self.PrintException()
				done = True
				print(fut + ' cancel exception!')
				self.sleep(self.orderRateLimit / 1000)
				#self.logger.warn( 'Order cancellations failed: %s' % oid )x