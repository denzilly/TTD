from binance.client import Client
import os
import time

from helpers import *



key = os.environ['API']
secret = os.environ['SECRET']
client = Client(key, secret)
#client.API_URL = "https://testnet.binance.vision/api"



def check_bal():
    bal = {}

    bal['DOGE'] = client.get_asset_balance(asset='DOGE')['free']
    bal['USDT'] = client.get_asset_balance(asset='uSDT')['free']

    return bal



def buy(bal):
    order = client.order_market_buy(
            symbol='BTCUSDT',
            quoteOrderQty=bal['USDT'])

    neat(order, get_trade_keys())
    log_trade(order,get_trade_keys())


def sell(bal):
    order = client.order_market_sell(
            symbol='BTCUSDT',
            quantity=bal['BTC'])

    neat(order, get_trade_keys())
    log_trade(order,get_trade_keys())


def get_price():
    book = client.get_order_book(symbol="DOGEUSDT")
    bestbid = float(book['bids'][0][0])
    bestoffer = float(book['asks'][0][0])
    mid = (bestbid + bestoffer) / 2

    print(f"[  {bestbid}   {mid}   {bestoffer}   ]")
    


get_price()