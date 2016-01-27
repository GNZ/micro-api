from project.image.repository import ImageRepository


class ImageService:
    def __init__(self):
        self.image_repository = ImageRepository()

    def create(self):
        return self.image_repository.create()

    def getAll(self):
        return self.image_repository.all()

    def get(self, id):
        return self.image_repository.read(id)

    def delete(self, id):
        return self.image_repository.delete(id)

    def update(self, image):
        return self.image_repository.update(image)
