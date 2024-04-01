"""ImageProvider realisation"""

from typing import Optional
import logging
import requests
from requests.exceptions import ConnectionError
from constants import IMAGE_SERVER_ADDRESS, TIMEOUT


logger = logging.getLogger(__name__)

class ImageProvider:
    """Class for load images"""

    def __init__(self, host: str = IMAGE_SERVER_ADDRESS):
        self.host = host

    def get_image(self, image_id: int) -> Optional[bytes]:
        """
        Get one image by its id

        :param image_id: image id
        :raise FileNotFoundError: file does not exist
        :return:
            image if exists else None
        """

        image_path = f'{self.host}/images/{image_id}'
        try:
            image = requests.get(image_path, timeout=TIMEOUT).content
        except ConnectionError:
            image = None

        return image


    def get_images(self, image_ids: list[int]) -> list[Optional[bytes]]:
        """
        Get images by their ids

        :param image_ids: list of image ids
        :return:
            list of images
        """
        images = []
        for image_id in image_ids:
            image = self.get_image(image_id)
            images.append(image)

        return images
