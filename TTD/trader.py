from binance.client import Client
import os

key = os.environ['API']
secret = os.environ['SECRET']



client = Client(key, secret)


# side = "SELL"


# if (side == "BUY"):
#     client.create_order(
#         symbol='DOGEUSDT',
#         side=Client.SIDE_BUY,
#         type=Client.ORDER_TYPE_MARKET,
#         quantity=40)

# if side == "SELL":
#     client.create_order(
#         symbol='DOGEUSDT',
#         side=Client.SIDE_SELL,
#         type=Client.ORDER_TYPE_MARKET,
#         quantity=120)
