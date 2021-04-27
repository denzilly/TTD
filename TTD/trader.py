from binance.client import Client
import os
import time

from helpers import *



key = os.environ['TESTAPI']
secret = os.environ['TESTSECRET']
client = Client(key, secret)
client.API_URL = "https://testnet.binance.vision/api"



def check_bal():
    bal = {}

    bal['BTC'] = client.get_asset_balance(asset='BTC')['free']
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












#TEST LOOP

side = "dfg"

# while(True):


#     BTC_bal = client.get_asset_balance(asset='BTC')['free']
#     USDT_bal = client.get_asset_balance(asset='uSDT')['free']

#     pif(["Current Balance:","BTC :" + BTC_bal, "USDT :" + USDT_bal])

#     if (side == "BUY"):
#         buy(check_bal())
#     if side == "SELL":
#         sell(check_bal())


#     side = input("what do you want to do?")
#     if side == "break":
#         break

#     time.sleep(2)

    
#     #print(client.get_aggregate_trades(symbol='BTCUSDT'))