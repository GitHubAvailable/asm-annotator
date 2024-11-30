"""
model.py - The abstract LLM class.
"""

import abc
from typing import Any, Container


class LLM(abc.ABC):
    """An abstract class that represents a general LLM."""
    @abc.abstractmethod
    def __call__(self, messages: Container) -> Any:
        pass
    
    def generate(self, messages: Container) -> Any:
        """
        Generate response to given messages container and return the response.

        Parameter
        ---------
        messages: Container, the session the model should respond to.
        """
        self.__call__(messages)