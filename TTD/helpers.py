from datetime import date
import csv

def get_trade_keys():
    keys = ["symbol", "price", "origQty", "executedQty", "type", "side", "fills"]
    return keys



def neat(trade, keys):
    #create a compact dict of trade info
    t_c ={}
    for x in keys:
        if x == "fills":
            try:
                t_c["Fill_price"] = trade[x][0]["price"]
                t_c["Fill_qty"] = trade[x][0]["qty"]
            except IndexError:
                print("failed to fill")
                pass
        else:
            t_c[x] = trade[x]
    output = [(key + ": " + t_c[key]) for key in t_c.keys()]
    pif(output)
    



def pif(words):
    size = max(len(word) for word in words)
    print('*' * (size + 4))
    for word in words:
        print('* {:<{}} *'.format(word, size))
    print('*' * (size + 4))



def log_trade(trade, keys):
    #create a compact dict of trade info
    
    t_c ={}
    for x in keys:
        if x == "fills":
            try:
                t_c["Fill_price"] = trade[x][0]["price"]
                t_c["Fill_qty"] = trade[x][0]["qty"]
            except IndexError:
                print("failed to fill")
                pass
        else:
            t_c[x] = trade[x]
    
    
    with open(str(date.today()) + ".csv", "a") as f:
        writer = csv.writer(f)
        for key, value in t_c.items():
            writer.writerow([key,value])
        print("trade was logged")




class vote_cache:
    def __init__(self, buy_votes, sell_votes, hold_votes, state):
        self.buy_votes = 0
        self.sell_votes = 0
        self.hold_votes = 0
        self.state = "short"



    def add_vote(self, vote_type):
        if vote_type == "buy":
            self.buy_votes += 1
        if vote_type == "sell":
            self.sell_votes += 1
        if vote_type == "hold":
            self.hold_votes += 1

    
    def clear_votes(self):
        self.buy_votes = 0
        self.sell_votes = 0
        self.hold_votes = 0


# class Wallet:
#     def __init__(self, doge_bal, usdt_bal):
#         self.doge_bal = doge_bal
#         self.usdt_bal = usdt_bal

#     def check(self):
#         pif(["USDT Balance: " + self.usdt_bal, "DOGE Balance: " + self.doge_bal ])
