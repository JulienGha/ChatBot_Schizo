import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

# here is the redis url, as we use docker we can just put the name
redis_url = 'redis://redis:6379'

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()