DROP TABLE IF EXISTS post;

CREATE TABLE post (
    post_id TEXT PRIMARY KEY,
    job_id TEXT,
    filename TEXT,
    job_status TEXT,
    comp_time INTEGER
);
