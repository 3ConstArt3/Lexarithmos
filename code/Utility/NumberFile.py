# -*- coding: utf-8 -*-
import json
import os

from itertools import permutations
from typing import Any, Dict, List, Tuple, Optional, Iterable

class NumberFile:

    """
    A class that is used to represent the
    dictionary, containing all the phrases
    that are stored from the user, along
    with their word number values.

    - All keys are stored as strings for stable .json serialization.
    - `Preview`, groups numbers by digit permutations ("anagrams").
    """

    def __init__(self, json_file_path: str = "Data/number_file.json") -> None:

        """
        Initializes the store and load of the existing data, if present.

        :param json_file_path: The path to the .json file used for persistence.
        """

        self.json_file_path = json_file_path
        os.makedirs(os.path.dirname(self.json_file_path), exist_ok=True)
        self.number_store: Dict[str, Dict[str, Any]] = self._load_from_file()

    def update(self, entry: Tuple[str, List[int]], insert: bool = True) -> None:

        """
        Inserts or deletes a phrase mapping.

        :param entry: A tuple of (phrase, numbers) where numbers[0] is the primary number and numbers[1] are its digit-sum divisions.
        :param insert: When True, insert/update the phrase; otherwise delete it.
        :raises ValueError: If numbers is empty or phrase is empty/whitespace or when deleting, if the phrase is absent under the key.
        :raises TypeError: If numbers contain non-integers.
        :raises KeyError: When deleting, if the key does not exist.
        :raises RuntimeError: If persisting, the disk fails.
        """

        phrase_text, number_series = entry
        self._validate_phrase(phrase_text)
        self._validate_numbers(number_series)

        primary_number = number_series[0]
        if insert: self._insert_phrase(phrase_text, number_series)
        else: self._delete_phrase(phrase_text, primary_number)

        self._cleanup_store()
        self._save_to_file()

    @staticmethod
    def _validate_phrase(phrase_text: str) -> None:
        
        """
        Validates that a phrase is a non-empty string.

        :raises ValueError: If the phrase is empty or whitespace.
        """
        if not isinstance(phrase_text, str) or not phrase_text.strip():
            raise ValueError("Phrase must be a non-empty string.")

    @staticmethod
    def _validate_numbers(number_series: Iterable[int]) -> None:
        
        """
        Validates the numbers' list. It ensures it is
        non-empty and contains only integers.

        :raises ValueError: If the number_series is empty.
        :raises TypeError: If any element of number_series is not an integer.
        """
        
        try: sequence = list(number_series)
        except TypeError as exc:
            raise TypeError("Numbers must be an iterable of integers.") from exc

        if not sequence: raise ValueError("Number list cannot be empty.")
        if any(not isinstance(n, int) for n in sequence):
            raise TypeError("All numbers must be integers.")

    def _insert_phrase(self, phrase_text: str, number_series: List[int]) -> None:
        
        """
        Inserts or updates a phrase for its primary number.

        :param phrase_text: The phrase to record.
        :param number_series: [primary_number, *divisions].
        """
        
        primary_number, divisions = number_series[0], number_series[1:]
        key_str = str(primary_number)

        if key_str not in self.number_store:
            self.number_store[key_str] = {"divisions": divisions, "phrases": [phrase_text]}
        else:
            
            existing_phrases = set(self.number_store[key_str]["phrases"])
            existing_phrases.add(phrase_text)
            self.number_store[key_str]["phrases"] = sorted(existing_phrases)

    def _delete_phrase(self, phrase_text: str, primary_number: int) -> None:
        
        """
        Deletes a phrase under the specified primary number.

        :param phrase_text: The phrase to remove.
        :param primary_number: The primary number key.
        :raises KeyError: If the key does not exist.
        :raises ValueError: If the phrase does not exist under the key.
        """
        
        key_str = str(primary_number)
        if key_str not in self.number_store:
            raise KeyError(f"Key {primary_number} does not exist.")

        try: 
            self.number_store[key_str]["phrases"].remove(phrase_text)
        except ValueError as exc:
            raise ValueError(f"Phrase '{phrase_text}' does "
                             f"not exist under key {primary_number}.") from exc

    def _cleanup_store(self) -> None:
        
        """
        Remove all empty entries and keep keys sorted numerically.
        """
        
        self.number_store = {k: v for k, v in self.number_store.items() if v["phrases"]}
        self.number_store = dict(sorted(self.number_store.items(), key=lambda item: int(item[0])))

    def _save_to_file(self, data: Optional[Dict[str, Any]] = None, path: Optional[str] = None) -> None:
        
        """
        Persists the provided data or current store to a .json file.

        :param data: The data to write. It defaults to the in-memory store.
        :param path: The target path. It defaults to the configured .json file path.
        :raises RuntimeError: If writing to the disk fails.
        """
        
        target_path = path or self.json_file_path
        payload: Dict[str, Any] = data or self.number_store
        
        try:
            
            with open(target_path, "w", encoding="utf-8") as fp:
                json.dump(payload, fp, ensure_ascii=False, indent=4)
        except OSError as exc:
            raise RuntimeError(f"Failed to write .json to '{target_path}': {exc}") from exc

    def _load_from_file(self) -> Dict[str, Dict[str, Any]]:
        
        """
        Loads the store from the disk, returning
        an empty mapping on error.
        """
        
        if not os.path.exists(self.json_file_path): return {}
        try:
            
            with open(self.json_file_path, "r", encoding="utf-8") as fp:
                return json.load(fp)
        except (OSError, json.JSONDecodeError): return {}

    @staticmethod
    def _permutations_of(number: int) -> List[int]:
        
        """
        Returns all unique digit permutations 
        of a number as integers.

        :param number: The input number.
        :return: The unique permutations interpreted as integers.
        """
        return list({int("".join(p)) for p in permutations(str(number))})
