import json
from pathlib import Path

class FileManager:
    MediaPath = Path(__file__).parent.parent.parent.joinpath("Media")
    @staticmethod
    def ReadJson(file):
        '''Reads a file as json with a path relative to App/Media'''
        if FileManager.MediaPath.joinpath(file).is_file():
            parsedJson = {}
            with open(FileManager.MediaPath.joinpath(file), "r") as f:
                parsedJson = json.load(f)
            return parsedJson
        else:
            raise FileNotFoundError(f"The file {file} does not exist")

    @staticmethod
    def WriteJson(file, obj):
        '''Writes an object as json to a file relative to App/Media'''
        try:
            with open(FileManager.MediaPath.joinpath(file), "w") as f:
                f.write(json.dumps(obj))
            return None
        except Exception as e:
            return e