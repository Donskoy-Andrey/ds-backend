"""Plate reader realisation"""

import io
import torch
from torch import nn
from torchvision import transforms as T
from torchvision.models import resnet18
from PIL import Image, UnidentifiedImageError
from constants import DEVICE, N_LETTERS, MEAN, STD, INDEX_LETTER_MAP, IN_CHANNELS
from exceptions import ImageNotFoundError


class PlateReader(nn.Module):
    """Class that reads numbers from plates"""

    def __init__(self, ):
        super(PlateReader, self).__init__()
        self.resnet = nn.Sequential(*(list(resnet18().children())[:-2]))
        self.cnn = nn.Conv1d(
            in_channels=IN_CHANNELS, kernel_size=3, padding=1, out_channels=N_LETTERS
        )
        self.relu = nn.ReLU()

    @staticmethod
    def load_from_file(path: str) -> "PlateReader":
        """
        Load weights into the model

        :param path: path to the weights
        :return:
            Fitted model
        """
        model = PlateReader()
        model.to(DEVICE)
        model.load_state_dict(torch.load(path))

        model.eval()
        return model

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward step"""

        x = self.resnet(x)
        x = x.mean(axis=2)
        x = self.cnn(x)
        return x

    def read_text(self, image: io.BytesIO) -> str:
        """
        :param image: image in bytes
        :return:
            Text from image
        :raise InvalidImageException:
            If function has problems with image processing
        """

        transform = T.Compose([
            T.PILToTensor()
        ])

        try:
            image = Image.open(image)
        except UnidentifiedImageError:
            raise ImageNotFoundError

        image = transform(image)

        image = image.repeat(3, 1, 1)
        norm = T.Normalize(MEAN, STD)
        image = norm(image.float() / 255.)
        image = image.to(DEVICE)

        with torch.no_grad():
            val_predictions = self.forward(image.unsqueeze(0))
            y_predictions = torch.argmax(val_predictions, dim=1)
            res = ''.join([
                INDEX_LETTER_MAP[letter_id] for letter_id in y_predictions.cpu()[0].numpy()
            ])

        return res
