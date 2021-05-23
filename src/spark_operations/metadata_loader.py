from dotenv import load_dotenv
from json import load as json_load
from os import getenv


class _MetadataLoader:
    def __init__(self):
        load_dotenv()
        metadataFile = open(getenv('metadataFile'))
        self._metadata = json_load(metadataFile)
        metadataFile.close()

    def get_metadata(self):
        return self._metadata
