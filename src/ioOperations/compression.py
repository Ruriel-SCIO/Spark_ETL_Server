import gzip
import shutil
#Compress the file from inputLocation and saves it on outputLocation
def compress(inputLocation, outputLocation):
    with open(inputLocation, 'rb') as input:
        with gzip.open(outputLocation, 'wb') as output:
            shutil.copyfileobj(input, output)
            
#Decompress the file from inputLocation and save it on outputLocation
def decompress(inputLocation, outputLocation):
    with gzip.open(inputLocation, 'rb') as compressedFile:
        with open(outputLocation, 'wb') as output:
            shutil.copyfileobj(compressedFile, output)