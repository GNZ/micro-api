import os


class Config(object):
    DEBUG = True
    MOCK_CAMERA = False
    IMAGE_OUTPUT_DIR = os.path.abspath('images/output')
    IMAGE_INPUT_DIR = os.path.abspath('images/input')
    DB_DIR = os.path.abspath('db')
    DB_NAME = 'micro.db'
    DB_PATH = DB_DIR + '/' + DB_NAME
    IMAGE_BASE_URL = '/images/output'
    CAMERA_ENDPOINT = 'http://192.168.0.116:8080/?action=snapshot'


class Production(Config):
    DEVELOPMENT = False


class Development(Config):
    DEVELOPMENT = True
    MOCK_CAMERA = True
    CAMERA_MOCK_IMAGE_ID = 'blood_100x'
