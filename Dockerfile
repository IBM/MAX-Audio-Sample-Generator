FROM codait/max-base:v1.1.3

# Fill in these with a link to the bucket containing the model and the model file name
ARG model_bucket=https://max-assets.s3.us.cloud-object-storage.appdomain.cloud/max-audio-sample-generator
ARG model_files=models.tar.gz

WORKDIR /workspace

# Get model archive and unzip it to assets folder
RUN wget -nv ${model_bucket}/${model_files} --output-document=assets/${model_files} --show-progress --progress=bar:force:noscroll && \
  tar -x -C assets/ -f assets/${model_files} -v && rm assets/${model_files}

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace

# check file integrity
RUN md5sum -c md5sums.txt

EXPOSE 5000

CMD python app.py
