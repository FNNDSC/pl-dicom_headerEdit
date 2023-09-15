# Edit DICOM header fields

[![Version](https://img.shields.io/docker/v/fnndsc/pl-dicom_headeredit?sort=semver)](https://hub.docker.com/r/fnndsc/pl-dicom_headerEdit)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-dicom_headerEdit)](https://github.com/FNNDSC/pl-dicom_headerEdit/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-dicom_headerEdit/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-dicom_headerEdit/actions/workflows/ci.yml)

`pl-dicom_headerEdit` is a [_ChRIS_](https://chrisproject.org/) _ds_ plugin which accepts as input a filesystem tree containing nested DICOM files, and edits each DICOM header consistently. Output DICOMs are saved in a concordant location in the output directory.

## Abstract

This page briefly describes a ChRIS plugin that is built around [`pfdicom_tagSub`](https://github.com/FNNDSC/pfdicom_tagSub) and exposes all of its functionality. Please refer to the referenced link for detailed information about the usage flags. The most common use case of this plugin is to anonymize DICOM files by editing their headers; however any potential use case that requires header changes is supported. Note that this is largely a rewrite of the [`pl-pfdicom_tagSub`](https://github.com/FNNDSC/pfdicom_tagSub) plugin using the [`chris_plugin_template`](https://github.com/FNNDSC/python-chrisapp-template) to allow for the new design pattern of "percolating" `arg_parsers` up from ancestor apps.

## Installation

`pl-dicom_headerEdit` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-dicom_headerEdit)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-dicom_headerEdit` as a container:

```shell
singularity exec docker://fnndsc/pl-dicom_headeredit dicom_headerEdit [--args values...] input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-dicom_headeredit dicom_headerEdit --help
```

Take care that the plugin image is all small letters (`pl-dicom_headeredit`), but the actual script name has some Camel case (`dicom_headerEdit`)!

## Examples

You can run `dicom_headerEdit` with a `--man` flag to get in-line help (including some examples):

```shell
singularity exec --cleanenv docker://fnndsc/pl-dicom_headeredit dicom_headerEdit --man in out   
```

Note that being a ChRIS DS plugin, `dicom_headerEdit` requires two positional arguments: a directory containing input data, and a directory where to create output data. The order of these positional arguments in largely irrelevant. We suggest positioning them either at the very front or very end of the CLI.

In this example, assume that you have a directory called `in` that contains DICOM data. This data can be nested into any arbitrary tree.

```shell
singularity exec --cleanenv docker://fnndsc/pl-dicom_headeredit dicom_headerEdit  \
            in out                                                                \
            --fileFilter dcm                                                      \
            --splitToken ","                                                      \
            --splitKeyValue "="                                                   \
            --tagInfo '
                PatientName         =  %_name|patientID_PatientName,
                PatientID           =  %_md5|7_PatientID,
                AccessionNumber     =  %_md5|8_AccessionNumber,
                PatientBirthDate    =  %_strmsk|******01_PatientBirthDate,
                re:.*hysician       =  %_md5|4_#tag,
                re:.*stitution      =  #tag,
                re:.*ddress         =  #tag
            ' --threads 0 --printElapsedTime

```

Here, the script will create for each directory in the input that contains files with `dcm` a corresponding directory in the output tree. In each output location, the corresponding input DICOM files will have headers edited as in the `--tagInfo`.

* the ``PatientName`` value will be replaced with a Fake Name, seeded on the ``PatientID``;

* the ``PatientID`` value will be replaced with the first 7 characters of an md5 hash of the ``PatientID``;

* the ``AccessionNumber``  value will be replaced with the first 8 characters of an md5 hash of the `AccessionNumber`

* the ``PatientBirthDate`` value will set the final two characters, i.e. the day of birth, to ``01`` and preserve the other birthdate values

* any tags with the substring ``hysician`` will have their values replaced with the first 4 characters of the corresponding tag value md5 hash

* any tags with ``stitution`` and ``ddress`` substrings in the tag contents will have the corresponding value simply set to the tag name.

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
