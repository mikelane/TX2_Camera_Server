import pathlib
import sys

sys.path.insert(0, str(pathlib.Path('../Image_Capture').resolve()))

from flask import Flask, render_template
import os
from datetime import datetime
import time
import calendar
import traceback

from capture_raw_image import capture_raw
from process_image import process_raw_file

app = Flask(__name__)


@app.route('/')
def health_check():
    return 'Server is operational'


@app.route('/take_picture', )
def take_picture():
    config_file = pathlib.Path(pathlib.Path().home(), '.config', 'Image_Capture', 'camera.cfg')
    output_filepath = pathlib.Path('static', 'images', '{:%Y-%m-%d}'.format(datetime.today()), 'img_{:d}.png'.format(calendar.timegm(time.gmtime())))
    raw_filepath = pathlib.Path(output_filepath.parent, '{}.raw'.format(output_filepath.stem))
    os.makedirs(name=str(output_filepath.parent), exist_ok=True)

    try:
        capture_raw(filename=str(raw_filepath), verbose=False, device=0, count=1, config_filename=str(config_file))
    except OSError as e:
        return 'Something went wrong with the image capture. {}'.format(traceback.format_exc())

    try:
        process_raw_file(raw_filename=str(raw_filepath), processed_filename=str(output_filepath), config_filename=str(config_file))
    except FileNotFoundError:
        return 'Something went wrong with saving the image'

    os.remove(str(raw_filepath))

    return render_template('image.html', image_filepath=str(output_filepath))


if __name__ == '__main__':
    app.run()
