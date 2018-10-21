import subprocess
import app_config
import os
from pdb import set_trace as bp

from flask import (Flask, send_from_directory, send_file, 
                   request, flash,
                   redirect, url_for, render_template)
from flask_restful import Api
from werkzeug.utils import secure_filename
from helpers.helpers import get_post_id
from resources.post_resource import PostResource
from accessors.db_accessor import DbAccessor
import app_config
from tasks.tasks import make_mosaic
from helpers.helpers import get_post_id
import time
from PIL import Image
from accessors.tile_calculator_accessor import TileCalculator
import requests
import json


app = Flask(__name__, static_url_path=app_config.UPLOAD_FOLDER)
api = Api(app)

api.add_resource(PostResource, '/api/post_resource/<string:post_id>',
                 endpoint='post_result')

@app.route('/result/<string:post_id>', endpoint='result')
def img_result(post_id):
    context = dict()
    with app.test_client() as client:
        res = client.get(url_for('post_result', post_id=post_id))
    res = json.loads(res.get_data())
    filename = os.path.basename(res['filename'])
    if res['status'] == 'finished':
        filename = 'mosaic_of_%s'%filename
    img_url = url_for('uploaded_file',filename=filename)
    time_left = res['comp_time'] - int(time.time())
    if time_left <= 0:
        status = 'Image will be completed momentarily'
    else:
        status = 'Estimated time remaining: %s seconds'%time_left
    return render_template('result.html', status=status,
                    img_url=img_url) 

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    enlargement = 3
    threads = 3
    tile_size = 8
    tile_directory = app_config.TILE_DIRECTORY
    max_repeats = 0
    post_id = get_post_id()
    if request.method == 'POST':
        if 'upload_image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['upload_image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            full_path = os.path.join(app_config.UPLOAD_FOLDER,filename)
            file.save(full_path)
            img = Image.open(full_path)
            size = img.size
            img.close()
            calc = TileCalculator()
            comp_time = calc.get_time(size, enlargement, tile_size, threads)
            db = DbAccessor()
            args = (post_id, full_path, enlargement, tile_directory,
                    threads, max_repeats, tile_size)
            db.submit_job(post_id, full_path, comp_time,
                          make_mosaic, args)
            print(post_id)
            print(comp_time - int(time.time()))
            #return redirect(url_for('uploaded_file', filename=filename))
            return redirect(url_for('result', post_id=post_id))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app_config.UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    subprocess.Popen(['python','worker.py'])
    app.run(debug=True)
