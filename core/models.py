# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from core.actions import Action


@dataclass(frozen=True)
class PhraseAnalysis:

    """
    Represents the complete lexarithmic
    analysis result of a phrase.
    """

    original_text: str
    normalized_words: List[str]
    total_value: int
    subdivisions: List[int]


@dataclass(frozen=True)
class PhraseResult:

    """
    Represents the final result of a phrase
    processing action.
    """

    analysis: PhraseAnalysis
    action: Action
    success: bool
    message: str
