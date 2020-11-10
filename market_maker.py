# These vars load from database :)"

pairs = {'dnB0rWq2T3XNlOHWObP6exuBVjMtI3S4BdDssUi5s4iuCgO9VK2xcpndNSfWPa3d': ['XLM/USDT', 'ADA/USDT', 'DASH/USDT', 'ZEC/USDT', 'ATOM/USDT', 'IOST/USDT', 'THETA/USDT', 'XTZ/USDT', 'OMG/USDT', 'COMP/USDT', 'ZRX/USDT', 'KNC/USDT', 'ZIL/USDT', 'DOGE/USDT', 'RLC/USDT', 'BAT/USDT', 'IOTA/USDT', 'XMR/USDT'],
		'7hMrKo1CbbhS58I85uaZtfz2cKUFbDIXlZEIGzCqXEMu7V8QcqjYBonrU93GfH1U': ['XLM/USDT', 'ADA/USDT', 'DASH/USDT', 'ZEC/USDT', 'ATOM/USDT', 'IOST/USDT', 'THETA/USDT', 'XTZ/USDT', 'OMG/USDT', 'COMP/USDT', 'ZRX/USDT', 'KNC/USDT', 'ZIL/USDT', 'DOGE/USDT', 'RLC/USDT', 'BAT/USDT', 'IOTA/USDT', 'XMR/USDT'],
		}#'key':['array', 'of', 'usdt-margin', 'to', 'trade']}#'BTC/USDT'

binApi2 =  {'dnB0rWq2T3XNlOHWObP6exuBVjMtI3S4BdDssUi5s4iuCgO9VK2xcpndNSfWPa3d':'Xw4A5VcHB3ZDJZuLGhxh8Lq9ouLWIxMERj1p4jeorKvvhzkDxXj3Qx1eiVonMcPs',
               '7hMrKo1CbbhS58I85uaZtfz2cKUFbDIXlZEIGzCqXEMu7V8QcqjYBonrU93GfH1U': '2Wqi6TL1L1JAQyuaEWAJisiAEmh4SsCSpopEZrQ04NIRv49gA1Yh3hBuXOsxlGOB',
         }#      'key': 'secret'}


settings = {'dnB0rWq2T3XNlOHWObP6exuBVjMtI3S4BdDssUi5s4iuCgO9VK2xcpndNSfWPa3d':{'TP': 40, 'SL': -20, 'max_skew_mult': 10, 'qty_div': 15, 'lev': 25},
			'7hMrKo1CbbhS58I85uaZtfz2cKUFbDIXlZEIGzCqXEMu7V8QcqjYBonrU93GfH1U':{'TP': 40, 'SL': -20, 'max_skew_mult': 10, 'qty_div': 15, 'lev': 25}}


#done of vars in db


print(len(pairs))
fifteens = ['XLM/USDT', 'ADA/USDT', 'DASH/USDT', 'ZEC/USDT', 'ATOM/USDT']
tens = ['OMG/USDT', 'COMP/USDT', 'ZRX/USDT', 'XMR/USDT', 'ZIL/USDT', 'KNC/USDT', 'XTZ/USDT', 'IOTA/USDT', 'BAT/USDT', 'IOST/USDT', 'THETA/USDT']
fives = ['DOGE/USDT']
threes = ['RLC/USDT']

#jarettrsdunn+alimm@gmail.com
#binApi = "8799eb6011f07a7dbba434907f71adc5f7e76af1fd12be26bb4e3294904e9852"
#binSecret = "e487c0edb6ec0f6fd839919858dce4a3f936d7d67fe0e6a4773b579173fe1355"

feeTiers = {0:{'maker': 0.02/100, 'bnbmaker': 0.018/100},
			1:{'maker': 0.016/100, 'bnbmaker': 0.0144/100},
			2:{'maker': 0.014/100, 'bnbmaker': 0.0128/100},
			3:{'maker': 0.012/100, 'bnbmaker': 0.0108/100},
			4:{'maker': 0.01/100, 'bnbmaker': 0.009/100},
			5:{'maker': 0.008/100, 'bnbmaker': 0.0072/100},
			6:{'maker': 0.006/100, 'bnbmaker': 0.0054/100},
			7:{'maker': 0.004/100, 'bnbmaker': 0.0036/100},
			8:{'maker': 0.002/100, 'bnbmaker': 0.0018/100},
			9:{'maker': 0, 'bnbmaker': 0}
			}
import multiprocessing


from strategies.mm import Place_Orders

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
	while True:
		try:
			t = fh.run()
			done = False
			while done == False:
				if t.is_alive():
					sleep(5)
				else:
					dome = True
					sleep(1)
		except:
			sleep(5)
	proc = threading.Thread(target=loop_in_thread, args=())
	print('1 proc')
	proc.start()
	proc.terminate() 
	sleep(5)

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
#t = threading.Thread(target=loop_in_thread, args=())
#t.start()
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
	#if 'Quantity less than zero' not in string and 'Unknown order sent' not in string:
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
		# TP and SL are by position, and are calculated by unrealized % * leverage (and are close to the ROE % presented by the binance web interface)
		self.TP = 40
		self.SL = 20

		#max_skew_mult is how many times the desired order size it'll accept being in position long or short before it stops orderng in that direction. For example, if we have max_skew_mult=5 and the desired order size is $20 while we have $80 in position in that direction, it'll enter as $80<$20x5. However, if we had $120 in position in that same direction it wouldn't enter that order
		self.max_skew_mult = 10

		#this is the size of the order the algo will enter. if you have $30 in your account and the qty_div is 15, it will enter orders that are $30/15= $2 large. This calculation ignores leverage
		self.qty_div = 15

		#the leverage multiplier to use - if the script refuses to enter orders after changing this, you'll need to manually close your positions and re-run
		self.lev = 25

		#binance broker apikey to use
		self.brokerKey = 'v0tiKJjj'

		self.threethousandmin = None
		self.Place_Orders = {}
		self.equity_usd		 = {}
		self.equity_btc	 = {}
		self.equity_usd_init	= {}
		self.equity_btc_init	= {}
		self.con_size		   = float( CONTRACT_SIZE )
		self.client			 = {}
		self.feeRate = None
		self.client2 = {}
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
		self.positions		  = {}
		self.spread_data		= None
		self.this_mtime		 = None
		self.ts				 = None
		self.vols			   = OrderedDict()
		self.orderRateLimit = 100
	def create_client( self, key ):
		#self.client = RestClient( KEY, SECRET, URL )
		#print(binApi)
		binance_futures = ccxt.binance(
			{"apiKey": key,
			"secret": binApi2[key],
			 'options': {'defaultType': 'future'},

	'enableRateLimit': True,
})

		#binance_futures.set_sandbox_mode(True)
			
		self.client2[key] = (ccxt.binance({	"apiKey": key,
	"secret": binApi2[key],
	'enableRateLimit': True}))
		self.client[key] = (binance_futures)
		#print(dir(self.client))		   
		m = binance_futures.fetchMarkets()
		
	

	def randomword(self, length):
	   letters = string.ascii_lowercase
	   return ''.join(random.choice(letters) for i in range(length))

	def getTrades( self, client, pair, endTime, quoteTotal, commissionTotal ):
		d		 = datetime.utcnow()  - timedelta(hours = 4)
		epoch = datetime(1970,1,1)
		st = int((d - epoch).total_seconds()) * 1000
		days = 4/24
		if start_time > st:
			st = start_time
			days	= ( datetime.utcnow() - self.start_time ).total_seconds() / SECONDS_IN_DAY
		oldTime = 9999999999999999999999999999999999999
		sleep(self.orderRateLimit / 1000)
		if endTime == 0:
			trades = client.fapiPrivateGetUserTrades({"symbol": pair.replace('/', ''), "limit": 1000, 'startTime': st })
		else:
			trades = client.fapiPrivateGetUserTrades({"symbol": pair.replace('/', ''), "limit": 1000, 'startTime': st , 'endTime': endTime})
		#print(len(trades))
		for t in trades:
			if t['time'] < oldTime:
				oldTime = t['time']
			commissionTotal = commissionTotal + float(t['commission'])
			if float(t['quoteQty']) > 0:
				quoteTotal = quoteTotal + float(t['quoteQty'])
			else:
				quoteTotal = quoteTotal - float(t['quoteQty'])
			self.feeRate = float(t['commission']) / float(t['quoteQty'])
		if len(trades) < 999:
			
			return([quoteTotal, commissionTotal, days])
		else:
			return(getTrades(client, pair, oldTime, quoteTotal, commissionTotal))

	def get_bbo( self, contract ): # Get best b/o excluding own orders
		
		# Get orderbook
		try:
			best_bid	= mids[contract]['bid']
			best_ask	= mids[contract]['ask']
		except:
			keys = []
			for key in binApi2:
				keys.append(key)
			ran = keys[random.randint(0, len(keys)-1)]
			ticker = client2[ran].fetchTicker( contract )
			best_bid = ticker['bid']
			best_ask = ticker['ask']

		return { 'bid': best_bid, 'ask': best_ask }
	
		
	def get_futures( self, client ): # Get all current futures instruments
		
		self.futures_prv	= cp.deepcopy( self.futures )
		sleep(self.orderRateLimit / 1000)
		insts			   = client.fetchMarkets()

		#print(insts[0])
		self.futures		= sort_by_key( { 
			i[ 'symbol' ]: i for i in insts if i['type'] == 'future' and i['active'] == True
		} )
		sleep(self.orderRateLimit / 1000)
		account = client.fapiPrivateGetAccount()
		feeTier = account['feeTier']
		if self.feeRate == None:
			self.feeRate = feeTiers[feeTier]['maker']

		exchange_info = client.fapiPublicGetExchangeInfo()
		for rl in exchange_info['rateLimits']:
			if rl['rateLimitType'] == 'ORDERS':
				if rl['interval'] == 'MINUTE' and rl['intervalNum'] == 1:
					self.orderRateLimit = 1.1 * (1000 * (60 / rl['limit']))
					client.rateLimit = self.orderRateLimit
					if self.Place_Orders[client.apiKey] is not None:
						self.Place_Orders[client.apiKey].orderRateLimit = self.orderRateLimit
		#sleep(100)
		#print(self.futures)
		#for k, v in self.futures.items():
			#self.futures[ k ][ 'expi_dt' ] = datetime.strptime( 
			#								   v[ 'expiration' ][ : -4 ], 
			#								   '%Y-%m-%d %H:%M:%S' )
						
		
	def get_pct_delta( self ):		 
		self.update_status()
		return sum( self.deltas.values()) / float(self.equity_btc[client.apiKey])

	def get_spot_old( self, pair ):
		print('getspotold!')
		sleep(1)
		#print(self.client2.fetchTicker( pair )['bid'])
		keys = []
		for key in binApi2:
			keys.append(key)
		ran = keys[random.randint(0, len(keys)-1)]
		return self.client2[ran].fetchTicker( pair )['bid']
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
	
	
	

		
								
	def cancelall(self, client):
		if client == None:
			for key in binApi2.keys():	
				client = ccxt.binance(
					{"apiKey": key,
					"secret": binApi2[key],
					 'options': {'defaultType': 'future'},

			'enableRateLimit': True,
		})

				#binance_futures.set_sandbox_mode(True)
					

				
		
		for pair in pairs[client.apiKey]:
			try:
				ords		= self.openorders[client.apiKey][pair]
				for order in ords:
					#print(order)
					oid = order ['info'] ['orderId']
				   # print(order)
					try:
						sleep(self.orderRateLimit / 1000)
						client.cancelOrder( oid , pair )
					except Exception as e:
						PrintException()
			except KeyError as e:
				pass
			except Exception as e:
				PrintException()
	def restart( self ):		
		try:
			strMsg = 'RESTARTING'
			print( strMsg )
			#self.cancelall(None)
			strMsg += ' '
			for i in range( 0, 5 ):
				strMsg += '.'
				print( strMsg )
				sleep( 1 )
		except:
			pass
		finally:
			os.execv( sys.executable, [ sys.executable ] + sys.argv )		
			
	def output_status ( self, client ):
		while True:
			try:
				now	 = datetime.utcnow()
				days	= ( now - self.start_time ).total_seconds() / SECONDS_IN_DAY
				print( client.apiKey + ' ********************************************************************' )
				print( client.apiKey + ' Start Time:		%s' % self.start_time.strftime( '%Y-%m-%d %H:%M:%S' ))
				print( client.apiKey + ' Current Time:	  %s' % now.strftime( '%Y-%m-%d %H:%M:%S' ))
				print( client.apiKey + ' Days:			  %s' % round( days, 1 ))
				print( client.apiKey + ' Hours:			 %s' % round( days * 24, 1 ))
				print( client.apiKey + ' Spot Price:		%s' % self.get_spot('BTC/USDT'))
				
				equity_usd = self.equity_usd[client.apiKey]
				equity_btc = self.equity_btc[client.apiKey]
				print(equity_usd)
				print(self.equity_usd_init[client.apiKey])
				pnl_usd = equity_usd - self.equity_usd_init[client.apiKey]
				pnl_btc = equity_btc - self.equity_btc_init[client.apiKey]
				
				
				#print( '%% Delta:		   %s%%'% round( self.get_pct_delta() / PCT, 1 ))
				#print( 'Total Delta (BTC): %s'   % round( sum( self.deltas.values()), 2 ))		
				#print_dict_of_dicts( {
				#	k: {
				#		'BTC': self.deltas[ k ]
				#	} for k in self.deltas.keys()
				#	}, 
				#	roundto = 2, title = 'Deltas' )
				
				#print(self.positions)
				if len(self.positions[client.apiKey]) > 1:
					for k in self.positions[client.apiKey].keys():
						try: 
							abc = self.bids[k]
						except:
							self.bids[k] = self.get_bbo(k)['bid']
					print_dict_of_dicts( {
						k: {
							'Contracts $ Value': round(self.positions[client.apiKey][ k ][ 'positionAmt' ] * self.bids[k] * 100) / 100
						} for k in self.positions[client.apiKey].keys()
						}, 

						title = client.apiKey + ' Positions' )
					
					
				if not self.monitor:
					print_dict_of_dicts( {
						k: {
							'%': self.vols[ k ]
						} for k in self.vols.keys()
						}, 
						multiple = 100, title = client.apiKey + ' Vols' )
					#print( '\nMean Loop Time: %s' % round( self.mean_looptime, 2 ))
					#self.cancelall()
				print( '' )	
				print(' ')
				days	= ( datetime.utcnow() - self.start_time ).total_seconds() / SECONDS_IN_DAY
				print(client.apiKey + ' Volumes Traded Projected Daily of Required (' + str(days) + ' days passed thus far...)')
				print(client.apiKey + ' Equity: $' + str(round(self.equity_usd[client.apiKey]*100)/100))
				btc = self.get_spot('BTC/USDT')
				print(client.apiKey + ' btc')
				percent = self.equity_usd[client.apiKey] / btc
				print('')
				print(client.apiKey + ' Equity ($):		%7.2f'   % equity_usd)
				print(client.apiKey + ' P&L ($)			%7.2f'   % pnl_usd)
				print(client.apiKey + ' Equity (BTC):	  %7.4f'   % equity_btc)
				print(client.apiKey + ' P&L (BTC)		  %7.4f'   % pnl_btc)
				print('')
				volumes = []
				tradet = 0
				feest = 0
				for pair in pairs[client.apiKey]:
					gettrades = self.getTrades(client, pair, 0, 0, 0)

					#print(gettrades)
					volume = (gettrades[0] / (gettrades[2]))
					feest = feest + gettrades[0] * self.feeRate
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
						if volume > 0:
							if self.threethousandmin == None:
								print(client.apiKey + ' ' + pair + ': ' + str(round(volume*1000)/10) + '%' + ', (Real) USD traded: $' + str(round(gettrades[0]*100)/100) + ', fees paid: $' + str(round(gettrades[1] * 10000)/10000))
							else:
								print(client.apiKey + ' ' + pair + ': ' + str(round(volume*1000)/10) + '%' + ', w/ ' + str(self.threethousandmin * self.equity_usd[client.apiKey]) + '$ minimum for sustainable strategy, ' + str(round((volume * self.threethousandmin)*1000)/10) + '%'  + ' (Real) USD traded: $' + str(round(gettrades[0]*100)/100) + ', fees paid: $' + str(round(gettrades[1] * 10000)/10000))
					else:
						if gettrades[0] > 0:
							print(client.apiKey + ' (Real) USD traded: $' + str(round(gettrades[0]*100)/100) + ', fees paid: $' + str(round(gettrades[1] * 10000)/10000))
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
				h = h * self.equity_usd[client.apiKey]
				print('')
				print(client.apiKey + ' Approx. traded volumes over 30 days: ' + str(tradet) + ', in BTC: ' + str(round(tradet/btc*1000)/1000))
				print(client.apiKey + ' Approx. Min Equity at ' + str(self.lev) + 'x in USD to Achieve 100% Daily Requirements Across 6 Highest %s Above: $' + str(round(h * 100)/100))
				diff = h / self.equity_usd[client.apiKey]
				btcneed = (((tradet * diff / btc) / 3000) )
				print(client.apiKey + ' That\'s ' + str(round(diff*100)/100) + 'x the balance now, bringing projected USD/month to: ' + str(round(tradet * diff * 100)/100) + ', and BTC: ' + str(round((tradet * diff / btc)* 100)/100))
				if self.threethousandmin is not None:
					diff = self.threethousandmin
					print(client.apiKey + ' With ' + str(self.threethousandmin) + 'x the balance now that we\'d need for the 3000 btc/month minimum, though, projected USD/month to: ' + str(round(tradet * diff * 100)/100) + ', and BTC: ' + str(round((tradet * diff / btc)* 100)/100))

				apy = 365 / (gettrades[2])
				pnl = (((self.equity_usd[client.apiKey] + feest) / self.equity_usd[client.apiKey]) -1) * 100
				pnl2 = pnl * apy
				print(client.apiKey + ' Now, if we were running in a trial mode of Binance Market Maker Program\'s Rebates, or if we had achieved these rates already, we would have earned $' + str(round(feest * 100)/100) + ' by now (on our actual equity), or rather earning ' + str(round(pnl*1000)/1000) + '% PnL so far, or ' + str(round(pnl2*1000)/1000) + ' % Annual Percentage Yield!')
				
				if btcneed < 1 and btcneed != 0:
					h = h / btcneed
					self.threethousandmin = (round(h * 100)/100) / self.equity_usd[client.apiKey]

					print(client.apiKey + ' For 3000 btc/month volumes, would make the equity minimum approx. $' + str(round(h * 100)/100))
				sleep(30)
				print('')
			except Exception as e:
				#PrintException()	
				PrintException()
				sleep(10)
		proc = threading.Thread(target=self.output_status, args=())
		print('3 proc')
		proc.start()
		proc.terminate() 	
		sleep(5)	
	def run( self ):
		for key in binApi2.keys():
			self.TP = settings[key]['TP']
			self.SL = settings[key]['SL']
			self.max_skew_mult = settings[key]['max_skew_mult']
			self.qty_div = settings[key]['qty_div']
			self.lev = settings[key]['lev']
			self.create_client(key)
			self.openorders[key] = {}
			self.positions[key] = {}
			
			self.equity_btc[key] = None
			self.equity_usd[key] = None
			self.equity_btc_init[key] = None
			self.equity_usd_init[key] = None
			self.Place_Orders[key] = None
		
		for key in binApi2.keys():
			t = multiprocessing.Process(target=self.run_first, args=(key,))
			t.start()
			

			t_ts = t_out = t_loop = t_mtime = datetime.utcnow()
			
			while True:
				client = self.client[key]
				self.get_futures(client)
				
				# Restart if a new contract is listed
				#if len( self.futures ) != len( self.futures_prv ):
				#	self.restart()
				
				
				t_now   = datetime.utcnow()
				
				# Update time series and vols
				if ( t_now - t_ts ).total_seconds() >= WAVELEN_TS:
					t_ts = t_now
					
					self.update_timeseries()
					self.update_vols()
				
				# ()
				
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
	
	def run_first( self, key ):
		
		
		
		#self.cancelall()
		self.logger = get_logger( 'root', LOG_LEVEL )
		# Get all futures contracts
		for client in self.client.values():
			self.get_futures(client)
			#sleep(10)
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
			t = threading.Thread(target=self.looptiloop, args=(client,))
			t.start()
			
			self.this_mtime = getmtime( __file__ )
			self.symbols	= [ BTC_SYMBOL ] + list( pairs[client.apiKey]); self.symbols.sort()
			self.deltas	 = OrderedDict( { s: None for s in self.symbols } )
			
			# Create historical time series data for estimating vol
			ts_keys = self.symbols + [ 'timestamp' ]; ts_keys.sort()
			
			self.ts = [
				OrderedDict( { f: None for f in ts_keys } ) for i in range( NLAGS + 1 )
			]
			
			self.vols   = OrderedDict( { s: VOL_PRIOR for s in self.symbols } )
			#sleep(10)
			

			self.Place_Orders[client.apiKey] = Place_Orders(client, multiprocessing, self.brokerKey, self.qty_div, self.orderRateLimit, self.max_skew_mult, self.get_precision, math, self.TP, self.SL, asyncio, sleep, threading, PrintException, ticksize_floor, ticksize_ceil, pairs[client.apiKey], fifteens, tens, fives, threes, self.con_size, self.get_spot, self.equity_btc[client.apiKey], self.positions[client.apiKey], self.get_ticksize, self.vols, self.get_bbo, self.openorders[client.apiKey], self.equity_usd[client.apiKey], self.randomword, self.logger, PCT_LIM_LONG, PCT_LIM_SHORT, DECAY_POS_LIM, MIN_ORDER_SIZE, CONTRACT_SIZE, MAX_LAYERS, BTC_SYMBOL, RISK_CHARGE_VOL, BP)
				
			t = threading.Thread(target=self.updateOrders, args=(client,))
			t.daemon = True
			t.start()	
			
			t = threading.Thread(target=self.updateBids, args=())
			t.daemon = True
			t.start()	
			
			t = threading.Thread(target=self.updatePositions, args=(client,))
			t.daemon = True
			t.start()	
			try:
				self.positions[client.apiKey]  = OrderedDict( { f: {
					'size':		 0,
					'positionAmt':	  0,
					'indexPrice':   None,
					'markPrice':	None
				} for f in pairs[client.apiKey] } )
				sleep(self.orderRateLimit / 1000)
				positions	   = client.fapiPrivateGetPositionRisk()

				#print('lala')
				#print(positions)
				
				for pos in positions:
					if pos['symbol'].split('USDT')[0] + '/USDT' in pairs[client.apiKey]:
						pos['positionAmt'] = float(pos['positionAmt'])
						pos['entryPrice'] = float(pos['entryPrice'])
						pos['unRealizedProfit'] = float(pos['unRealizedProfit'])
						pos['leverage'] = float(pos['leverage'])
						notional = math.fabs(pos['positionAmt']) * pos['entryPrice']
						#fee = self.feeRate * notional
						#notional = notional - fee
						if notional > 0:
							notionalplus = notional + pos['unRealizedProfit']
							percent = ((notionalplus / notional) -1) * 100

							pos['ROE'] = percent * pos['leverage']
						else:
							pos['ROE'] = 0
						self.positions[client.apiKey][ pos['symbol'].split('USDT')[0] + '/USDT'] = pos

						#print(pos['ROE'])	
				if self.Place_Orders[client.apiKey] is not None:
					self.Place_Orders[client.apiKey].positions = self.positions[client.apiKey]
				
			except Exception as e:
				PrintException()	
			for pair in pairs[client.apiKey]:
				sleep(self.orderRateLimit / 1000)
				try:
					client.fapiPrivatePostLeverage({'symbol': pair.replace('/USDT', 'USDT'), 'leverage': self.lev})
				except:
					sleep(self.orderRateLimit / 1000)
					direction = 'sell'
					if self.positions[client.apiKey][fut]['positionAmt'] < 0:
						direction = 'buy'
					qty = self.math.fabs(self.positions[client.apiKey][fut]['positionAmt'])
					self.creates[fut] = True
					print(str(qty) + ' ' + fut)
					self.Place_Orders[client.apiKey].create_order(  fut, "Market", direction, qty, None, {"newClientOrderId": "x-v0tiKJjj-" + self.randomword(20)})
					self.positions[client.apiKey][fut]['ROE'] = 0
			try:
				t = threading.Thread(target=self.output_status, args=(client,))
				t.daemon = True
				t.start()
					

				t = threading.Thread(target=self.Place_Orders[client.apiKey].run(), args=())
				t.daemon = True
				t.start()


				
			except Exception as e:
				PrintException()

			self.update_status()
			#sleep(3)
	def updateOrders(self, client):
		while True:
			try:
				for pair in pairs[client.apiKey]:
					try:
						#print(pair)
						try:
							sleep(self.orderRateLimit / 1000)
							self.openorders[client.apiKey][pair] = client.fetchOpenOrders( pair )
						except Exception as e:
							PrintException()
					except:
						sleep(5)
				if self.Place_Orders[client.apiKey] is not None:
					self.Place_Orders[client.apiKey].openorders = self.openorders[client.apiKey]
			except:
				PrintException()
				sleep(1)
	def updatePositions( self, client ):
		while True:
			try:
				self.positions[client.apiKey]  = OrderedDict( { f: {
					'size':		 0,
					'positionAmt':	  0,
					'indexPrice':   None,
					'markPrice':	None
				} for f in pairs[client.apiKey] } )
				sleep(self.orderRateLimit / 1000)
				positions	   = client.fapiPrivateGetPositionRisk()

				#print('lala')
				#print(positions)
				
				for pos in positions:
					if pos['symbol'].split('USDT')[0] + '/USDT' in pairs[client.apiKey]:
						pos['positionAmt'] = float(pos['positionAmt'])
						pos['entryPrice'] = float(pos['entryPrice'])
						pos['unRealizedProfit'] = float(pos['unRealizedProfit'])
						pos['leverage'] = float(pos['leverage'])
						notional = math.fabs(pos['positionAmt']) * pos['entryPrice']
						fee = self.feeRate * notional
						notional = notional - fee
						if notional > 0:
							notionalplus = notional + pos['unRealizedProfit']
							percent = ((notionalplus / notional) -1) * 100

							pos['ROE'] = percent * pos['leverage']
						else:
							pos['ROE'] = 0

						self.positions[client.apiKey][ pos['symbol'].split('USDT')[0] + '/USDT'] = pos
						
				if self.Place_Orders[client.apiKey] is not None:
					self.Place_Orders[client.apiKey].positions = self.positions[client.apiKey]
				#print(self.positions)	
			except Exception as e:
				PrintException()
				sleep(5)
	def updateBids( self ):
		while True:
			alist = []
			for key in pairs.keys():
				for pair in pairs[key]:
					if pair not in alist:
						alist.append(pair)
						#print(pair)
			for pair in alist:
				try:
					if pair in mids:
						self.bids[pair] = mids[pair]['bid']
					else:
						self.bids[pair] = self.get_spot_old(pair)
				except:
					PrintException()
					sleep(5)
	def looptiloop(self, client):
		while True:
		
			try:
				while True:
					balance = client.fetch_balance()
					self.equity_usd[client.apiKey] = balance['USDT']['total']

					self.equity_btc[client.apiKey] = self.equity_usd[client.apiKey] / self.get_spot('BTC/USDT')
					if self.equity_usd_init[client.apiKey] == None and self.equity_usd[client.apiKey] > 0:
						self.equity_usd_init[client.apiKey]	= self.equity_usd[client.apiKey]
						self.equity_btc_init[client.apiKey]	= self.equity_btc[client.apiKey] 
					if self.Place_Orders[client.apiKey] is not None:
						self.Place_Orders[client.apiKey].equity_btc = self.equity_btc[client.apiKey]
						self.Place_Orders[client.apiKey].equity_usd = self.equity_usd[client.apiKey]
					sleep(1)
					
			except Exception as e:
				print(client.apiKey)
				PrintException()
				sleep(5)
			
				
				
				
				
				

	
	def update_status( self ):
		  
			 
		abc=123		
		#self.deltas = OrderedDict( 
		#	{ k: float(self.positions[ k ][ 'positionAmt' ]) for k in pairs}
		#)
		

		
		
	
	def update_timeseries( self ):
		
		if self.monitor:
			return None
		
		for t in range( NLAGS, 0, -1 ):
			self.ts[ t ]	= cp.deepcopy( self.ts[ t - 1 ] )
		
		spot					= self.get_spot('BTC/USDT')
		self.ts[ 0 ][ BTC_SYMBOL ]	= spot
		alist = []
		for key in pairs.keys():
			for pair in pairs[key]:
				if pair not in alist:
					alist.append(pair)
					#print(pair)
		for c in alist:
			
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
		for key in self.Place_Orders.keys():
			if self.Place_Orders[key] is not None:
				self.Place_Orders[key].vols = self.vols					
		
if __name__ == '__main__':
	
	try:
		mmbot = MarketMaker( monitor = args.monitor, output = args.output )
		mmbot.run()
	except( KeyboardInterrupt, SystemExit ):
		print( "Cancelling open orders" )
		mmbot.cancelall(None)
		sys.exit()
	except:
		print( traceback.format_exc())
		if args.restart:
			mmbot.cancelall(None)
			mmbot.restart()
		
