# Edit DICOM header fields

[![Version](https://img.shields.io/docker/v/fnndsc/pl-dicom_headerEdit?sort=semver)](https://hub.docker.com/r/fnndsc/pl-dicom_headerEdit)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-dicom_headerEdit)](https://github.com/FNNDSC/pl-dicom_headerEdit/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-dicom_headerEdit/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-dicom_headerEdit/actions/workflows/ci.yml)

`pl-dicom_headerEdit` is a [_ChRIS_](https://chrisproject.org/) _ds_ plugin which accepts as input a filesystem tree containing nested DICOM files, and edits each DICOM header consistently. Output DICOMs are saved in a concordant location in the output directory.

## Abstract

This page briefly describes a ChRIS plugin that is built around [pfdicom_tagSub](https://github.com/FNNDSC/pfdicom_tagSub) and exposes all of its functionality. Please refer to the referenced link for detailed information about the usage flags. The most common use case of this plugin is to anonymize DICOM files by editing their headers; however any potential use case that requires header changes is supported.

## Installation

`pl-dicom_headerEdit` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-dicom_headerEdit)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-dicom_headerEdit` as a container:

```shell
singularity exec docker://fnndsc/pl-dicom_headerEdit dicom_headerEdit [--args values...] input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-dicom_headerEdit dicom_headerEdit --help
```

## Examples

`dicom_headerEdit` requires two positional arguments: a directory containing input data, and a directory where to create output data. First, create the input directory and move input data into it.

```shell
mkdir incoming/ outgoing/
mv some.dat other.dat incoming/
singularity exec docker://fnndsc/pl-dicom_headerEdit:latest dicom_headerEdit [--args] incoming/ outgoing/
```

## Development

Instructions for developers.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl-dicom_headerEdit .
```

### Running

Mount the source code `dicom_headerEdit.py` into a container to try out changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/dicom_headerEdit.py:/usr/local/lib/python3.10/site-packages/dicom_headerEdit.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-dicom_headerEdit dicom_headerEdit /incoming /outgoing
```

### Testing

Run unit tests using `pytest`.
It's recommended to rebuild the image to ensure that sources are up-to-date.
Use the option `--build-arg extras_require=dev` to install extra dependencies for testing.

```shell
docker build -t localhost/fnndsc/pl-dicom_headerEdit:dev --build-arg extras_require=dev .
docker run --rm -it localhost/fnndsc/pl-dicom_headerEdit:dev pytest
```

## Release

Steps for release can be automated by [Github Actions](.github/workflows/ci.yml).
This section is about how to do those steps manually.

### Increase Version Number

Increase the version number in `setup.py` and commit this file.

### Push Container Image

Build and push an image tagged by the version. For example, for version `1.2.3`:

```
docker build -t docker.io/fnndsc/pl-dicom_headerEdit:1.2.3 .
docker push docker.io/fnndsc/pl-dicom_headerEdit:1.2.3
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to a _ChRIS Store_.

```shell
docker run --rm localhost/fnndsc/pl-dicom_headerEdit:dev chris_plugin_info > chris_plugin_info.json
```

_-30-_