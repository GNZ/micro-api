from flask_restful import Resource, marshal_with

from project.analysis.model import Analysis
from project.analysis.service import ImageAnalysisService


class AnalysisController(Resource):
    def __init__(self):
        self.analysis_service = ImageAnalysisService()

    @marshal_with(Analysis.json_fields)
    def post(self, image_id):
        analysis = self.analysis_service.analyse(image_id)

        return analysis
