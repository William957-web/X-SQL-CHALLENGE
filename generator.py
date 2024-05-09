from sqlitedict import SqliteDict, encode, decode, decode_key
import pickle
import base64
import os

#payload = Payload('echo "pwned by whale120" > proof.txt')
db = SqliteDict("product.sqlite")
db["1"] = {"name":"Edible ramen", "description":"It's a delicious and quite well knowned dish.", "price":"10"}
db["2"] = {"name":"Edible corn", "description":"Yummy OuO", "price":"999999999999"}
db["3"] = {"name":"Edible whale", "description":"womp oWo?", "price":"999999999999"}
db.commit()
db.close()
