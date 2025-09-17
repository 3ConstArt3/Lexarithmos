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
        self.number_store = self._load_from_file()

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

    def generate_permutations_file(self, permutation_file_path: str = "Data/permutations_file.json") -> None:

        """
        Generate a preview JSON file that groups all digit permutations of each key in the number file.

        :param permutation_file_path: Path to save the generated preview_file.json.
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
        Build a variations index for each base key found in ``number_file.json`` and
        save it to ``variations_file.json``.

        :param variations_file_path: Output JSON path where the variation mapping will be written.
        :raises FileNotFoundError: If ``number_file_path`` does not exist.
        :raises ValueError: If ``number_file_path`` is not valid JSON.
        """

        if not os.path.exists(self.json_file_path):
            raise FileNotFoundError(f"File not found: {self.json_file_path}")

        try:
            with open(self.json_file_path, "r", encoding="utf-8") as f:
                number_data: Dict[str, Dict[str, Any]] = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {self.json_file_path}: {exc}") from exc

        max_key_len: int = max((len(k) for k in number_data.keys()), default=0)
        variations_index: Dict[str, Dict[str, Dict[str, List[str]]]] = {}

        def _balanced_candidates(base: str) -> List[str]:

            """Generate balanced strings for two-digit distinct bases within max length."""
            if len(base) != 2 or base[0] == base[1]:
                return []
            a, b = base[0], base[1]
            max_repeats = max_key_len // 2  # each balanced block has length 2*n
            candidates: List[str] = []
            for n in range(1, max_repeats + 1):
                candidates.append(a * n + b * n)  # a..ab..b
                candidates.append(b * n + a * n)  # b..ba..a
            return candidates

        processed_keys: set[str] = set()

        # Iterate in numeric order so the smallest representative key owns the group.
        for base_key in sorted(number_data.keys(), key=lambda s: int(s)):

            if base_key in processed_keys: continue
            variations_map: Dict[str, List[str]] = {}
            group_keys: set[str] = set()

            # Include the base key itself if present.
            if base_key in number_data:

                phrases = number_data.get(base_key, {}).get("key-phrases", [])
                variations_map[base_key] = phrases
                group_keys.add(base_key)

            # Symmetrical number (base + reversed(base)).
            symmetrical: str = base_key + base_key[::-1]
            if symmetrical in number_data:

                phrases = number_data.get(symmetrical, {}).get("key-phrases", [])
                variations_map[symmetrical] = phrases
                group_keys.add(symmetrical)

            # Repetitive numbers: base repeated k times for k ≥ 2.
            base_len: int = len(base_key)
            if base_len > 0:

                max_repeats: int = max_key_len // base_len
                for k in range(2, max_repeats + 1):

                    repeated: str = base_key * k
                    if repeated in number_data:

                        phrases = number_data.get(repeated, {}).get("key-phrases", [])
                        variations_map[repeated] = phrases
                        group_keys.add(repeated)

            # Balanced numbers (only for two-digit bases with distinct digits).
            for cand in _balanced_candidates(base_key):

                if cand in number_data:

                    phrases = number_data.get(cand, {}).get("key-phrases", [])
                    variations_map[cand] = phrases
                    group_keys.add(cand)

            # Only add the base key to the index if it has at least one variation beyond itself.
            if len(variations_map) > 1:

                variations_index[base_key] = {
                    "variations": dict(sorted(variations_map.items(), key=lambda x: int(x[0])))
                }

                # Mark all keys in this group as processed, so they won't become separate entries later.
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
        
        try: sequence = list(number_series)
        except TypeError as exc: raise TypeError("Numbers must be an iterable of integers.") from exc

        if not sequence: raise ValueError("Number list cannot be empty.")
        if any(not isinstance(n, int) for n in sequence):
            raise TypeError("All numbers must be integers.")

    def _insert_phrase(self, key_phrase: str, number_series: List[int]) -> None:
        
        """
        Inserts or updates a phrase for its primary number.

        :param key_phrase: The phrase to record.
        :param number_series: [primary_number, *divisions].
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
        :raises ValueError: If the phrase does not exist under the key.
        """
        
        key_str = str(primary_number)
        if key_str not in self.number_store:
            raise KeyError(f"Key {primary_number} does not exist.")

        try: self.number_store[key_str]["key-phrases"].remove(key_phrase)
        except ValueError as exc: raise ValueError(f"Phrase '{key_phrase}' does not exist under key {primary_number}.") from exc

    def _cleanup_store(self) -> None:
        
        """
        Remove all empty entries and keep keys sorted numerically.
        """
        
        self.number_store = {k: v for k, v in self.number_store.items() if v["key-phrases"]}
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

        return list({int("".join(p)) for p in permutations(str(number)) if p[0] != "0"})
