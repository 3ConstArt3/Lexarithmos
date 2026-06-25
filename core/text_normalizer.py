# -*- coding: utf-8 -*-
import unicodedata

from string import punctuation
from typing import List


class TextNormalizer:

    """
    Cleans and normalizes Greek text before
    lexarithmic processing.
    """

    def normalize(self, text: str) -> List[str]:

        """
        Converts raw text into clean uppercase words.

        :param text: The raw input text.
        :return: A list of cleaned uppercase words.
        """

        without_accents = self._remove_accents(text)
        without_symbols = self._remove_symbols(without_accents)
        return without_symbols.upper().split()

    @staticmethod
    def _remove_symbols(text: str) -> str:

        """
        Removes punctuation symbols from text.
        """

        return "".join(char for char in text if char not in punctuation)

    @staticmethod
    def _remove_accents(text: str) -> str:

        """
        Removes accents from Greek text.
        """

        normalized = unicodedata.normalize("NFD", text)

        without_accents = "".join(
            char for char in normalized
            if not unicodedata.combining(char)
        )

        return unicodedata.normalize("NFC", without_accents)
