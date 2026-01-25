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
    """

    def __init__(self, json_file_path: str = "Data/number_file.json") -> None:

        """
        Initializes the dictionary storage files and
        loads the necessary data if they are present.

        :param json_file_path: The main .json usage file path.
        """

        self.json_file_path = json_file_path
        os.makedirs(os.path.dirname(self.json_file_path), exist_ok=True)
        self.number_store = self._load_from_file()

    def update(self, entry: Tuple[str, List[int]], insert: bool = True) -> None:

        """
        Inserts | updates or deletes a phrase mapping.

        :param entry: A tuple of (phrase, numbers) where numbers[0] is the primary number and numbers[1] are its digit-sum divisions.
        :param insert: When its value is True, then insert | update the phrase. Otherwise, delete it.
        :raises ValueError: If the number list is empty or the phrase is empty/whitespace or upon deletion, if the phrase is absent.
        :raises TypeError: If the numbers contain non-integer values.
        :raises KeyError: If the key does not exist, upon deletion.
        :raises RuntimeError: If persisting, the disk fails.
        """

        phrase_text, number_series = entry
        self._validate_phrase(phrase_text)
        self._validate_numbers(number_series)

        primary_number = number_series[0]
        if insert:
            self._insert_phrase(phrase_text, number_series)
        else:
            self._delete_phrase(phrase_text, primary_number)

        self._cleanup_store()
        self._save_to_file()

    def generate_permutations_file(self, permutation_file_path: str = "Data/permutations_file.json") -> None:

        """
        Generates a preview .json file that groups
        all the digit permutations of each key
        in the dictionary of the storage.

        :param permutation_file_path: The path to save the preview file.
        """

        if not os.path.exists(self.json_file_path):
            raise FileNotFoundError(f"File not found: {self.json_file_path}")

        with open(self.json_file_path, "r", encoding="utf-8") as file:
            number_data: Dict[str, Dict[str, Any]] = json.load(file)

        preview_data: Dict[str, Dict[str, Any]] = {}
        processed_keys: set[str] = set()

        for key, record in number_data.items():

            if key in processed_keys: continue

            base_number = int(key)
            subdivisions = record.get("sub-divisions", [])

            permutation_map: Dict[str, List[str]] = {}
            all_permutations = self._permutations_of(base_number)

            for perm in all_permutations:

                perm_str = str(perm)
                if perm_str in number_data:
                    phrases = number_data[perm_str].get("key-phrases", [])
                    permutation_map[perm_str] = phrases
                    processed_keys.add(perm_str)

            preview_data[key] = {
                "sub-divisions": subdivisions,
                "permutations": dict(sorted(permutation_map.items(), key=lambda x: int(x[0])))
            }

        os.makedirs(os.path.dirname(permutation_file_path), exist_ok=True)
        with open(permutation_file_path, "w", encoding="utf-8") as out_file:
            json.dump(preview_data, out_file, ensure_ascii=False, indent=4)

    def generate_variations_file(self, variations_file_path: str = "Data/variations_file.json") -> None:

        """
        Builds a variation indexing system,
        for each key inside the dictionary.

        :param variations_file_path: The path where the variation mapping will be written.
        :raises FileNotFoundError: If the number_file_path does not exist.
        :raises ValueError: If the number_file_path is not a valid .json.
        """

        if not os.path.exists(self.json_file_path):
            raise FileNotFoundError(f"File not found: {self.json_file_path}")

        try:

            with open(self.json_file_path, "r", encoding="utf-8") as f:
                number_data = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {self.json_file_path}: {exc}") from exc

        max_key_len = max((len(k) for k in number_data.keys()), default=0)
        variations_index: Dict[str, Dict[str, Dict[str, List[str]]]] = {}

        def _balanced_candidates(base: str) -> List[str]:

            """
            Generates balanced strings for two-digit
            distinct bases within the max length.

            :param base: The base key to be processed.
            :return: A list of all the candidates for base the key.
            """

            if len(base) != 2 or base[0] == base[1]: return []

            a, b = base[0], base[1]
            maximum_repeats = max_key_len // 2
            candidates: List[str] = []
            for n in range(1, maximum_repeats + 1):
                candidates.append(a * n + b * n)
                candidates.append(b * n + a * n)

            return candidates

        processed_keys: set[str] = set()
        for base_key in sorted(number_data.keys(), key=lambda s: int(s)):

            if base_key in processed_keys: continue
            variations_map: Dict[str, List[str]] = {}
            group_keys = set()

            if base_key in number_data:
                phrases = number_data.get(base_key, {}).get("key-phrases", [])
                variations_map[base_key] = phrases
                group_keys.add(base_key)

            # Step 1) Find the 'symmetrical' number of the base-key.
            symmetrical: str = base_key + base_key[::-1]
            if symmetrical in number_data:
                phrases = number_data.get(symmetrical, {}).get("key-phrases", [])
                variations_map[symmetrical] = phrases
                group_keys.add(symmetrical)

            # Step 2) Find the 'repetitive' numbers of the base-key.
            base_len = len(base_key)
            if base_len > 0:

                max_repeats = max_key_len // base_len
                for k in range(2, max_repeats + 1):

                    repeated: str = base_key * k
                    if repeated in number_data:
                        phrases = number_data.get(repeated, {}).get("key-phrases", [])
                        variations_map[repeated] = phrases
                        group_keys.add(repeated)

            # Step 3) Find the 'balanced' numbers for the base-key.
            for candidate in _balanced_candidates(base_key):

                if candidate in number_data:
                    phrases = number_data.get(candidate, {}).get("key-phrases", [])
                    variations_map[candidate] = phrases
                    group_keys.add(candidate)

            if len(variations_map) > 1:
                variations_index[base_key] = {
                    "variations": dict(
                        sorted(variations_map.items(), key=lambda x: int(x[0]))
                    )
                }
                processed_keys.update(group_keys)

        os.makedirs(os.path.dirname(variations_file_path), exist_ok=True)
        tmp_path = variations_file_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as out:
            json.dump(variations_index, out, ensure_ascii=False, indent=4)
        os.replace(tmp_path, variations_file_path)

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

        try:
            sequence = list(number_series)
        except TypeError as exc:
            raise TypeError("Numbers must be an iterable of integers.") from exc

        if not sequence: raise ValueError("Number list cannot be empty.")
        if any(not isinstance(n, int) for n in sequence):
            raise TypeError("All numbers must be integers.")

    def _insert_phrase(self, key_phrase: str, number_series: List[int]) -> None:

        """
        Inserts or updates a phrase for its primary number.

        :param key_phrase: The phrase to record.
        :param number_series: [primary_number, sub-divisions].
        """

        primary_number, sub_divisions = number_series[0], number_series[1:]
        key_str = str(primary_number)

        if key_str not in self.number_store:

            self.number_store[key_str] = {
                "sub-divisions": sub_divisions,
                "key-phrases": [key_phrase]
            }
        else:

            existing_phrases = set(self.number_store[key_str]["key-phrases"])
            existing_phrases.add(key_phrase)
            self.number_store[key_str]["key-phrases"] = sorted(existing_phrases)

    def _delete_phrase(self, key_phrase: str, primary_number: int) -> None:

        """
        Deletes a phrase under the specified primary number.

        :param key_phrase: The phrase to remove.
        :param primary_number: The primary number-key.
        :raises KeyError: If the key does not exist.
        :raises ValueError: If the phrase does not exist under the provided key.
        """

        key_str = str(primary_number)
        if key_str not in self.number_store:
            raise KeyError(f"Key {primary_number} does not exist.")

        try:
            self.number_store[key_str]["key-phrases"].remove(key_phrase)
        except ValueError as exc:
            raise ValueError(f"Phrase '{key_phrase}' does not exist under key {primary_number}.") from exc

    def _cleanup_store(self) -> None:

        """
        Removes all empty entries and keep the
        dictionary keys sorted in numerical order.
        """

        self.number_store = {k: v for k, v in self.number_store.items() if v["key-phrases"]}
        self.number_store = dict(sorted(self.number_store.items(), key=lambda item: int(item[0])))

    def _save_to_file(self, data: Optional[Dict[str, Any]] = None, path: Optional[str] = None) -> None:

        """
        Saves the provided or current data to a .json file,
        to improve readability and statistical post-analysis.

        :param data: The data to write to the disk.
        :param path: The target path for the data.
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
        Loads the dictionary from the disk. If the
        dictionary doesn't exist, then it raises an error.
        """

        if not os.path.exists(self.json_file_path): return {}
        try:
            with open(self.json_file_path, "r", encoding="utf-8") as fp:
                return json.load(fp)
        except (OSError, json.JSONDecodeError):
            return {}

    @staticmethod
    def _permutations_of(number: int) -> List[int]:

        """
        Returns all unique digit permutations 
        of a number as integers.

        :param number: The input number.
        :return: The unique permutations interpreted as integers.
        """

        return list({int("".join(p)) for p in permutations(str(number)) if p[0] != "0"})
