import redis
from rq import Queue, Connection, Worker

def start_workers():
    listen = ['default']
    conn = redis.Redis()
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()


if __name__ == '__main__':
    start_workers()
