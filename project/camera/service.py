from flask import current_app

from project.image.repository import ImageRepository
from project.image.model import Image

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except:
    "Pi Camera not available"


class CameraService:
    def __init__(self):
        self.image_repository = ImageRepository()

    def capture_image(self):
        if current_app.config.get('DEVELOPMENT'):
            raw_image = self.image_repository.read(current_app.config['CAMERA_MOCK_IMAGE_ID'])
        else:
            with PiCamera() as camera:
                raw_image = PiRGBArray(camera)
                camera.capture(raw_image, format='bgr', use_video_port=True)

        return raw_image.array
