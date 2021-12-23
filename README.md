# microirods


## Installation

### Anaconda

Download anaconda and install it : https://www.anaconda.com/products/individual

create a new environment
conda create -n irods-env python=3.9

Activate the environment
conda activate irods-env

### Python iRODS Client (PRC)
pip install python-irodsclient


### Extra library to manipulate excel sheet
pip install numpy
pip install pandas
pip install xlrd


## Library usage

```
usage: microirods [-h] {info,upload,remove} ...

Manage microscopy images with IRODS

positional arguments:
  {info,upload,remove}
    info                Get info from a iRODS destination
    upload              Upload a file of files in a directory to an iRODS
                        destination
    remove              Remove a file in an iRODS destination

optional arguments:
  -h, --help            show this help message and exit

Process finished with exit code 0
```

### Upload images
```
usage: microirods upload [-h] --destination DESTINATION --source SOURCE
                         --irods_session IRODS_SESSION [--metadata METADATA]
                         [--file_extensions FILE_EXTENSIONS]

optional arguments:
  -h, --help            show this help message and exit
  --destination DESTINATION
                        iRODS destination
  --source SOURCE       source file/folder
  --irods_session IRODS_SESSION
                        The path to the iRODS environment JSON file
  --metadata METADATA   metadata file
  --file_extensions FILE_EXTENSIONS
                        File extensions to upload, e.g. nd2 or multiple one
                        separated by comma, e.g. tif,tiff,czi
```


#### Example:
```
upload --irods_session C:\Users\myuser\.irods\irods_environment.json --destination /irods/environment --source test_dataset\ --file_extension tif,czi --metadata test_dataset\metadata.xlsx
```
