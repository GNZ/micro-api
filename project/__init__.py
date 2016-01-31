import os

from flask import Flask
from flask_restful import Api

# Initialize api

app = Flask(__name__)

# Load config
obj_name = 'project.config.' + os.getenv('MICRO_ENVIRONMENT')
app.config.from_object(obj_name)

api = Api(app, catch_all_404s=True)

# Create folders
if os.path.exists(app.config.get('IMAGE_OUTPUT_DIR')):
    os.makedirs(app.config.get('IMAGE_OUTPUT_DIR'))

# Initialize db
if os.path.exists(app.config.get('DB_DIR')):
    os.makedirs(app.config.get('DB_DIR'))

from peewee import SqliteDatabase

micro_db = SqliteDatabase(app.config.get('DB_PATH'))

# Modules

from project.analysis.controller import AnalysisController
from project.image.controller import ImageController
from project.image.model import Image
from project.analysis.model import Analysis
from project.image_list.controller import ImageListController


# TODO: Move this away
@app.before_request
def _db_connect():
    micro_db.connect()
    micro_db.create_tables([Image, Analysis], safe=True)


@app.teardown_request
def _close_db(exception):
    if not micro_db.is_closed():
        micro_db.close()


# Add resource paths
api.add_resource(ImageController, '/images/<id>')
api.add_resource(ImageListController, '/images')
api.add_resource(AnalysisController, '/images/<image_id>/analyses')

if __name__ == '__main__':
    # Run
    app.run(host='0.0.0.0')
