from os import listdir as listDir
from shutil import rmtree as rmTree


def _decodeLine(line):
    line = line.replace("\"[", "[")
    line = line.replace("]\"", "]")
    line = line.encode('latin1', 'backslashreplace').decode('unicode-escape')
    line = line.replace("\"{", "{")
    line = line.replace("}\"", "}")
    return line


def formatFile(tempFolder, outputLocation):
    tmpFileList = listDir(tempFolder)
    if '_SUCCESS' in tmpFileList:
        with open(outputLocation, 'w') as output:
            for tmpFileName in tmpFileList:
                if tmpFileName.endswith(".json"):
                    tmpFileLocation = tempFolder+'/'+tmpFileName
                    with open(tmpFileLocation) as tmpFile:
                        for line in tmpFile:
                            line = line.strip()
                            if len(line) > 0:
                                output.write(_decodeLine(line))
                                output.write('\n')
        rmTree(tempFolder)
        return True
    else:
        return False
