import os
from os import listdir
from os.path import isfile, join

class FileHandler():
    def __init__(self) -> None:
        self.specs = os.getcwd() + '/specs/'
        self.data = os.getcwd() + '/data/'
        self.specs_files = [f for f in self.__get_files_folder(self.specs) if self.__get_extension(f) == 'csv']
        self.data_files = [f for f in self.__get_files_folder(self.data) if self.__get_extension(f) == 'txt']
    
    @staticmethod
    def __get_files_folder(path: str) -> list:
        return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    @staticmethod
    def __get_extension(filename: str) -> str:
        return filename.rsplit('.', 1)[-1]

    @staticmethod
    def __get_name(filename: str) -> str:
        filename = filename.rsplit('/', 1)[1]
        if '_' in filename:
            return filename.rsplit('.', 1)[0].rsplit('_', 1)[0]
        else:
            return filename.rsplit('.', 1)[0]

    def spec_and_file(self) -> list:
        result = []
        for s in self.specs_files:
            for d in self.data_files:
                if self.__get_name(s) == self.__get_name(d):
                    result.append((s, d))
        return result