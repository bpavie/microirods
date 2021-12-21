from irods.session import iRODSSession

def get_file_list(file_irods_environment: str,
                  irods_destination: str) ->None:
    """

    :param file_name:
    :param metadata_file_name:
    :return:
    """
    with iRODSSession(irods_env_file=file_irods_environment) as session:
        coll = session.collections.get(irods_destination)

        # Listing all subcollections and printing their names:
        for subcoll in coll.subcollections:
            print("Collection: " + subcoll.name)

        # Listing all data objects and printing their names:
        for data_object in coll.data_objects:
            print("Data object: " + data_object.name)