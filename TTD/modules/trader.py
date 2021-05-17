from binance.client import Client
import os
import time
import redis
import simpleaudio as sa

r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
key = os.environ['API']
secret = os.environ['SECRET']
client = Client(key, secret)
#client.API_URL = "https://testnet.binance.vision/api"


#set the balance in redis
def set_bal(r):
    
    #uncomment this for real trading
    r.set("dogebal",client.get_asset_balance(asset='DOGE')['free'])
    r.set("usdtbal",client.get_asset_balance(asset='uSDT')['free'])

    dogebal_u = (float(r.get("dogebal")) * float(r.get("price")))
    usdtbal = float(r.get("usdtbal"))
    
    print(dogebal_u)
    print(usdtbal)

    if dogebal_u < 10:
        r.set("position", "short")
    elif usdtbal < 10:
        r.set("position", "long")
    else:
        r.set("position", "neutral")

    print(f" current position is: {r.get('position')}")

    

    
#set the latest mid in redis
def set_price(r):

    book = client.get_order_book(symbol="DOGEUSDT")
    bestbid = float(book['bids'][0][0])
    bestoffer = float(book['asks'][0][0])
    mid = (bestbid + bestoffer) / 2

    r.set("price", round(mid,4))

    print(f"[  {bestbid}   {mid}   {bestoffer}   ]")



def buy(qty_pct,realtrade):
   


    #fake buy logic
    data = {}
    for key in ["usdtbal", "dogebal", "price"]:
        data[key] = float(r.get(key))



    print(f"PRICE IS {data['price']}")
    #quantities in respective CCY

    buy_u = 10  + (qty_pct * data['usdtbal'])
    buy_d = buy_u / data['price']
    remaining_u_u = ( data['usdtbal'] - buy_u )
    remaining_d_d = ( data['dogebal'] + buy_d) 

    #avoid underspending
    if ( remaining_u_u < 10): 
        buy_u = 0.99 * data["usdtbal"]
        print("might as well just do all of it..")
        remaining_u_u = ( data['usdtbal'] - buy_u )
        remaining_d_d = ( data['dogebal'] + buy_d)
          
    
    
    

    if  realtrade:
        print(f" buy percentage = {qty_pct}")
        print(f"balance is {data['dogebal']} DOGE")
        print(f"buying {round(buy_d,2)} DOGE @ {data['price']} = {buy_u} USDT")
        r.set("thistrade", f"Buying {round(buy_d,2)} DOGE @ {data['price']}")
        r.set("lasttrade", f"Bought {round(buy_d,2)} DOGE @ {data['price']}")
        wave_obj = sa.WaveObject.from_wave_file("assets/sounds/dogs.wav")
        play_obj = wave_obj.play()
        #binance_buy(buy_d)
        

        # #uncomment when debugging
        r.set('usdtbal', data['usdtbal'] - buy_u)
        r.set('dogebal', data['dogebal'] + buy_d)

    r.set("nexttrade", f"Buy {round(buy_d,2)} DOGE")






def sell(qty_pct,realtrade):
    
    data = {}
    for key in ["usdtbal", "dogebal", "price"]:
        data[key] = float(r.get(key))


    #quantities in respective CCY

    sell_d = (10 / data['price']) + qty_pct * data['dogebal']
    sell_u = sell_d * data['price']
    remaining_d_u = ( data['dogebal'] - sell_d ) * data['price'] 
    remaining_u_u = ( data['usdtbal'] + sell_u)

    #avoid underspending
    if ( remaining_d_u < 10): 
        sell_d = 0.99 * data["dogebal"]
        print("might as well just do all of it..")
        remaining_d_u = ( data['dogebal'] - sell_d ) * data['price'] 
        remaining_u_u = ( data['usdtbal'] + sell_u)
            

    if realtrade:
        print(f" sell percentage = {qty_pct}")
        print(f"balance is {data['dogebal']} DOGE")
        print(f"selling {round(sell_d,2)} DOGE @ {data['price']} = {sell_u} USDT")
        r.set("thistrade", f"Selling {round(sell_d,2)} DOGE @ {data['price']}")
        r.set("lasttrade", f"Sold {round(sell_d,2)} DOGE @ {data['price']}")
        wave_obj = sa.WaveObject.from_wave_file("assets/sounds/dogs.wav")
        play_obj = wave_obj.play()
        #binance_sell(sell_d)
       


        # #uncomment when debugging
        r.set('usdtbal', data['usdtbal'] + sell_u)
        r.set('dogebal', data['dogebal'] - sell_d)

    r.set("nexttrade", f"Sell {round(sell_d,2)} DOGE")







def binance_buy(qty):
    qty = round(qty,1)
    order = client.order_market_buy(
            symbol='DOGEUSDT',
            quantity=qty)

    #neat(order, get_trade_keys())
    


def binance_sell(qty):
    qty = round(qty,1)
    order = client.order_market_sell(
            symbol='DOGEUSDT',
            quantity=qty)

    #neat(order, get_trade_keys())
    


