import os


class Config(object):
    DEBUG = True
    MOCK_CAMERA = False
    IMAGE_OUTPUT_DIR = os.path.abspath('images/output')
    IMAGE_OUTPUT_THUMB_DIR = os.path.abspath('images/output/thumb')
    IMAGE_INPUT_DIR = os.path.abspath('images/input')
    STATIC_FOLDER = os.path.abspath('images/output')
    STATIC_URL_PATH = '/images/output'
    DB_DIR = os.path.abspath('db')
    DB_NAME = 'micro.db'
    DB_PATH = DB_DIR + '/' + DB_NAME
    CAMERA_ENDPOINT = 'http://localhost:8080/?action=snapshot'


class Production(Config):
    DEVELOPMENT = False


class Development(Config):
    DEVELOPMENT = True
    MOCK_CAMERA = True
    CAMERA_MOCK_IMAGE_ID = 'blood_100x'
