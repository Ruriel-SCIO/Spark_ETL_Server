from .metadata import _MetadataLoader
from io_operations import compression
from os.path import basename
from os import makedirs
from uuid import uuid4
from tempfile import gettempdir
from shutil import copyfile
class ETL:
    def __init__(self):
        self.metadata = _MetadataLoader().get_metadata()

    #Reads the file to be processed. If it's compressed, uncompress in the temp folder and return it's location.
    #Otherwise, simply copies it to the temp folder.
    def pre_processing(self, fileLocation):
        metadata = self.metadata
        outputFolder = '{}/{}/{}'.format(gettempdir(), 'spark_etl_server', uuid4())
        outputFilename = basename(fileLocation)
        makedirs(outputFolder, exist_ok=True)
        if 'compression' in metadata:
            length = len(outputFilename)
            outputFileLocation = '{}/{}'.format(outputFolder, outputFilename[:length-3])
            compression.decompress(fileLocation, outputFileLocation)
        else:
            outputFileLocation = '{}/{}'.format(outputFolder, outputFilename)
            copyfile(fileLocation, outputFileLocation)
        return outputFileLocation