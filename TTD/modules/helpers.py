from datetime import date
import csv

from modules.vote_logic import det_qty


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


#find longest list in a list of lists
def longest_list(l):
    longest = 0
    for x in l:
        if len(l) > longest:
            longest = l


