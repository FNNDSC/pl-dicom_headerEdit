from setuptools import setup

setup(
    name='dicom_headerEdit',
    version='1.1.0',
    description='"dicom_headerEdit" is a ChRIS DS plugin that allows for batch editing of DICOM header fields.',
    author='FNNDSC',
    author_email='dev@babyMRI.org',
    url='https://github.com/FNNDSC/pl-dicom_headerEdit',
    py_modules=['dicom_headerEdit'],
    install_requires=['chris_plugin'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'dicom_headerEdit = dicom_headerEdit:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1',
            'pytest-mock~=3.8'
        ]
    }
)
