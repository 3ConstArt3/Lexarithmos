# -*- coding: utf-8 -*-
from typing import List

from core.text_normalizer import TextNormalizer
from core.lexarithmos_calculator import LexarithmosCalculator
from core.digit_reducer import DigitReducer
from core.models import PhraseAnalysis


class Transformer:

    """
    Coordinates text normalization, lexarithmic
    calculation and digit reduction.
    """

    def __init__(self) -> None:

        """
        Initializes the transformer components.
        """

        self.normalizer = TextNormalizer()
        self.calculator = LexarithmosCalculator()
        self.reducer = DigitReducer()

    def transform_message(self, text: str) -> List[int]:

        """
        Transforms Greek text into numeric subdivisions.

        This method remains available for compatibility
        with the existing application flow.
        """

        analysis = self.analyze_message(text)
        return analysis.subdivisions

    def analyze_message(self, text: str) -> PhraseAnalysis:

        """
        Produces a complete lexarithmic analysis
        for the given Greek text.

        :param text: The original input text.
        :return: A PhraseAnalysis object.
        """

        normalized_words = self.normalizer.normalize(text)
        total_value = self.calculator.calculate_phrase_value(normalized_words)
        subdivisions = self.reducer.reduce(total_value)

        return PhraseAnalysis(
            original_text=text,
            normalized_words=normalized_words,
            total_value=total_value,
            subdivisions=subdivisions
        )
