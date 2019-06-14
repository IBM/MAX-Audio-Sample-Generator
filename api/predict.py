#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from core.model import ModelWrapper
from maxfw.core import MAX_API, CustomMAXAPI
from flask import make_response
from config import DEFAULT_MODEL, MODELS

# Set up parser for predict request (http://flask-restplus.readthedocs.io/en/stable/parsing.html)
input_parser = MAX_API.parser()
input_parser.add_argument('model', type=str, default=DEFAULT_MODEL, choices=MODELS)


class ModelPredictAPI(CustomMAXAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc(produces=['audio/wav'])
    @MAX_API.expect(input_parser)
    def get(self):
        """Generate audio file"""
        args = input_parser.parse_args()
        model = args['model']
        _ = self.model_wrapper.predict(model)

        response = make_response(open('output.wav', 'rb').read())
        response.headers.set('Content-Type', 'audio/wav')
        response.headers.set('Content-Disposition', 'attachment', filename='result.wav')

        return response
