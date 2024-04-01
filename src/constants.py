import logging
import numpy as np
import torch


# General
N_LETTERS = 22
INDEX_LETTER_MAP = {
    0: '9', 1: 'н', 2: 'а', 3: 'к', 4: 'м', 5: '5',
    6: 'е', 7: '3', 8: 'т', 9: 'х', 10: 'о', 11: '8',
    12: '0', 13: 'у', 14: '4', 15: 'р', 16: '7', 17: '2',
    18: '1', 19: 'с', 20: 'в', 21: '6',
}
LOGGER_LEVEL = logging.INFO
LOGGER_FORMAT = '[%(levelname)s] [%(asctime)s] %(message)s'
TIMEOUT = 1


# Servers
BASIC_PORT = 8080
BASIC_HOST = '0.0.0.0'
BASIC_ADDRESS = f'http://{BASIC_HOST}:{BASIC_PORT}'

# IMAGE_SERVER_HOST = '178.154.220.122'
IMAGE_SERVER_HOST = 'external_image_server'
IMAGE_SERVER_PORT = 7777
IMAGE_SERVER_ADDRESS = f'http://{IMAGE_SERVER_HOST}:{IMAGE_SERVER_PORT}'

# Model
DEVICE = torch.device('cpu')
MODEL_WEIGHTS = '/app/model_weights/plate_reader_model.pth'
IN_CHANNELS = 512
MEAN = np.array([0.485, 0.456, 0.406])
STD = np.array([0.229, 0.224, 0.225])
