from flask import current_app


class ImageUtils:
    def getOutputFilename(self, id):
        return self.buildJpegFilename(current_app.config.get('IMAGE_OUTPUT_DIR'), id)

    def getInputFilename(self, id):
        return self.buildJpegFilename(current_app.config.get('IMAGE_INPUT_DIR'), id)

    def buildJpegFilename(self, folder, id):
        return folder + '/' + str(id) + '.jpg'
