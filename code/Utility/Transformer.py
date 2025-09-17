# -*- coding: utf-8 -*-
import unicodedata

from string import punctuation
from typing import List

class Transformer:

    """
    Transforms Greek words into numerical
    values based on a predefined letter
    mapping. It cleans the input text by
    removing accents, symbols and
    punctuation, it then computes
    word values and produces subdivisions
    of the resulting total value (digit sums).
    """

    LETTER_TO_VALUE = {
        "Α": 1, "Β": 2, "Γ": 3, "Δ": 4, "Ε": 5,
        "Ζ": 7, "Η": 8, "Θ": 9, "Ι": 10, "Κ": 20,
        "Λ": 30, "Μ": 40, "Ν": 50, "Ξ": 60, "Ο": 70,
        "Π": 80, "Ρ": 100, "Σ": 200, "Τ": 300, "Υ": 400,
        "Φ": 500, "Χ": 600, "Ψ": 700, "Ω": 800
    }

    def transform_message(self, text: str) -> List[int]:

        """
        Transforms a Greek text into a list of numerical subdivisions.

        :param text: The input Greek text.
        :return: A list of subdivisions derived from the total numerical value.
        """

        words = self._clean_text(text)
        total_value = sum(self._compute_word_value(word) for word in words)
        return self._digit_subdivisions(total_value)

    def _clean_text(self, text: str) -> List[str]:

        """
        Removes accents and punctuation from the text, converts
        them to uppercase, and splits them into words.

        :param text: The raw input text.
        :return: The cleaned uppercase words.
        """

        without_accents = self._remove_accents(text)
        without_symbols = self._remove_symbols(without_accents)
        return without_symbols.upper().split()

    @staticmethod
    def _remove_symbols(text: str) -> str:

        """
        Removes all punctuation symbols from the text.

        :param text: The text to process.
        :return: The text without punctuation.
        """
        return "".join(char for char in text if char not in punctuation)

    @staticmethod
    def _remove_accents(text: str) -> str:

        """
        Removes all accents from the Greek text.

        :param text: The text to process.
        :return: The text without accents.
        """

        normalized = unicodedata.normalize("NFD", text)
        without_accents = "".join(
            char for char in normalized
            if not unicodedata.combining(char)
        )

        return unicodedata.normalize("NFC", without_accents)

    def _compute_word_value(self, word: str) -> int:

        """
        Computes the numerical value of a single
        word based on a Greek letter map.

        :param word: A word containing Greek characters.
        :return: The numerical value of the word.
        :raises ValueError: If the word contains invalid characters.
        """

        try:

            return sum(
                self.LETTER_TO_VALUE[char] for char in word
                if char in self.LETTER_TO_VALUE
            )
        except KeyError as error:
            raise ValueError(f"Invalid character '{error.args[0]}' in word '{word}'.") from error

    @staticmethod
    def _digit_subdivisions(number: int) -> List[int]:

        """
        Generates subdivisions of a number by
        repeatedly summing its digits until it is < 10.

        :param number: The input number.
        :return: A list of all subdivisions, including the original number.
        """

        subdivisions = [number]
        while number >= 10:

            number = sum(int(digit) for digit in str(number))
            subdivisions.append(number)

        return subdivisions
