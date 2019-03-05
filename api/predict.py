from core.model import ModelWrapper

from maxfw.core import MAX_API, PredictAPI, MetadataAPI

from librosa.output import write_wav
from flask import make_response
from flask_restplus import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage

from config import MODEL_META_DATA, DEFAULT_MODEL, MODELS

# Set up parser for predict request (http://flask-restplus.readthedocs.io/en/stable/parsing.html)
input_parser = MAX_API.parser()
input_parser.add_argument('model',type=str, default=DEFAULT_MODEL, choices=MODELS)


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc(produces=['audio/wav'])
    @MAX_API.expect(input_parser)
    def get(self):
        """Make a prediction given input data"""
        args = input_parser.parse_args()
        model = args['model']
        preds = self.model_wrapper.predict(model)

        response = make_response(open('output.wav', 'rb').read())
        response.headers.set('Content-Type', 'audio/wav')
        response.headers.set('Content-Disposition', 'attachment', filename='result.wav')

        return response
