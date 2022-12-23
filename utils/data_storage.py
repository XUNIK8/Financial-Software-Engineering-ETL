from abc import ABC, abstractmethod


class DataStorage(ABC):
    """
    Abstract DataStorage class with abstract methods read and write.
    Inherited by concrete class FileDataStorage.
    Attribute: description; detailed description of an instance
    Member Function: read; read data according to provided config
    Member Function: write; write data according to provided config
    
    """
    def __init__(self, description):
        self._description = description

    
    @property
    def description(self):
        return self._description
    

    @description.setter
    def description(self, description):
        self._description = description


    @abstractmethod
    def read(self, config):
        pass


    @abstractmethod
    def write(self, config):
        pass
