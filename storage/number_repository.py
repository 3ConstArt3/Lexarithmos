# -*- coding: utf-8 -*-
from typing import Any, Dict, Iterable

from storage.json_repository import JsonRepository
from core.models import PhraseAnalysis
from config.paths import NUMBER_FILE_PATH

from core.exceptions import (
    InvalidPhraseError,
    PhraseNotFoundError
)


class NumberRepository:

    """
    Stores, updates and deletes phrase analysis
    records grouped by their primary number.
    """

    def __init__(self, file_path: str = NUMBER_FILE_PATH) -> None:

        """
        Initializes the number repository.

        :param file_path: The main number storage file path.
        """

        self.json_repository = JsonRepository(file_path)
        self.number_store: Dict[str, Any] = self.json_repository.load()

    def insert(self, analysis: PhraseAnalysis) -> None:

        """
        Inserts a phrase analysis record.

        :param analysis: The phrase analysis to store.
        """

        self._validate_analysis(analysis)

        key = str(analysis.total_value)
        sub_divisions = analysis.subdivisions[1:]

        if key not in self.number_store:

            self.number_store[key] = {
                "sub-divisions": sub_divisions,
                "key-phrases": [analysis.original_text]
            }

        else:

            phrases = set(self.number_store[key].get("key-phrases", []))
            phrases.add(analysis.original_text)
            self.number_store[key]["key-phrases"] = sorted(phrases)

        self._cleanup_store()
        self.json_repository.save(self.number_store)

    def delete(self, analysis: PhraseAnalysis) -> None:

        """
        Deletes a phrase analysis record.

        :param analysis: The phrase analysis to remove.
        """

        self._validate_analysis(analysis)

        key = str(analysis.total_value)

        if key not in self.number_store:
            raise PhraseNotFoundError(f"Key {key} does not exist.")

        try:

            self.number_store[key]["key-phrases"].remove(analysis.original_text)

        except InvalidPhraseError as exc:
            raise InvalidPhraseError(
                f"Phrase '{analysis.original_text}' does not exist under key {key}."
            ) from exc

        self._cleanup_store()
        self.json_repository.save(self.number_store)

    def get_all(self) -> Dict[str, Dict[str, Any]]:

        """
        Returns all stored number data.

        :return: The current number store.
        """

        return self.number_store

    @staticmethod
    def _validate_analysis(analysis: PhraseAnalysis) -> None:

        """
        Validates the phrase analysis object.
        """

        if not isinstance(analysis.original_text, str) or not analysis.original_text.strip():
            raise InvalidPhraseError("Phrase must be a non-empty string.")

        NumberRepository._validate_numbers(analysis.subdivisions)

    @staticmethod
    def _validate_numbers(numbers: Iterable[int]) -> None:

        """
        Validates that all subdivision values are integers.
        """

        sequence = list(numbers)

        if not sequence:
            raise InvalidPhraseError("Subdivision list cannot be empty.")

        if any(not isinstance(number, int) for number in sequence):
            raise TypeError("All subdivision values must be integers.")

    def _cleanup_store(self) -> None:

        """
        Removes empty entries and sorts keys numerically.
        """

        self.number_store = {
            key: value
            for key, value in self.number_store.items()
            if value.get("key-phrases")
        }

        self.number_store = dict(
            sorted(self.number_store.items(), key=lambda item: int(item[0]))
        )
