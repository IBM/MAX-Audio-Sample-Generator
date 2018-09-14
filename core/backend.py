import tensorflow as tf
import numpy as np
import logging
from config import DEFAULT_MODEL_PATH, MODELS, INPUT_TENSOR, OUTPUT_TENSOR
from librosa.output import write_wav

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class SingleModelWrapper(object):

    def __init__(self, model, path):
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.sess = tf.Session(graph = self.graph)
            saver = tf.train.import_meta_graph('{}/train_{}/infer/infer.meta'.format(path, model))
            saver.restore(self.sess, tf.train.latest_checkpoint('{}/train_{}/'.format(path, model)))
            self.input = self.graph.get_tensor_by_name(INPUT_TENSOR)
            self.output  = self.graph.get_tensor_by_name(OUTPUT_TENSOR)

    def predict(self):
        # Create 50 random latent vectors z
        _z = (np.random.rand(50, 100) * 2.) - 1
        # Synthesize G(input)
        preds = self.sess.run(self.output, {self.input: _z})
        return preds


class ModelWrapper(object):
    """Model wrapper for TensorFlow models in SavedModel format"""
    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading models from: {}...'.format(path))
        self.models = {}
        for model in MODELS:
            logger.info('Loading model: {}'.format(model))
            self.models[model] = SingleModelWrapper(model=model, path=path)

        logger.info('Loaded all models')

    def predict(self, model):
        logger.info('Generating audio from model: {}'.format(model))
        preds = self.models[model].predict()
        write_wav('output.wav', preds[0], 16000)
        wav_bytes = open('output.wav')
        return wav_bytes
