import pickle
import time
from app_config import TIME_PATH
import os


def calculate_tile_number(size, enlargement, tile_size, threads):
    w,h = size
    width = (w * enlargement) // tile_size
    height = (h * enlargement) // tile_size
    tile_number = width * height
    tiles = (tile_number) // threads
    return tiles

class TileCalculator:
    def __init__(self):
        self.avg_time = 1.0
        self.total_tiles = 0
        self.total_time = 0
        self.fp = TIME_PATH
        self.load()

    def get_time(self, shape, enlargement, tile_size, threads):
        tiles = calculate_tile_number(shape, enlargement, tile_size, threads)
        completion_time = int(time.time()) + int(self.avg_time * tiles)
        return completion_time

    def update(self, tiles, elapsed_time):
        self.load()
        self.total_tiles += tiles
        self.total_time += elapsed_time
        if self.total_tiles > 0 and self.total_time > 0:
            self.avg_time = self.total_time/ self.total_tiles
            self.save()

    def load(self):
        if not os.path.isfile(self.fp):
            return None
        with open(self.fp,'rb') as fn: 
            out_dict = pickle.load(fn)
            self.avg_time = out_dict['avg_time']
            self.total_tiles = out_dict['total_tiles']
            self.total_time = out_dict['total_time']

    def save(self):
        out_dict = {'avg_time': self.avg_time,
                    'total_tiles' : self.total_tiles,
                    'total_time' : self.total_time}
        with open(self.fp,'wb') as fn: 
            pickle.dump(out_dict, fn)


