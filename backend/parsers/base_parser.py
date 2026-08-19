from abc import ABC, abstractmethod

class LogParser(ABC):

    @abstractmethod
    def parse(self, line: str) -> dict:
        pass
    