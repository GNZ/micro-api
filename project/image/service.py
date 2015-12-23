from project.camera.service import CameraService
from project.image.model import Image
from project.image.repository import ImageRepository


class ImageService:
    def __init__(self):
        self.image_repository = ImageRepository()
        self.camera_service = CameraService()

    def create(self):
        image = Image()
        image.array = self.camera_service.capture_image()

        return self.image_repository.save(image)

    def get(self, id):
        return self.image_repository.read(id)

    def delete(self, id):
        return self.image_repository.delete(id)
