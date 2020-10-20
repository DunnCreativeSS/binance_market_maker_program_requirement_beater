# This code is for sample purposes only, comes as is and with no warranty or guarantee of performance
# ADA, XTZ, XLM
pairs = ['XLM/USDT', 'ADA/USDT', 'DASH/USDT', 'ZEC/USDT', 'ATOM/USDT', 'IOST/USDT', 'THETA/USDT', 'XTZ/USDT', 'OMG/USDT', 'COMP/USDT', 'ZRX/USDT', 'KNC/USDT', 'ZIL/USDT', 'DOGE/USDT', 'RLC/USDT', 'BAT/USDT', 'IOTA/USDT', 'XMR/USDT']#'BTC/USDT'
print(len(pairs))
fifteens = ['XLM/USDT', 'ADA/USDT', 'DASH/USDT', 'ZEC/USDT', 'ATOM/USDT']
tens = ['OMG/USDT', 'COMP/USDT', 'ZRX/USDT', 'XMR/USDT', 'ZIL/USDT', 'KNC/USDT', 'XTZ/USDT', 'IOTA/USDT', 'BAT/USDT', 'IOST/USDT', 'THETA/USDT']
fives = ['DOGE/USDT']
threes = ['RLC/USDT']
binApi2 = 'dnB0rWq2T3XNlOHWObP6exuBVjMtI3S4BdDssUi5s4iuCgO9VK2xcpndNSfWPa3d'
binSecret2 = 'Xw4A5VcHB3ZDJZuLGhxh8Lq9ouLWIxMERj1p4jeorKvvhzkDxXj3Qx1eiVonMcPs'
#jarettrsdunn+alimm@gmail.com
#binApi = "8799eb6011f07a7dbba434907f71adc5f7e76af1fd12be26bb4e3294904e9852"
#binSecret = "e487c0edb6ec0f6fd839919858dce4a3f936d7d67fe0e6a4773b579173fe1355"
from collections	import OrderedDict
from datetime	   import datetime
import asyncio
import threading
from datetime import timedelta
import sys
import linecache
import os
import traceback
from os.path		import getmtime
import ccxtpro
import asyncio
import requests

from cryptofeed import FeedHandler
from cryptofeed import FeedHandler
from cryptofeed.callback import BookCallback, TickerCallback, TradeCallback
from cryptofeed.defines import BID, ASK, FUNDING, L2_BOOK, OPEN_INTEREST, TICKER, TRADES
from cryptofeed.exchanges import BinanceFutures
fh = FeedHandler()
mids = {}
async def ticker(feed, pair, bid, ask, timestamp, ex):
    global mids
    #print(f'Ex?: {ex} Timestamp: {timestamp} Feed: {feed} Pair: {pair} Bid: {bid} Ask: {ask}')
    
    if 'BINANCE' in feed:
        #ETH-USD_200925
        name = pair.replace('-', '/')
        #print(dt)


   # print(feed + '-' + name + '-' + dt +': ' + str( 0.5 * ( float(bid) + float(ask))))
    mids[name] = {'ask': float(ask), 'bid':  float(bid)}

pairs2 = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo').json()
bcontracts = []
for symbol in pairs2['symbols']:
    split = len(symbol['baseAsset'])
    normalized = symbol['symbol'][:split] + '-' + symbol['symbol'][split:]
    #print(normalized)
    bcontracts.append(normalized)
config = {TICKER: bcontracts}

fh.add_feed(BinanceFutures(config=config, callbacks={TICKER: TickerCallback(ticker)}))
def loop_in_thread():
    fh.run()
from time		   import sleep
from utils		  import ( get_logger, lag, print_dict, print_dict_of_dicts, sort_by_key,
							 ticksize_ceil, ticksize_floor, ticksize_round )
import json
import random, string
import copy as cp
import argparse, logging, math, os, pathlib, sys, time, traceback
import ccxt
try:
	from deribit_api	import RestClient
except ImportError:
	print("Please install the deribit_api pacakge", file=sys.stderr)
	print("	pip3 install deribit_api", file=sys.stderr)
	exit(1)
t = threading.Thread(target=loop_in_thread, args=())
t.start()
# Add command line switches
parser  = argparse.ArgumentParser( description = 'Bot' )
d		 = datetime.utcnow()  - timedelta(hours = 0)
epoch = datetime(1970,1,1)
start_time = int((d - epoch).total_seconds()) * 1000
print(start_time)

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    string = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    print(string)

# Use production platform/account
parser.add_argument( '-p',
					 dest   = 'use_prod',
					 action = 'store_true' )

# Do not display regular status updates to terminal
parser.add_argument( '--no-output',
					 dest   = 'output',
					 action = 'store_false' )

# Monitor account only, do not send trades
parser.add_argument( '-m',
					 dest   = 'monitor',
					 action = 'store_true' )

# Do not restart bot on errors
parser.add_argument( '--no-restart',
					 dest   = 'restart',
					 action = 'store_false' )

args	= parser.parse_args()

if not args.use_prod:
	KEY	 = ''
	SECRET  = ''
	URL	 = 'https://test.deribit.com'
else:
	KEY	 = ''
	SECRET  = ''
	URL	 = 'https://www.deribit.com'
	
BP				  = 1e-4	  # one basis point
BTC_SYMBOL		  = 'btc'
CONTRACT_SIZE	   = 10	 # USD
COV_RETURN_CAP	  = 100	   # cap on variance for vol estimate
DECAY_POS_LIM	   = 0.1	   # position lim decay factor toward expiry
EWMA_WGT_COV		= 4		 # parameter in % points for EWMA volatility estimate
EWMA_WGT_LOOPTIME   = 0.1	   # parameter for EWMA looptime estimate
FORECAST_RETURN_CAP = 20		# cap on returns for vol estimate
LOG_LEVEL		   = logging.INFO
MIN_ORDER_SIZE	  = 75
MAX_LAYERS		  =  4		# max orders to layer the ob with on each side
MKT_IMPACT		  =  0.01   # base 1-sided spread between bid/offer
NLAGS			   =  2		# number of lags in time series
PCT				 = 100 * BP  # one percentage point
PCT_LIM_LONG		= 200	# % position limit long
PCT_LIM_SHORT	   = 100	   # % position limit short
PCT_QTY_BASE		= 0.05	   # pct order qty in bps as pct of acct on each order
MIN_LOOP_TIME	   =   14.6	 # Minimum time between loops
RISK_CHARGE_VOL	 =   1.5	# vol risk charge in bps per 100 vol
SECONDS_IN_DAY	  = 3600 * 24
SECONDS_IN_YEAR	 = 365 * SECONDS_IN_DAY
WAVELEN_MTIME_CHK   = 15		# time in seconds between check for file change
WAVELEN_OUT		 = 15		# time in seconds between output to terminal
WAVELEN_TS		  = 15		# time in seconds between time series update
VOL_PRIOR		   = 100	   # vol estimation starting level in percentage pts

	

	#DECAY_POS_LIM = data['RISK_CHARGE_VOL']['current']
	
EWMA_WGT_COV		*= PCT
MKT_IMPACT		  *= BP
PCT_LIM_LONG		*= PCT
PCT_LIM_SHORT	   *= PCT
PCT_QTY_BASE		*= BP
VOL_PRIOR		   *= PCT


class MarketMaker( object ):
	
	def __init__( self, monitor = True, output = True ):
		self.equity_usd		 = None
		self.equity_btc		 = None
		self.equity_usd_init	= None
		self.equity_btc_init	= None
		self.con_size		   = float( CONTRACT_SIZE )
		self.client			 = None
		self.client2 = None
		self.openorders = {}
		self.orderbooks = {}
		self.bids = {}
		self.deltas			 = OrderedDict()
		self.futures			= OrderedDict()
		self.futures_prv		= OrderedDict()
		self.logger			 = None
		self.mean_looptime	  = 1
		self.monitor			= monitor
		self.output			 = output or monitor
		self.positions		  = OrderedDict()
		self.spread_data		= None
		self.this_mtime		 = None
		self.ts				 = None
		self.vols			   = OrderedDict()
	
	def create_client( self ):
		#self.client = RestClient( KEY, SECRET, URL )
		#print(binApi)
		binance_futures = ccxt.binance(
			{"apiKey": binApi2,
			"secret": binSecret2,
			 'options': {'defaultType': 'future'},
	'enableRateLimit': True,
})

		#binance_futures.set_sandbox_mode(True)
			
		self.client2 = ccxt.binance({	"apiKey": binApi2,
	"secret": binSecret2})
		self.client = binance_futures
		#print(dir(self.client))		   
		m = binance_futures.fetchMarkets()
		
	

	def randomword(self, length):
	   letters = string.ascii_lowercase
	   return ''.join(random.choice(letters) for i in range(length))

	def getTrades( self, pair, endTime, quoteTotal, commissionTotal ):
		d		 = datetime.utcnow()  - timedelta(hours = 4)
		epoch = datetime(1970,1,1)
		st = int((d - epoch).total_seconds()) * 1000
		days = 4/24
		if start_time > st:
			st = start_time
			days	= ( datetime.utcnow() - self.start_time ).total_seconds() / SECONDS_IN_DAY
		oldTime = 9999999999999999999999999999999999999
		if endTime == 0:
			trades = self.client.fapiPrivateGetUserTrades({"symbol": pair.replace('/', ''), "limit": 1000, 'startTime': st})
		else:
			trades = self.client.fapiPrivateGetUserTrades({"symbol": pair.replace('/', ''), "limit": 1000, 'startTime': st, 'endTime': endTime})
		for t in trades:
			if t['time'] < oldTime:
				oldTime = t['time']
			commissionTotal = commissionTotal + float(t['commission'])
			if float(t['quoteQty']) > 0:
				quoteTotal = quoteTotal + float(t['quoteQty'])
			else:
				quoteTotal = quoteTotal - float(t['quoteQty'])
		if len(trades) < 999:
			
			return([quoteTotal, commissionTotal, days])
		else:
			return(getTrades(pair, oldTime, quoteTotal, commissionTotal))

	def get_bbo( self, contract ): # Get best b/o excluding own orders
		
		# Get orderbook
		best_bid	= mids[contract]['bid']
		best_ask	= mids[contract]['ask']
		
		return { 'bid': best_bid, 'ask': best_ask }
	
		
	def get_futures( self ): # Get all current futures instruments
		
		self.futures_prv	= cp.deepcopy( self.futures )
		insts			   = self.client.fetchMarkets()

		#print(insts[0])
		self.futures		= sort_by_key( { 
			i[ 'symbol' ]: i for i in insts if i['type'] == 'future' and i['active'] == True
		} )
		#print(self.futures)
		#for k, v in self.futures.items():
			#self.futures[ k ][ 'expi_dt' ] = datetime.strptime( 
			#								   v[ 'expiration' ][ : -4 ], 
			#								   '%Y-%m-%d %H:%M:%S' )
						
		
	def get_pct_delta( self ):		 
		self.update_status()
		return sum( self.deltas.values()) / float(self.equity_btc)

	def get_spot_old( self, pair ):
		print('getspotold!')
		sleep(1)
		#print(self.client2.fetchTicker( pair )['bid'])
		
		return self.client2.fetchTicker( pair )['bid']
	def get_spot( self, pair ):
		#print(self.client2.fetchTicker( pair )['bid'])
		try:
			self.bids[pair] = mids[ pair ]['bid']
		except:
			self.bids[pair] = self.get_spot_old(pair)
		return self.bids[pair]

	
	def get_precision( self, contract ):
		return self.futures[ contract ] ['info'] [ 'pricePrecision' ]

	
	def get_ticksize( self, contract ):
		return self.futures[ contract ] ['info'] ['filters'] [ 0 ] [ 'tickSize' ]
	
	
	

		
	def place_orders( self ):

		if self.monitor:
			return None
		
		con_sz  = self.con_size		
		
		for fut in pairs:
			
			
			spot			= self.get_spot(fut)
			bal_btc		 = self.equity_btc
			pos			 = float(self.positions[ fut ][ 'positionAmt' ])
			pos_lim_long	= bal_btc * PCT_LIM_LONG * 20 #/ len(self.futures)
			pos_lim_short   = bal_btc * PCT_LIM_SHORT * 20 #/ len(self.futures)
			#print(pos_lim_long)
			#expi			= self.futures[ fut ][ 'expi_dt' ]
			#tte			 = max( 0, ( expi - datetime.utcnow()).total_seconds() / SECONDS_IN_DAY )
			pos_decay	   = 1.0 - math.exp( -DECAY_POS_LIM * 8035200 )
			pos_lim_long   *= pos_decay
			pos_lim_short  *= pos_decay
			pos_lim_long   -= pos
			pos_lim_short  += pos
			pos_lim_long	= max( 0, pos_lim_long  )
			pos_lim_short   = max( 0, pos_lim_short )
			
			min_order_size_btc = (MIN_ORDER_SIZE * CONTRACT_SIZE) / spot
			#print(min_order_size_btc) #0.0006833471711135484 0.08546200188472201
			qtybtc  = 1 / spot #(bal_btc * 20 / 500) / len(pairs)

			nbids   = min( math.trunc( pos_lim_long  / qtybtc ), MAX_LAYERS )
			nasks   = min( math.trunc( pos_lim_short / qtybtc ), MAX_LAYERS )
			
			place_bids = nbids > 0
			place_asks = nasks > 0
			
			if not place_bids and not place_asks:
				print( 'No bid no offer for %s' % fut, min_order_size_btc )
				continue
				
			tsz = float(self.get_ticksize( fut ))			
			# Perform pricing
			vol = max( self.vols[ BTC_SYMBOL ], self.vols[ fut ] )

			eps		 = BP * vol * RISK_CHARGE_VOL
			riskfac	 = math.exp( eps )

			bbo	 = self.get_bbo( fut )
			bid_mkt = bbo[ 'bid' ]
			ask_mkt = bbo[ 'ask' ]
			
			if bid_mkt is None and ask_mkt is None:
				bid_mkt = ask_mkt = spot
			elif bid_mkt is None:
				bid_mkt = min( spot, ask_mkt )
			elif ask_mkt is None:
				ask_mkt = max( spot, bid_mkt )
			mid_mkt = 0.5 * ( bid_mkt + ask_mkt )
			
			ords		= self.openorders[fut]
			cancel_oids = []
			bid_ords	= ask_ords = []
			
			if place_bids:
				
				bid_ords		= [ o for o in ords if o['info']['side'] == 'BUY'  ]
				#print(len(bid_ords))
				len_bid_ords	= ( len( bid_ords ))
				bid0			= bid_mkt#mid_mkt * math.exp( -MKT_IMPACT )
				
				bids	= [ bid0 * 1 + (.0001 * -i) for i in range( 0, nbids + 0 ) ]

				bids[ 0 ]   = ticksize_floor( bids[ 0 ], tsz )
				
			if place_asks:
				
				ask_ords		= [ o for o in ords if o['info']['side'] == 'SELL' ]	
				#print(len(ask_ords))
				len_ask_ords	= ( len( ask_ords ) )
				ask0			= ask_mkt#mid_mkt * math.exp(  MKT_IMPACT )
				
				asks	= [ ask0 * 1 + (.0001 * i) for i in range( 0, nasks + 0 ) ]
				
				asks[ 0 ]   = ticksize_ceil( asks[ 0 ], tsz  )
			bprices = []
			aprices = []
			for bid in bid_ords:
				bprices.append(float(bid['info']['price']))
			for ask in ask_ords:
				aprices.append(float(ask['info']['price']))
			#print(fut)
			#print('asks')
			#print(ask_mkt)
			#print(asks)
			#print('bids')
			#print(bid_mkt)
			#print(bids)
			for i in range( max( nbids, nasks )):
				# BIDS
				if place_bids and i < nbids:

					if i > 0:
						prc = ticksize_floor( min( bids[ i ], bids[ i - 1 ] - tsz ), tsz )
					else:
						prc = bids[ 0 ]

					qty = (self.equity_usd / 15) / prc#round( prc * qtybtc )   / spot					 
					max_skew = qty * 1.1
					if i < len_bid_ords:	

						oid = bid_ords[ i ]['info']['orderId']
						#print(oid)
						try:
							if prc not in bprices:
								self.client.editOrder( oid, fut, "Limit", "buy", qty, prc )
							#else:
								#print(str(prc) + ' in bprices!')
						except (SystemExit, KeyboardInterrupt):
							raise
						except Exception as e:
							PrintException()	 
					else:
						#print(qty * prc)
						try:
							if self.positions[fut]['positionAmt'] <= qty * 2.1: 
								self.client.createOrder(  fut, "Limit", 'buy', qty, prc, {"newClientOrderId": "x-GYswxDoF-" + self.randomword(20)})
							#else:
								#print('not buying maxskew, pos: ' + str(self.positions[fut]['positionAmt']) + ' mod: ' + str(qty * 2.1))
						except (SystemExit, KeyboardInterrupt):
							raise
						except Exception as e:
							PrintException()
							self.logger.warn( 'Bid order failed: %s bid for %s'
												% ( prc, qty ))

				# OFFERS

				if place_asks and i < nasks:

					if i > 0:
						prc = ticksize_ceil( max( asks[ i ], asks[ i - 1 ] + tsz ), tsz )
					else:
						prc = asks[ 0 ]
						
					qty = (self.equity_usd / 15) / prc#round( prc * qtybtc ) / spot
					
					if i < len_ask_ords:
						oid = ask_ords[ i ]['info']['orderId']
						#print(oid)
						try:
							if prc not in aprices:
								self.client.editOrder( oid, fut, "Limit", "sell", qty, prc )
							#else:
								#print(str(prc) + ' in aprices!')
						except (SystemExit, KeyboardInterrupt):
							raise
						except Exception as e:
							PrintException()

					else:
						try: #-5 > -2
							if self.positions[fut]['positionAmt'] >= qty * 2.1 * -1: 
								self.client.createOrder(  fut, "Limit", 'sell', qty, prc, {"newClientOrderId": "x-GYswxDoF-" + self.randomword(20)})
							#else:
								#print('not selling maxskew, pos: ' + str(self.positions[fut]['positionAmt']) + ' mod: ' + str(qty * 2.1 * -1))

						except (SystemExit, KeyboardInterrupt):
							raise
						except Exception as e:
							self.logger.warn( 'Offer order failed: %s at %s'
												% ( qty, prc ))


			if nbids < len( bid_ords ):
				cancel_oids += [ o['info']['orderId'] for o in bid_ords[ nbids : ]]
			if nasks < len( ask_ords ):
				cancel_oids += [ o['info']['orderId'] for o in ask_ords[ nasks : ]]
			for oid in cancel_oids:
				try:
					self.client.cancelOrder( oid , fut )
				except:
					self.logger.warn( 'Order cancellations failed: %s' % oid )
										
	def cancelall(self):
		for pair in pairs:
			ords		= self.openorders[pair]
			for order in ords:
				#print(order)
				oid = order ['info'] ['orderId']
			   # print(order)
				try:
					self.client.cancelOrder( oid , pair )
				except Exception as e:
					PrintException()
	def restart( self ):		
		try:
			strMsg = 'RESTARTING'
			print( strMsg )
			self.cancelall()
			strMsg += ' '
			for i in range( 0, 5 ):
				strMsg += '.'
				print( strMsg )
				sleep( 1 )
		except:
			pass
		finally:
			os.execv( sys.executable, [ sys.executable ] + sys.argv )		
			

	def run( self ):
		
		self.run_first()

		t_ts = t_out = t_loop = t_mtime = datetime.utcnow()

		while True:

			self.get_futures()
			
			# Restart if a new contract is listed
			#if len( self.futures ) != len( self.futures_prv ):
			#	self.restart()
			
			
			t_now   = datetime.utcnow()
			
			# Update time series and vols
			if ( t_now - t_ts ).total_seconds() >= WAVELEN_TS:
				t_ts = t_now
				
				self.update_timeseries()
				self.update_vols()
	
			self.place_orders()
			
			# Display status to terminal
			if self.output:	
				t_now   = datetime.utcnow()
			
			# Restart if file change detected
			t_now   = datetime.utcnow()
			if ( t_now - t_mtime ).total_seconds() > WAVELEN_MTIME_CHK:
				t_mtime = t_now
				#if getmtime( __file__ ) > self.this_mtime:
				#	self.restart()
			
			t_now	   = datetime.utcnow()
			looptime	= ( t_now - t_loop ).total_seconds()
			
			# Estimate mean looptime
			w1  = EWMA_WGT_LOOPTIME
			w2  = 1.0 - w1
			t1  = looptime
			t2  = self.mean_looptime
			
			self.mean_looptime = w1 * t1 + w2 * t2
			
			t_loop	  = t_now
			sleep_time  = MIN_LOOP_TIME - looptime
			#if sleep_time > 0:
			#	time.sleep( sleep_time )
			if self.monitor:
				time.sleep( WAVELEN_OUT )
	def loop_in_thread(self):
		while True:
			loop = asyncio.new_event_loop()
			
			loop.run_until_complete(self.looptiloop(loop))
			
	def run_first( self ):
		
		self.create_client()
		#self.cancelall()
		self.logger = get_logger( 'root', LOG_LEVEL )
		# Get all futures contracts
		self.get_futures()
		sleep(10)
		"""
		pairs = []
		for fut in self.futures.keys():
			try:
				self.get_spot_old(fut)
				pairs.append(fut)
			except:
				print(fut)
		"""
		self.start_time		 = datetime.utcnow()- timedelta(hours = 0)
		t = threading.Thread(target=self.loop_in_thread, args=())
		t.start()
		self.this_mtime = getmtime( __file__ )
		self.symbols	= [ BTC_SYMBOL ] + list( pairs); self.symbols.sort()
		self.deltas	 = OrderedDict( { s: None for s in self.symbols } )
		
		# Create historical time series data for estimating vol
		ts_keys = self.symbols + [ 'timestamp' ]; ts_keys.sort()
		
		self.ts = [
			OrderedDict( { f: None for f in ts_keys } ) for i in range( NLAGS + 1 )
		]
		
		self.vols   = OrderedDict( { s: VOL_PRIOR for s in self.symbols } )
		sleep(10)
		self.update_status()

		
		
		for pair in pairs:
			
			self.client.fapiPrivatePostLeverage({'symbol': pair.replace('/USDT', 'USDT'), 'leverage': 25})
			
		sleep(3)
	
	async def looptiloop(self, loop):
		while True:
			try:
				exchange = ccxtpro.binance(
				{"apiKey": binApi2,
    'enableRateLimit': True,
				"secret": binSecret2,
				 'options': {'defaultType': 'future', 'watchBalance': 'future',"fetchBalance": "future",},'asyncio_loop': loop})
				await exchange.load_markets()
				#exchange.verbose = True
				try:
					balance = await exchange.fetch_balance()
					self.equity_usd = balance['USDT']['total']
					self.equity_btc = self.equity_usd * self.get_spot('BTC/USDT')
					if self.equity_usd_init == None:
						self.equity_usd_init	= self.equity_usd
						self.equity_btc_init	= self.equity_btc 
				except Exception as e:
					PrintException()
				try:
					self.positions  = OrderedDict( { f: {
						'size':		 0,
						'positionAmt':	  0,
						'indexPrice':   None,
						'markPrice':	None
					} for f in pairs } )
					positions	   = self.client.fapiPrivateGetPositionRisk()
					#print('lala')
					#print(positions)
					
					for pos in positions:
						if pos['symbol'].split('USDT')[0] + '/USDT' in pairs:
							pos['positionAmt'] = float(pos['positionAmt'])

							self.positions[ pos['symbol'].split('USDT')[0] + '/USDT'] = pos
				except Exception as e:
					PrintException()
				for pair in pairs:
					#print(pair)
					try:
						self.openorders[pair] = self.client.fetchOpenOrders( pair )
					except Exception as e:
						PrintException()
				
				
				for pair in pairs:
					self.bids[pair] = mids[pair]['bid']
					"""
					try:
						orderbook = await exchange.watch_order_book(pair)
						self.orderbooks[pair] = orderbook
						self.bids[pair] = orderbook['bids'][0][0]
					except Exception as e:
						PrintException()
					"""
				if not self.output:
					return None
				
				self.update_status()
				
				now	 = datetime.utcnow()
				days	= ( now - self.start_time ).total_seconds() / SECONDS_IN_DAY
				print( '********************************************************************' )
				print( 'Start Time:		%s' % self.start_time.strftime( '%Y-%m-%d %H:%M:%S' ))
				print( 'Current Time:	  %s' % now.strftime( '%Y-%m-%d %H:%M:%S' ))
				print( 'Days:			  %s' % round( days, 1 ))
				print( 'Hours:			 %s' % round( days * 24, 1 ))
				print( 'Spot Price:		%s' % self.get_spot('BTC/USDT'))
				
				equity_usd = self.equity_usd
				equity_btc = self.equity_btc
				pnl_usd = equity_usd - self.equity_usd_init
				pnl_btc = equity_btc - self.equity_btc_init
				
				print( 'Equity ($):		%7.2f'   % equity_usd)
				print( 'P&L ($)			%7.2f'   % pnl_usd)
				print( 'Equity (BTC):	  %7.4f'   % equity_btc)
				print( 'P&L (BTC)		  %7.4f'   % pnl_btc)
				#print( '%% Delta:		   %s%%'% round( self.get_pct_delta() / PCT, 1 ))
				#print( 'Total Delta (BTC): %s'   % round( sum( self.deltas.values()), 2 ))		
				#print_dict_of_dicts( {
				#	k: {
				#		'BTC': self.deltas[ k ]
				#	} for k in self.deltas.keys()
				#	}, 
				#	roundto = 2, title = 'Deltas' )
				
				#print(self.positions)
				print_dict_of_dicts( {
					k: {
						'Contracts $ Value': round(self.positions[ k ][ 'positionAmt' ] * self.bids[k] * 100) / 100
					} for k in self.positions.keys()
					}, 

					title = 'Positions' )
				
					
				if not self.monitor:
					print_dict_of_dicts( {
						k: {
							'%': self.vols[ k ]
						} for k in self.vols.keys()
						}, 
						multiple = 100, title = 'Vols' )
					print( '\nMean Loop Time: %s' % round( self.mean_looptime, 2 ))
					#self.cancelall()
				print( '' )	
				print(' ')
				days	= ( datetime.utcnow() - self.start_time ).total_seconds() / SECONDS_IN_DAY
				print('Volumes Traded Projected Daily of Required (' + str(days) + ' days passed thus far...)')
				print('Equity: $' + str(round(self.equity_usd*100)/100))
				btc = self.get_spot('BTC/USDT')
				print('btc')
				percent = self.equity_usd / btc
				volumes = []
				tradet = 0
				feest = 0
				for pair in pairs:
					gettrades = self.getTrades(pair, 0, 0, 0)

					#print(gettrades)
					volume = (gettrades[0] / (gettrades[2]))
					feest = feest + gettrades[0] * 0.0002
					tradet = tradet + volume * 30
					printprint = True
					if pair in fifteens:
						volume = (volume / 15000)
					elif pair in tens:
						volume = (volume / 10000)
					elif pair in fives:
						volume = (volume / 5000)
					elif pair in threes:
						volume = (volume / 3000)
					else:
						printprint = False
						volume = (volume / 25000)
					volumes.append(volume)
					#print(volume)
					if printprint == True:
						print(pair + ': ' + str(round(volume*1000)/10) + '%' + ', (Real) USD traded: $' + str(round(gettrades[0]*100)/100) + ', fees paid: $' + str(round(gettrades[1] * 10000)/10000))
					else:
						print('(Real) USD traded: $' + str(round(gettrades[0]*100)/100) + ', fees paid: $' + str(round(gettrades[1] * 10000)/10000))
				volumes.sort()
				h = 100
				for i in range(0,5):
					if volumes[-i] < h and volumes[-i] > 0:
						h = volumes[-i]
						if h > 1:
							h = 1
				try:
					h = 1 / h
				except:
					h = 1
				mult = h
				h = h * self.equity_usd

				print('Approx. traded volumes over 30 days: ' + str(tradet) + ', in BTC: ' + str(round(tradet/btc*1000)/1000))
				print('Approx. Min Equity at 25x in USD to Achieve 100% Daily Requirements Across 6 Highest %s Above: $' + str(round(h * 100)/100))
				diff = h / self.equity_usd
				print('That\'s ' + str(round(diff*100)/100) + 'x the balance now, bringing projected USD/month to: ' + str(round(tradet * diff * 100)/100) + ', and BTC: ' + str(round((tradet * diff / btc)* 100)/100))
				apy = 365 / (gettrades[2])
				pnl = (((self.equity_usd + feest) / self.equity_usd) -1) * 100
				pnl2 = pnl * apy
				print('Now, if we were running in a trial mode of Binance Market Maker Program\'s Rebates, or if we had achieved these rates already, we would have earned $' + str(round(feest * 100)/100) + ' by now, or rather earning ' + str(round(pnl*1000)/1000) + '% PnL so far, or ' + str(round(pnl2*1000)/1000) + ' % Annual Percentage Yield!')
				btcneed = (((tradet * diff / btc) / 3000) )
				if btcneed < 1 and btcneed != 0:
					h = h / btcneed
					print('For 3000 btc/month volumes, would make the equity minimum approx. $' + str(round(h * 100)/100))
				
				await exchange.close()	
			except Exception as e:
			 	PrintException()
	
	def update_status( self ):
		  
			 
				
		self.deltas = OrderedDict( 
			{ k: float(self.positions[ k ][ 'positionAmt' ]) for k in pairs}
		)
		

		
		
	
	def update_timeseries( self ):
		
		if self.monitor:
			return None
		
		for t in range( NLAGS, 0, -1 ):
			self.ts[ t ]	= cp.deepcopy( self.ts[ t - 1 ] )
		
		spot					= self.get_spot('BTC/USDT')
		self.ts[ 0 ][ BTC_SYMBOL ]	= spot
		
		for c in pairs:
			
			bbo = self.get_bbo( c )
			bid = bbo[ 'bid' ]
			ask = bbo[ 'ask' ]

			if not bid is None and not ask is None:
				mid = 0.5 * ( bbo[ 'bid' ] + bbo[ 'ask' ] )
			else:
				continue
			self.ts[ 0 ][ c ]			   = mid
				
		self.ts[ 0 ][ 'timestamp' ]  = datetime.utcnow()

		
	def update_vols( self ):
		
		if self.monitor:
			return None
		
		w   = EWMA_WGT_COV
		ts  = self.ts
		
		t   = [ ts[ i ][ 'timestamp' ] for i in range( NLAGS + 1 ) ]
		p   = { c: None for c in self.vols.keys() }
		for c in ts[ 0 ].keys():
			p[ c ] = [ ts[ i ][ c ] for i in range( NLAGS + 1 ) ]
		
		if any( x is None for x in t ):
			return None
		for c in self.vols.keys():
			if any( x is None for x in p[ c ] ):
				return None
		
		NSECS   = SECONDS_IN_YEAR
		cov_cap = COV_RETURN_CAP / NSECS
		
		for s in self.vols.keys():
			
			x   = p[ s ]			
			dx  = x[ 0 ] / x[ 1 ] - 1
			dt  = ( t[ 0 ] - t[ 1 ] ).total_seconds()
			v   = min( dx ** 2 / dt, cov_cap ) * NSECS
			v   = w * v + ( 1 - w ) * self.vols[ s ] ** 2
			
			self.vols[ s ] = math.sqrt( v )
							
		
if __name__ == '__main__':
	
	try:
		mmbot = MarketMaker( monitor = args.monitor, output = args.output )
		mmbot.run()
	except( KeyboardInterrupt, SystemExit ):
		print( "Cancelling open orders" )
		mmbot.cancelall()
		sys.exit()
	except:
		print( traceback.format_exc())
		if args.restart:
			mmbot.restart()
		
