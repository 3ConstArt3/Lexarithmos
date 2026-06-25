# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Dict


class Analyzer(ABC):

    """
    Base interface for all research analyzers.
    """

    @property
    @abstractmethod
    def name(self) -> str:

        """
        Returns the analyzer's unique name.
        """

        pass

    @abstractmethod
    def analyze_and_save(self, number_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:

        """
        Runs the analyzer and saves its output.

        :param number_data: The stored number dictionary.
        :return: The generated analysis result.
        """

        pass
