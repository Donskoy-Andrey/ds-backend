"""My external server realisation"""

from flask import Flask, send_file, Response
import io
import logging
from constants import IMAGE_SERVER_HOST, IMAGE_SERVER_PORT


logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/images/<int:image_id>', methods=['GET'])
def load_images(image_id: int):
    try:
        image_file = open(f'/app/images/{image_id}.jpg', 'rb')
        image = image_file.read()
        image_file.close()
    except FileNotFoundError:
        logger.error(f'Image not found! image_id = {image_id}')
        return Response(status=404)

    return send_file(
        io.BytesIO(image),
        mimetype='image/jpg'
    )

@app.route('/')
def home_page():
    return "info: image server app"


if __name__ == '__main__':
    app.run(host=IMAGE_SERVER_HOST, port=IMAGE_SERVER_PORT, debug=True)
