import redis
import datetime as dt
import time
r = redis.Redis('localhost', charset="utf-8", decode_responses=True)



# if r.get("asdfs") == None:
#     print("it was none")
#     r.set("asdfs",str(dt.datetime.now()))

# else:
#     print(r.get("asdfs"))

while 1:
    print(r.lrange("buy",0,-1))
    time.sleep(3)