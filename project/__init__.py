import os

from flask import Flask
from flask_restful import Api
# Modules
from project.image.controller import ImageController

# Initialize api
app = Flask(__name__)

# Load config
obj_name = 'project.config.' + os.getenv('MICRO_ENVIRONMENT')
app.config.from_object(obj_name)

api = Api(app)

api.add_resource(ImageController, '/images', '/images/<id>')

if __name__ == '__main__':
    # Run
    app.run(host='0.0.0.0')
