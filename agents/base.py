from abc import ABC , abstractmethod
from typing import Dict

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    """

    def __init__(self, name:str = "BaseAgent"):
        self.name = name

    @abstractmethod
    def run(self, input_dict:Dict) -> Dict:
        """
        Each agent implements this method.
        Takes input_dict, returns output_dict
        """
        pass