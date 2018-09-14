from librosa.output import write_wav
from flask import make_response
from flask_restplus import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage

from config import MODEL_META_DATA, DEFAULT_MODEL, MODELS
from core.backend import ModelWrapper

api = Namespace('model', description='Model information and inference operations')

model_meta = api.model('ModelMetadata', {
    'id': fields.String(required=True, description='Model identifier'),
    'name': fields.String(required=True, description='Model name'),
    'description': fields.String(required=True, description='Model description'),
    'license': fields.String(required=False, description='Model license')
})


@api.route('/metadata')
class Model(Resource):
    @api.doc('get_metadata')
    @api.marshal_with(model_meta)
    def get(self):
        """Return the metadata associated with the model"""
        return MODEL_META_DATA

# Set up parser for predict request (http://flask-restplus.readthedocs.io/en/stable/parsing.html)
input_parser = api.parser()
input_parser.add_argument('model',type=str, default=DEFAULT_MODEL, choices=MODELS)


@api.route('/predict')
class Predict(Resource):

    model_wrapper = ModelWrapper()

    @api.doc(produces=['audio/wav'])
    @api.expect(input_parser)
    def get(self):
        """Make a prediction given input data"""
        args = input_parser.parse_args()
        model = args['model']
        preds = self.model_wrapper.predict(model)

        response = make_response(open('output.wav','rb').read())
        response.headers.set('Content-Type', 'audio/wav')
        response.headers.set('Content-Disposition', 'attachment', filename='result.wav')

        return response
