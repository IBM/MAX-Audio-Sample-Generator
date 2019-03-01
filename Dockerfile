FROM codait/max-base:v1.1.0

# Fill in these with a link to the bucket containing the model and the model file name
ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/max-audio-sample-generator
ARG model_files=models.tar.gz

# Get model archive and unzip it to assets folder
RUN wget -nv ${model_bucket}/${model_files} --output-document=/workspace/assets/${model_files} --show-progress --progress=bar:force:noscroll
RUN tar -x -C assets/ -f assets/${model_files} -v && rm assets/${model_files}

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace
RUN md5sum -c md5sums.txt  # check file integrity

EXPOSE 5000

CMD python app.py
