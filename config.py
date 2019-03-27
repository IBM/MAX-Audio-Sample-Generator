# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False

# Application settings

# API metadata
API_TITLE = 'MAX Audio Sample Generator'
API_DESC = 'Generate short audio clips of speech commands and lo-fi instrumental samples'
API_VERSION = '1.1.0'

# default model
MODEL_NAME = 'wavegan'
DEFAULT_MODEL_PATH = 'assets/models'
MODEL_LICENSE = 'Apache2'

# generator model options and default
DEFAULT_MODEL = 'lofi-instrumentals'
MODELS = ['lofi-instrumentals', 'up', 'down', 'left', 'right', 'stop', 'go']
INPUT_TENSOR = 'z:0'
OUTPUT_TENSOR = 'G_z:0'

MODEL_META_DATA = {
    'id': '{}'.format(MODEL_NAME.lower()),
    'name': 'WaveGAN audio generation model',
    'description': 'Generative Adversarial Network, trained using TensorFlow on spoken commands and lo-fi instrumental music',
    'type': 'Audio Modeling',
    'license': '{}'.format(MODEL_LICENSE),
    'source': 'https://developer.ibm.com/exchanges/models/all/max-audio-sample-generator/'
}
