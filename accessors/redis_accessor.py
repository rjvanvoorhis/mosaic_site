from redis import Redis
from rq import Queue

class RedisAccessor(object):
    def __init__(self, queue_name='default', connection=None):
        connection = connection if connection is not None else Redis()
        self.q = Queue(queue_name, connection=connection)

    def submit_job(self, func, args, timeout='10m'):
        job = self.q.enqueue_call(func=func, args=args, timeout=timeout)
        return job

    def get_job(self, job_id):
        job = self.q.fetch_job(job_id)
        return job

