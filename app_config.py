import os


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_URI = 'https://127.0.0.1:5000/'
TIME_PATH = os.path.join(PROJECT_PATH, 'avg_time.pickle')
TILE_DIRECTORY = os.path.join(PROJECT_PATH,'photomosaic/tile_directory')
DATABASE_SCHEMA = os.path.join(PROJECT_PATH,'schemas/mosaic.sql')
UPLOAD_FOLDER = os.path.join(PROJECT_PATH,'MEDIA')
DATABASE = os.path.join(PROJECT_PATH,'mosaic.sqlite')
