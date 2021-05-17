import redis

import math

#from trader import *
from modules.trader import *

r = redis.Redis('localhost', charset="utf-8", decode_responses=True)


def get_trade_direction(r):

    data = {}
    for key in ["buy","sell","votes","hold"]:
        data[key] = len(r.lrange(key, 0, -1))
    for key in ["threshold", "position", "viewer_count"]:
        data[key] = r.get(key)

    data['threshold'] = int(data['threshold'])
    data['viewer_count'] = int(data['viewer_count'])

    direction = "hold"

    if data['position'] == "long":
        if (data["sell"] >= data["threshold"] and data["sell"] >= data["hold"]):
            direction = "sell"        
        elif  (data["hold"] > data["threshold"]):
            direction = "hold"
        else:
            direction = "hold"
    if data['position'] == "short":
        if (data["buy"] >= data["threshold"] and data["buy"] >= data["hold"]):
             direction = "buy"
        elif  (data["hold"] > data["threshold"]):
            direction = "hold"
        else:
            direction = "hold"




    elif data['position'] == "neutral":
        
        if (data["buy"] >= data["sell"] and data["buy"] >= data["threshold"] and data["buy"] >= data["hold"]):
            direction = "buy"
            
        if (data["sell"] > data["buy"] and data["sell"] >= data["threshold"] and data["sell"] >= data["hold"]):
            direction = "sell"

        


    return direction,data



def trade(r):
    direction, data = get_trade_direction(r)

    if direction == "buy":
        buy(det_qty(data["buy"], data['viewer_count']), realtrade=True)
        print("BUY BUY BUY")
        r.set("popup", "open")

    elif direction == "sell":
        sell(det_qty(data["sell"], data['viewer_count']), realtrade=True)
        print("SELL SELL SELL")
        r.set("popup", "open")

    else:
        print("Holding")


def get_nexttrade(r):
    direction, data = get_trade_direction(r)
    
    if direction == "buy":
        buy(det_qty(data["buy"], data['viewer_count']), realtrade=False)
        
    elif direction == "sell":
        sell(det_qty(data["sell"], data['viewer_count']), realtrade=False)
        
    else:
        r.set("nexttrade", "HOLD")




def reset(r):

    for key in ["buy","sell","votes","hold","threshold"]:
        r.delete(key)
    if int(r.get("viewer_count")) > 100:
        r.set("threshhold", math.ceil(int(r.get("viewer_count")) / 10))
    else:
        r.set("threshold", 10)
    
    print(f'Viewer count : {r.get("viewer_count")}')
    print(f'Threshold : {r.get("threshold")}')




#determine the quantity to sell, in %
def det_qty(direction,viewers):
    
    if viewers > 100:
        qty_pct = ( ( ( direction / viewers ) - 0.1 ) * 2) 
    else:
        qty_pct = ((direction - 10) * .02)

    if qty_pct > 1:
        qty_pct = 1

    return qty_pct