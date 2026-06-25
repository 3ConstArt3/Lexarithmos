# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from analysis.pipeline.analyzer import Analyzer


class AnalysisPipeline:

    """
    Runs registered research analyzers.
    """

    def __init__(self) -> None:

        """
        Initializes an empty analyzer pipeline.
        """

        self.analyzers: List[Analyzer] = []

    def register(self, analyzer: Analyzer) -> None:

        """
        Registers a new analyzer.

        :param analyzer: The analyzer to register.
        """

        self.analyzers.append(analyzer)

    def run_all(self, number_data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:

        """
        Runs all registered analyzers.

        :param number_data: The stored number dictionary.
        :return: A dictionary with analyzer names and their results.
        """

        results: Dict[str, Dict[str, Any]] = {}

        for analyzer in self.analyzers:

            results[analyzer.name] = analyzer.analyze_and_save(number_data)

        return results
