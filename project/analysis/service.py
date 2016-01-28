from project.analysis.model import Analysis
from project.image.service import ImageService
from project.util.image_utils import ImageUtils


class ImageAnalysisService:
    image_utils = ImageUtils()
    image_service = ImageService()

    def analyse(self, image_id, analysis_type):
        # Load image
        image_object = self.image_service.get(image_id)

        # Try to get, otherwise create analysis
        analysis, created = Analysis.get_or_create(image=image_object.id, type=analysis_type.name)

        if not created:
            return analysis

        # Set result
        analysis.result = analysis_type().analyse(image=image_object)

        analysis.save()

        return analysis
