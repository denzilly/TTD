import redis
import datetime as dt
r = redis.Redis('localhost', charset="utf-8", decode_responses=True)



# if r.get("asdfs") == None:
#     print("it was none")
#     r.set("asdfs",str(dt.datetime.now()))

# else:
#     print(r.get("asdfs"))


buyvotes = len(r.lrange("buy",0,-1))
print(r.lrange('buy',0,-1))
print(buyvotes)