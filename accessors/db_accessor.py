import sqlite3
import app_config

from pdb import set_trace as bp
from flask import g
from accessors.redis_accessor import RedisAccessor

class DbAccessor(object):
    def __init__(self):
        self.rqa = RedisAccessor()
        try:
            if 'db' not in g:
                g.db = sqlite3.connect(app_config.DATABASE,
                                       detect_types=sqlite3.PARSE_DECLTYPES
                                       )
                g.db.row_factory = sqlite3.Row
            self.db = g.db
        except RuntimeError:
            self.db = sqlite3.connect(app_config.DATABASE,
                                       detect_types=sqlite3.PARSE_DECLTYPES
                                       )
            self.db.row_factory = sqlite3.Row
    
    def submit_job(self, post_id, filename, comp_time, func, args):
        job = self.rqa.submit_job(func, args)
        self.insert_job(post_id, job, filename, comp_time) 

    def close_db(self):
        try:
            self.db = g.pop('db', None)
        except RuntimeError:
            pass
        if self.db is not None:
            self.db.close()

    def insert_job(self, post_id, job, filename, comp_time):
        job_id = job.get_id()
        job_status = job.get_status()
        query = """INSERT INTO post (post_id, job_id, job_status, filename, comp_time) 
                   values (?, ?, ?, ?, ?)"""
        self.db.execute(query, (post_id, job_id, job_status, filename, comp_time))
        self.db.commit()

    def get_filename(self, post_id):
        query = """SELECT filename from post WHERE post_id = ?"""
        cur = self.db.execute(query, (post_id, ))
        return cur.fetchone()['filename']

    def get_job_status(self, post_id ):
        query = """SELECT job_status from post WHERE post_id = ?"""
        cur = self.db.execute(query, (post_id, ))    
        return cur.fetchone()['job_status']
   
    def get_job_id(self, post_id):
        query = """SELECT job_id from post WHERE post_id = ?"""
        cur = self.db.execute(query, (post_id, ))    
        return cur.fetchone()['job_id']

    def get_comp_time(self, post_id):
        query = """SELECT comp_time from post WHERE post_id = ?"""
        cur = self.db.execute(query, (post_id, ))    
        return cur.fetchone()['comp_time']
 
   
    def update_job_status(self, post_id):
        current_status = self.get_job_status(post_id)
        if current_status != 'finished':
            job_id = self.get_job_id(post_id)
            job_status = self.rqa.get_job(job_id).get_status()
            
            query = """UPDATE post set job_status = ? WHERE post_id = ?"""
            self.db.execute(query, (job_status, post_id))
            self.db.commit()

    def create_tables(self):
        with open(app_config.DATABASE_SCHEMA, 'r') as fn:
            self.db.executescript(fn.read())
