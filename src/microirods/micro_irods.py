# microirods.py
# 2021, Benjamin Pavie

r"""Upload, delete and get info on dataset on iRODS storage

(1) info --irods_session C:/Users/u0094799/.irods/irods_environment.json --destination /gbiomed_fbi/home/gbiomed_fbi_pilot002

(2) upload --irods_session C:/Users/u0094799/.irods/irods_environment.json --destination /gbiomed_fbi/home/gbiomed_fbi_pilot002 --source G:/Projects/IRODS/code/data --source G:/Projects/IRODS/code/data --file_extension nd2 --metadata G:/Projects/IRODS/code/data/metadata.xlsx


#Using the iRODS python client : https://github.com/irods/python-irodsclient
"""
import os
import argparse
import time
import sys
from microirods.get_info import get_file_list
from uploader import upload_and_set_metadata


def upload(args):
    print('upload:')
    upload_and_set_metadata(args.irods_session,
                            args.source,
                            args.destination,
                            args.file_extensions,
                            args.metadata)


def info(args):
    print('info:')
    print('Location: ' + args.destination)
    get_file_list(args.irods_session, args.destination)


def remove(args):
    print('TODO remove')


def _parse_args():
    # See https://towardsdatascience.com/a-simple-guide-to-command-line-arguments-with-argparse-6824c30ab1c3
    #     https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        prog='microirods',
        description="Manage microscopy images with IRODS")
    # parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
    # Set 3 main subcommands info/upload/remove
    subparser = parser.add_subparsers(dest='command')
    parser_info = subparser.add_parser('info', help='Get info from a iRODS destination')
    parser_info.set_defaults(func=info)
    parser_upload = subparser.add_parser('upload', help='Upload a file of files in a directory to an iRODS destination')
    parser_upload.set_defaults(func=upload)
    parser_remove = subparser.add_parser('remove', help='Remove a file in an iRODS destination')
    parser_remove.set_defaults(func=remove)

    # Upload file
    parser_upload.add_argument(
        '--destination',
        type=str,
        default=None,
        required=True,
        help="iRODS destination")
    parser_upload.add_argument(
        '--source',
        type=str,
        default=None,
        required=True,
        help="source file/folder")
    parser_upload.add_argument(
        '--irods_session',
        type=str,
        default=os.path.expanduser('~') + '/.irods/irods_environment.json',
        required=True,
        help="The path to the iRODS environment JSON file")
    parser_upload.add_argument(
        '--metadata',
        type=str,
        default=None,
        required=False,
        help="metadata file")
    parser_upload.add_argument(
        '--file_extensions',
        type=str,
        default=None,
        required=False,
        help="File extensions to upload, e.g. nd2 or multiple one separated by comma, e.g. tif,tiff,czi")

    # Get Info
    parser_info.add_argument(
        '--destination',
        type=str,
        default=None,
        required=True,
        help="iRODS destination")
    parser_info.add_argument(
        '--irods_session',
        type=str,
        default=os.path.expanduser('~') + '/.irods/irods_environment.json',
        required=True,
        help="The path to the iRODS environment JSON file")

    # Remove file
    parser_remove.add_argument(
        '--destination',
        type=str,
        default=None,
        required=True,
        help="iRODS destination")
    parser_remove.add_argument(
        '--irods_session',
        type=str,
        default=os.path.expanduser('~') + '/.irods/irods_environment.json',
        required=True,
        help="The path to the iRODS environment JSON file")

    # version=f'{__version__}')

    return parser.parse_args()


'''
    parser.add_argument(
        '--irods_session',
        type=str,
        default=os.path.expanduser('~')+'/.irods/irods_environment.json',
        help="The path to the IRODS environment JSON file")

    parser.add_argument(
        '--destination',
        type=str,
        default=None,
        help="IRODS destination")

    parser.add_argument(
        '--source',
        type=str,
        default=None,
        help="source file/folder")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--info',
                       action='store_true')
    group.add_argument('--upload', action='store_true')
    group.add_argument('--remove', action='store_true')
'''

'''
    parser.add_argument(
        '--compression',
        type=str,
        default=None,
        help="the algorithm used for compressing the image data; currently "
             "'zlib' is the only supported compression algorithm "
             "(default: no compression)")

    parser.add_argument(
        '--pyramid-levels',
        type=int,
        default=6,
        help='the maximum number of resolution levels in the pyramidal '
             'OME TIFF, including the full resolution image; successive '
             'pyramid levels are downsampled by a factor 2 '
             '(default: %(default)d)')

    parser.add_argument(
        '--tile-size',
        type=int,
        default=256,
        help='width in pixels of the tiles in the pyramidal OME TIFF; '
             'the tiles are square; tile size must be a multiple of 16 '
             '(default: %(default)d)')

    parser.add_argument(
        'nd2_filename',
        type=str,
        help="full filename of the input ND2 file")

    parser.add_argument(
        'pyramid_filename',
        type=str,
        nargs='?',
        help="full filename of the resulting pyramidal OME TIFF file; "
             "if no pyramid filename is provided the pyramidal OME TIFF will "
             "be written to the same directory as the original ND2 and with "
             "the same filename but with an .ome.tif extension")
'''

'''
def _get_pyramid_filename(nd2_filename: str,
                          pyramid_filename: Optional[str]) -> str:
    if pyramid_filename is not None:
        return pyramid_filename
    else:
        # If we have no pyramid filename, then we use the same directory
        # and the same filename of the ND2 file, but with .ome.tiff
        # as extension instead of .nd2.
        dirname = os.path.dirname(nd2_filename)
        filename = os.path.basename(Path(nd2_filename).with_suffix('.ome.tif'))
        return os.path.join(dirname, filename)
'''


def main():
    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    options = _parse_args()

    t1 = time.time()
    options.func(options)
    t2 = time.time()
    print(f'Processed in {t2 - t1:.1f} seconds.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
