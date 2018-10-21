from photomosaic.photomosaic import Photo_Mosaic
import os


def make_mosaic(post_id, filename, enlargement,
                tile_directory, threads, max_repeats, tile_size):
    print('post_id: %s'%post_id)
    
    mos = Photo_Mosaic(filename, enlargement=enlargement,
                       tile_directory=tile_directory, threads=threads,
                       max_repeats=max_repeats, tile_size=tile_size)
    base_name = os.path.basename(filename)
    final_path = 'mosaic_of_'+base_name
    filename=os.path.join(os.path.dirname(filename),final_path)
    mos.out_path = filename
    mos.save()
    return filename 
