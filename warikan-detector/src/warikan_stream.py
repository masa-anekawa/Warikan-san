from abc import ABC, abstractmethod
from botocore import response
from io import StringIO

class WarikanStream(ABC):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass


WarikanStream.register(StringIO)
WarikanStream.register(response.StreamingBody)
