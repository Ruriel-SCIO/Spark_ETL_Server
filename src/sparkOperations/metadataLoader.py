from json import load as jsonLoad
from os import getenv

#Reads the metadata specified in the config folder.
class _MetadataLoader:
    def __init__(self):
        metadataFile = open(getenv("METADATA_FILE"))
        self._metadata = jsonLoad(metadataFile)
        metadataFile.close()

    def getMetadata(self):
        return self._metadata
