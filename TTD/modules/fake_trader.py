import redis

r = redis.Redis('localhost', charset="utf-8", decode_responses=True)


price = 0.4020


def check_bal():

    #real balance logic here


    #fake balance logic here

    dogebal = r.get("dogebal")
    usdtbal = r.get("usdtbal")




def buy(qty_pct,realtrade):
    #real buy logic


    #fake buy logic
    data = {}
    for key in ["usdtbal", "dogebal"]:
        data[key] = float(r.get(key))



    #quantities in respective CCY

    buy_u = 10  + (qty_pct * data['usdtbal'])
    buy_d = buy_u / price
    remaining_u_u = ( data['usdtbal'] - buy_u )
    remaining_d_d = ( data['dogebal'] + buy_d) 

    #avoid underspending
    if ( remaining_u_u < 10): 
        buy_u = 0.99 * data["usdtbal"]
        print("might as well just do all of it..")
        remaining_u_u = ( data['usdtbal'] - buy_u )
        remaining_d_d = ( data['dogebal'] + buy_d)
        if realtrade:
            r.set("position","long")
    
    
    

    if  realtrade:
        print(f" buy percentage = {qty_pct}")
        print(f"balance is {data['dogebal']} DOGE")
        print(f"buying {buy_d} DOGE @ {price} = {buy_u} USDT")

        r.set("dogebal", remaining_d_d )
        r.set("usdtbal",  remaining_u_u )

    r.set("nexttrade", f"Buy {round(buy_d,2)} DOGE")




def sell(qty_pct,realtrade):
    #real sell logic

    #fake sell logic
    data = {}
    for key in ["usdtbal", "dogebal"]:
        data[key] = float(r.get(key))


    #quantities in respective CCY

    sell_d = (10 / price) + qty_pct * data['dogebal']
    sell_u = sell_d * price
    remaining_d_u = ( data['dogebal'] - sell_d ) * price 
    remaining_u_u = ( data['usdtbal'] + sell_u)

    #avoid underspending
    if ( remaining_d_u < 10): 
        sell_d = 0.99 * data["dogebal"]
        print("might as well just do all of it..")
        remaining_d_u = ( data['dogebal'] - sell_d ) * price 
        remaining_u_u = ( data['usdtbal'] + sell_u)
        if realtrade:
            r.set("position","short")
    

    if realtrade:
        print(f" sell percentage = {qty_pct}")
        print(f"balance is {data['dogebal']} DOGE")
        print(f"selling {sell_d} DOGE @ {price} = {sell_u} USDT")

        r.set("dogebal", remaining_d_u / price )
        r.set("usdtbal",  remaining_u_u )

    r.set("nexttrade", f"Sell {round(sell_d,2)} DOGE")


