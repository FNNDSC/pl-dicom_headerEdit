#!/usr/bin/env python

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter, RawTextHelpFormatter
from importlib.metadata import Distribution

from chris_plugin import chris_plugin

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


import  os, sys
import  pudb
import  json

import  pfmisc
from    pfmisc._colors              import Colors
from    pfmisc                      import other

from    pfdicom_tagSub              import  pfdicom_tagSub
from    pfdicom_tagSub.__main__     import  package_CLIDS,              \
                                            package_argsSynopsisDS,     \
                                            package_tagProcessingHelp
from    pfdicom_tagSub.__main__     import  parserDS
from    pflog                       import pflog


DISPLAY_TITLE = r"""
       _           _ _                       _                    _           _____    _ _ _
      | |         | (_)                     | |                  | |         |  ___|  | (_) |
 _ __ | |______ __| |_  ___ ___  _ __ ___   | |__   ___  __ _  __| | ___ _ __| |__  __| |_| |_
| '_ \| |______/ _` | |/ __/ _ \| '_ ` _ \  | '_ \ / _ \/ _` |/ _` |/ _ \ '__|  __|/ _` | | __|
| |_) | |     | (_| | | (_| (_) | | | | | | | | | |  __/ (_| | (_| |  __/ |  | |__| (_| | | |_
| .__/|_|      \__,_|_|\___\___/|_| |_| |_| |_| |_|\___|\__,_|\__,_|\___|_|  \____/\__,_|_|\__|
| |                                     ______
|_|                                    |______|
"""

str_desc    = '''
                        DICOM header edit from batch

    Edit arbitrary DICOM header tags according using predefined templates.

                            -- version ''' + \
            Colors.YELLOW + __version__ + Colors.CYAN + ''' --

    This is a ChRIS DS plugin that will edit the header information for each
    DICOM file in its upstream parent and save a modified copy in the corre-
    sponding location in the output directory.

    For the most part, this plugin is used to _anonymize_ DICOMS but can be
    used in any context where a DICOM tag needs to be changed.

''' + Colors.NO_COLOUR

parserDS.add_argument(  '--pftelDB',
                    dest        = 'pftelDB',
                    default     = '',
                    type        = str,
                    help        = 'optional pftel server DB path')

def synopsis(ab_shortOnly = False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis =  '''
    NAME

        ''' + __name__ + '''

    SYNOPSIS

        ''' + __name__ + package_CLIDS

    description = '''

    DESCRIPTION

        This plugin is a thin wrapper about ``pl-dicom_tagSub`` and provides
        the ability for editing DICOM headers in ChRIS workflows. The most
        often use case is for DICOM anonymization.

    ARGS ''' + package_argsSynopsisDS + '''

    NOTE: ''' + package_tagProcessingHelp + '''

    EXAMPLES

    Perform a DICOM anonymization by processing specific tags:

        dicom_headerEdit                                                        \\
            /var/www/html/normsmall                                             \\
            /var/www/html/anon                                                  \\
            --fileFilter dcm                                                    \\
            --tagStruct '
            {
                "PatientName":              "%_name|patientID_PatientName",
                "PatientID":                "%_md5|7_PatientID",
                "AccessionNumber":          "%_md5|8_AccessionNumber",
                "PatientBirthDate":         "%_strmsk|******01_PatientBirthDate",
                "re:.*hysician":            "%_md5|4_#tag",
                "re:.*stitution":           "#tag",
                "re:.*ddress":              "#tag"
            }
            ' --threads 0 --printElapsedTime

        -- OR equivalently --

        dicom_headerEdit                                                        \\
            /var/www/html/normsmall                                             \\
            /var/www/html/anon                                                  \\
            --fileFilter dcm                                                    \\
            --splitToken ","                                                    \\
            --splitKeyValue "="                                                 \\
            --tagInfo '
                PatientName         =  %_name|patientID_PatientName,
                PatientID           =  %_md5|7_PatientID,
                AccessionNumber     =  %_md5|8_AccessionNumber,
                PatientBirthDate    =  %_strmsk|******01_PatientBirthDate,
                re:.*hysician       =  %_md5|4_#tag,
                re:.*stitution      =  #tag,
                re:.*ddress         =  #tag
            ' --threads 0 --printElapsedTime

        will replace the explicitly named tags as shown:

        * the ``PatientName`` value will be replaced with a Fake Name,
          seeded on the ``PatientID``;

        * the ``PatientID`` value will be replaced with the first 7 characters
          of an md5 hash of the ``PatientID``;

        * the ``AccessionNumber``  value will be replaced with the first 8
          characters of an md5 hash of the `AccessionNumber`;

        * the ``PatientBirthDate`` value will set the final two characters,
          i.e. the day of birth, to ``01`` and preserve the other birthdate
          values;

        * any tags with the substring ``hysician`` will have their values
          replaced with the first 4 characters of the corresponding tag value
          md5 hash;

        * any tags with ``stitution`` and ``ddress`` substrings in the tag
          contents will have the corresponding value simply set to the tag
          name.

        NOTE:

        Spelling matters! Especially with the substring bulk replace, please
        make sure that the substring has no typos, otherwise the target tags
        will most probably not be processed.

    '''

    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description

def earlyExit_check(args) -> int:
    """Perform some preliminary checks
    """
    if args.man or args.synopsis:
        print(str_desc)
        if args.man:
            str_help     = synopsis(False)
        else:
            str_help     = synopsis(True)
        print(str_help)
        return 1
    if args.b_version:
        print("Name:    %s\nVersion: %s" % (__name__, __version__))
        return 1
    return 0

# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parserDS,
    title='Edit DICOM header fields',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='2Gi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
@pflog.tel_logTime(
            event       = 'dicom_headerEdit',
            log         = 'Edit DICOM header fields'
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    """
    :param options: non-positional arguments parsed by the parser given to @chris_plugin
    :param inputdir: directory containing input files (read-only)
    :param outputdir: directory where to write output files
    """

    d_run                   : dict = {}

    if int(options.verbosity)   : print(DISPLAY_TITLE)
    if earlyExit_check(options) : return 1

    options.str_version     = __version__
    options.str_desc        = synopsis(True)

    pf_dicom_tagSub         = pfdicom_tagSub.pfdicom_tagSub(vars(options))
    d_run                   = pf_dicom_tagSub.run(timerStart = True)

    if options.printElapsedTime:
        pf_dicom_tagSub.dp.qprint(
            "Elapsed time = %f seconds" % d_run['runTime']
        )

    return 0


if __name__ == '__main__':
    main()
