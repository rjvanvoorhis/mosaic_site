from flask_restful import Resource
from accessors.db_accessor import DbAccessor
from accessors.redis_accessor import RedisAccessor


class PostResource(Resource):
    def __init__(self):
        self.db = DbAccessor()
    
    def get(self, post_id):
        self.db.update_job_status(post_id)
        filename = self.db.get_filename(post_id) 
        status = self.db.get_job_status(post_id)
        comp_time = self.db.get_comp_time(post_id)
        return {'status': status, 'filename': filename, 'comp_time':comp_time}
    
