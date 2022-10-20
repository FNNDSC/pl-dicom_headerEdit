# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.10.6-slim-bullseye

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="Edit DICOM header fields" \
      org.opencontainers.image.description="dicom_headerEdit is a ChRIS DS plugin that allows for batch editing of DICOM header fields."

WORKDIR /usr/local/src/pl-dicom_headerEdit

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]"

CMD ["dicom_headerEdit", "--help"]
