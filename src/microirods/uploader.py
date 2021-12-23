from irods.session import iRODSSession
from irods.meta import (iRODSMeta, AVUOperation)
import glob
import os
import pandas as pd
import ntpath
from pathlib import Path


def __set_metadata(data_object, metadata_dic):
    for key, value in metadata_dic.items():
        data_object.metadata.add(key, str(value))


def __parse_metadata(metadata_file_path: str):
    data = pd.read_excel(metadata_file_path)
    # Remove all rows containing a NaN value in column Attribute (empty cell from excel sheet)
    data.dropna(subset=['Attribute'], inplace=True)
    # Set the column attribute as the index one
    data.set_index('Attribute', inplace=True)
    # create a dictionary where key is Attribute (the index) and value is Attribute values
    microscopy_dic = data.to_dict()['Attribute values']
    return microscopy_dic


def __upload_file_and_set_metadata(session,
                                   file_path: str,
                                   irods_destination: str,
                                   metadata_file_path: str = None) -> None:
    file_name = ntpath.basename(file_path)
    destination_path = irods_destination + '/' + file_name
    print('upload file:' + file_path + ' to :' + destination_path)
    session.data_objects.put(file_path, irods_destination, num_threads=1)
    data_object = session.data_objects.get(destination_path)
    if metadata_file_path:
        metadata_dic = __parse_metadata(metadata_file_path)
        __set_metadata(data_object, metadata_dic)


def upload_and_set_metadata(file_irods_environment: str,
                            file_path: str,
                            irods_destination: str,
                            file_extensions: str = None,
                            metadata_file_path: str = None) -> None:
    """
    :param file_irods_environment:
    :param file_path:
    :param irods_destination:
    :param file_extensions:
    :param metadata_file_path:
    :return:
    """
    with iRODSSession(irods_env_file=file_irods_environment) as session:
        # Check if the file exist
        if os.path.isfile(file_path):
            file_name = ntpath.basename(file_path)
            destination_path = irods_destination + '/' + file_name
            print('upload file:' + file_path + ' to :' + destination_path)
            session.data_objects.put(file_path, destination_path, num_threads=1)
            #            session.data_objects.metadata.remove_all()
            data_object = session.data_objects.get(destination_path)
            # 1-Remove all previous metadata
            data_object.metadata.remove_all()
            # 2-Add all metadata
            if metadata_file_path:
                metadata_dic = __parse_metadata(metadata_file_path)
                '''
                for key, value in metadata_dic.items():
                    print('key:' + key + ' / value: ' + str(value))
                    metadata = iRODSMeta(key, str(value), "")
                    data_object.metadata.add(metadata)
                '''
                # Create a list of AVUOperation then convert to tuple using tuple(list_name)
                avus = []
                metadata_dic = __parse_metadata(metadata_file_path)
                for key, value in metadata_dic.items():
                    avus.append(iRODSMeta(key, str(value), ""))
                data_object.metadata.apply_atomic_operations(
                    *[AVUOperation(operation="add", avu=avu_) for avu_ in avus])
                # AVUOperation(operation='add', avu = iRODSMeta(key, str(value), "")

            '''
            __upload_file_and_set_metadata(session,
                                           file_path,
                                           irods_destination,
                                           metadata_file_path)
            '''
        elif os.path.isdir(file_path):
            base_dir = Path(file_path)
            files = []
            extensions = file_extensions.split(',')
            for path in base_dir.glob(r'**/*'):
                #test_ext = path.suffix
                if path.suffix[1:] in extensions:
                    files.append(str(path))
            #files = glob.glob(file_path + '/*' + file_extension)
            files.sort()
            for file in files:
                file_name = ntpath.basename(file)
                destination_path = irods_destination + '/' + file_name
                print('upload file:' + file + ' to :' + destination_path)
                session.data_objects.put(file, destination_path, num_threads=1)
                data_object = session.data_objects.get(destination_path)
                # Add Metadata
                # See
                # https://github.com/irods/python-irodsclient/blob/master/irods/test/meta_test.py
                # https://github.com/irods/python-irodsclient/blob/master/irods/meta.py
                # 1-Remove all previous metadata
                data_object.metadata.remove_all()
                # 2- Add all metadata
                # TODO use obj.metadata.apply_atomic_operations
                if metadata_file_path:
                    metadata_dic = __parse_metadata(metadata_file_path)
                    # Create a list of AVUOperation then convert to tuple using tuple(list_name)
                    avus = []
                    metadata_dic = __parse_metadata(metadata_file_path)
                    for key, value in metadata_dic.items():
                        avus.append(iRODSMeta(key, str(value), ""))
                    data_object.metadata.apply_atomic_operations(
                        *[AVUOperation(operation="add", avu=avu_) for avu_ in avus])
                    '''
                    for key, value in metadata_dic.items():
                        print('key:' + key + ' / value: ' + str(value))
                        metadata = iRODSMeta(key, str(value), "")
                        data_object.metadata.add(metadata)
                    '''
                    # __set_metadata(data_object, metadata_dic)

                '''                
                __upload_file_and_set_metadata(session,
                                               file_full_path,
                                               irods_destination,
                                               metadata_file_path)
                '''
        else:
            return
