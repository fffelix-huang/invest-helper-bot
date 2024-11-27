import redis
from linebot.v3.messaging import ReplyMessageRequest, TextMessage

r = redis.Redis(host='localhost', port=6379, db=0)
