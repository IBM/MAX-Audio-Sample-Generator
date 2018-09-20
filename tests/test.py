import pytest
import requests
import scipy.io.wavfile
import numpy


def test_response():

    model_endpoint = 'http://localhost:5000/model/predict'

    models = ["lofi-instrumentals", "up", "down", "left", "right", "stop", "go"]

    for model in models:
        print("Testing " + model)
        r = requests.get(url=model_endpoint + "?model=" + model)
        assert r.status_code == 200
        f = open("/tmp/max-testing-" + model + ".wav", 'wb')
        f.write(r.content)
        f.close()

        audio = scipy.io.wavfile.read("/tmp/max-testing-" + model + ".wav")

        assert audio[0] == 16000  # 16k sample rate

        audio_len = len(audio[1]) / audio[0]  # length in seconds = samples / sample rate
        assert 1.5 > audio_len > 0.5  # all the files are around 1 second

        assert numpy.max(audio[1]) > 0
        assert numpy.min(audio[1]) < 0

        audio_range = numpy.max(audio[1]) - numpy.min(audio[1])
        assert audio_range > 0.05  # this is a very small range, the model should be improved in the future


if __name__ == '__main__':
    pytest.main([__file__])
