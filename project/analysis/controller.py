from flask import request
from flask_restful import Resource, marshal_with, abort

from project.analysis.model import Analysis
from project.analysis.service import ImageAnalysisService
from project.analysis.type import type_names


class AnalysisController(Resource):
    def __init__(self):
        self.analysis_service = ImageAnalysisService()

    @marshal_with(Analysis.json_fields)
    def post(self, image_id):
        analysis_type = get_analysis_type(request.get_json())

        analysis = self.analysis_service.analyse(image_id, analysis_type)

        return analysis


def get_analysis_type(json):
    type_name = json['type']

    try:
        type = type_names[type_name]
    except KeyError:
        abort(400)

    return type
