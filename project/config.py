import os


class Config(object):
    DEBUG = True
    MOCK_CAMERA = False
    IMAGE_OUTPUT_DIR = os.path.abspath('images/output')
    IMAGE_INPUT_DIR = os.path.abspath('images/input')
    IMAGE_BASE_URL = '/images/output'
    CAMERA_ENDPOINT = 'http://192.168.0.116:8080/?action=snapshot'


class Production(Config):
    DEVELOPMENT = False
    empty = True


class Development(Config):
    DEVELOPMENT = True
    MOCK_CAMERA = True
    CAMERA_MOCK_IMAGE_ID = 'blood23'
