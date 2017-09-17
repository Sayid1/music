import redis

conn = None


def connect():
    global conn
    if conn is None:
        print("连接redis")
        redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
        conn = redis.StrictRedis(connection_pool=redis_pool)
    else:
        pass
    return conn


def setUrl(value):
    global conn
    return conn.sadd('request_url', value)


def setMusic(name, musician_ids):
    global conn
    return conn.sadd('music', hash('%s%s' % (name, musician_ids)))
