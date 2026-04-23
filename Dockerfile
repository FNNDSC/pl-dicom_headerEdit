# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.12.1-slim-bookworm

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="Edit DICOM header fields" \
      org.opencontainers.image.description="dicom_headerEdit is a ChRIS DS plugin that allows for batch editing of DICOM header fields."

WORKDIR /usr/local/src/pl-dicom_headerEdit

COPY requirements.txt .
RUN --mount=type=cache,sharing=private,target=/root/.cache/pip pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]" \
    && cd / && rm -rf ${SRCDIR}

CMD ["dicom_headerEdit"]
