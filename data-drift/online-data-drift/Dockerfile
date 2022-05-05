FROM python:3.9-slim

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY model/requirements.txt .
RUN python3 -m pip install -r \
    requirements.txt --no-cache-dir \
    && rm -f requirements.txt

ADD . /workspace
WORKDIR /workspace

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]

