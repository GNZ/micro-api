import cv2
from flask import current_app

from project.db.service import DatabaseService
from project.image.model import Image
from project.util.camera.camera_utils import CameraService
from project.util.image_utils import ImageUtils


class ImageRepository:
    def __init__(self):
        self.image_utils = ImageUtils()

    def save(self, image):
        DatabaseService().save_image(image)

        file_name = self.image_utils.getOutputFilename(image.id)
        cv2.imwrite(file_name, image.array)

        print 'Writing to ' + file_name
        return image

    def create(self):
        image = Image.create()

        if current_app.config.get('DEVELOPMENT'):
            # Read mock image
            id = current_app.config['CAMERA_MOCK_IMAGE_ID']
            image.array = cv2.imread(self.image_utils.getInputFilename(id))
        else:
            # Get image from mjpeg server
            image.array = CameraService().capture_image()

        # Save captured image
        self.save(image)

        return image

    def read(self, id):
        image = DatabaseService().get_image(id)

        return image

    def all(self):
        return DatabaseService().get_images()

    def delete(self, id):
        return DatabaseService().delete_image(id)

    def update(self, image):
        return DatabaseService().update_image(image)
