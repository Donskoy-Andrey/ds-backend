from flask import Flask, request
from plate_reader import PlateReader, ImageNotFoundError
from image_provider import ImageProvider
import io
import logging
from constants import (
    MODEL_WEIGHTS, LOGGER_LEVEL, LOGGER_FORMAT,
    BASIC_PORT, BASIC_HOST,
)


app = Flask(__name__)
logger = logging.getLogger(__name__)
plate_reader = PlateReader.load_from_file(MODEL_WEIGHTS)
image_provider = ImageProvider()


def process_image(image_id: str):
    """
    Process image and read plate number on it

    :param image_id: image number
    :return:
        Text on image
    """
    if image_id is None or not image_id.isdigit():
        logger.error("Invalid image_id")
        return {"plate_number": "invalid image_id", "status_code": 422}

    image = image_provider.get_image(image_id=int(image_id))
    if image is None:
        logger.error("Problems with connection")
        return {"plate_number": "connection error with external server", "status_code": 502}

    image = io.BytesIO(image)

    try:
        plate_number = plate_reader.read_text(image)
    except ImageNotFoundError:
        logger.error("Image not found")
        return {"plate_number": "image not found", "status_code": 400}

    return {"plate_number": plate_number, "status_code": 200}

@app.route('/read_plate_number', methods=['POST'])
def read_plate_number():
    image_id = request.form.get("image_id")
    return process_image(image_id)


@app.route('/read_plate_numbers', methods=['POST'])
def read_plate_numbers():
    """
    Read a few images

    :template: image_ids=9965,10022
    """
    image_ids = request.form.get("image_ids")
    image_ids = image_ids.split(',')

    result = {}
    for image_id in image_ids:
        output = process_image(image_id)
        result[image_id] = output

    return result


@app.route('/')
def home_page():
    return "info: plate number server app"


if __name__ == '__main__':
    logging.basicConfig(format=LOGGER_FORMAT, level=LOGGER_LEVEL)
    app.config['JSON_AS_ASCII'] = False
    app.run(host=BASIC_HOST, port=BASIC_PORT, debug=True)
