from abc import ABC, abstractmethod


class CeneoDataObject(ABC):
    @abstractmethod
    def as_string(self):
        ...

    @abstractmethod
    def as_dict(self):
        ...
