# -*- coding: utf-8 -*-
from itertools import permutations
from typing import Any, Dict, List, Set

from analysis.pipeline.analyzer import Analyzer
from storage.json_repository import JsonRepository
from config.paths import PERMUTATIONS_FILE_PATH


class PermutationAnalyzer(Analyzer):

    """
    Builds a JSON index that groups stored
    numbers with their digit permutations.
    """

    @property
    def name(self) -> str:

        """
        Returns the analyzer's unique name.
        """

        return "permutation_analyzer"

    def __init__(self, output_path: str = PERMUTATIONS_FILE_PATH) -> None:

        self.output_repository = JsonRepository(output_path)

    def analyze(self, number_data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:

        preview_data: Dict[str, Dict[str, Any]] = {}
        processed_keys: Set[str] = set()

        for key, record in self._sort_number_data(number_data).items():

            if key in processed_keys:
                continue

            base_number = int(key)
            subdivisions = record.get("sub-divisions", [])

            permutation_map = self._find_existing_permutations(
                base_number=base_number,
                number_data=number_data,
                processed_keys=processed_keys
            )

            preview_data[key] = {
                "sub-divisions": subdivisions,
                "permutations": permutation_map
            }

        return preview_data

    def analyze_and_save(self, number_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:

        permutation_index = self.analyze(number_data)
        self.output_repository.save(permutation_index)

        return permutation_index

    def _find_existing_permutations(
        self,
        base_number: int,
        number_data: Dict[str, Dict[str, Any]],
        processed_keys: Set[str]
    ) -> Dict[str, List[str]]:

        permutation_map: Dict[str, List[str]] = {}

        for permutation_number in self._generate_unique_permutations(base_number):

            permutation_key = str(permutation_number)

            if permutation_key not in number_data:
                continue

            phrases = number_data[permutation_key].get("key-phrases", [])
            permutation_map[permutation_key] = phrases
            processed_keys.add(permutation_key)

        return dict(
            sorted(permutation_map.items(), key=lambda item: int(item[0]))
        )

    @staticmethod
    def _generate_unique_permutations(number: int) -> List[int]:

        unique_permutations = {
            int("".join(digits))
            for digits in permutations(str(number))
            if digits[0] != "0"
        }

        return sorted(unique_permutations)

    @staticmethod
    def _sort_number_data(
        number_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:

        return dict(
            sorted(number_data.items(), key=lambda item: int(item[0]))
        )
