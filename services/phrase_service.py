# -*- coding: utf-8 -*-
from typing import Optional

from core.actions import Action
from core.exceptions import InvalidPhraseError
from core.models import PhraseAnalysis, PhraseResult
from core.transformer import Transformer
from storage.number_repository import NumberRepository
from analysis.pipeline.analysis_pipeline import AnalysisPipeline
from analysis.pipeline.default_pipeline import build_default_pipeline


class PhraseService:

    """
    Handles phrase analysis, storage actions
    and analyzer refresh operations.
    """

    def __init__(
        self,
        transformer: Optional[Transformer] = None,
        number_repository: Optional[NumberRepository] = None,
        analysis_pipeline: Optional[AnalysisPipeline] = None
    ) -> None:

        """
        Initializes the phrase service dependencies.

        External dependencies can be injected
        for testing or custom research workflows.
        """

        self.transformer = transformer or Transformer()
        self.number_repository = number_repository or NumberRepository()
        self.analysis_pipeline = analysis_pipeline or build_default_pipeline()

    def process(self, input_phrase: str, action: Action) -> PhraseResult:

        """
        Processes a phrase and returns a complete result.
        """

        analysis = self.analyze(input_phrase)

        if action == Action.INSERT:

            self.insert(analysis)

            return PhraseResult(
                analysis=analysis,
                action=action,
                success=True,
                message="Phrase inserted successfully."
            )

        if action == Action.DELETE:

            self.delete(analysis)

            return PhraseResult(
                analysis=analysis,
                action=action,
                success=True,
                message="Phrase deleted successfully."
            )

        return PhraseResult(
            analysis=analysis,
            action=Action.COMPUTE_ONLY,
            success=True,
            message="Phrase computed successfully."
        )

    def analyze(self, input_phrase: str) -> PhraseAnalysis:

        """
        Produces a complete phrase analysis.
        """

        self._validate_phrase(input_phrase)
        phrase = input_phrase.strip()

        return self.transformer.analyze_message(phrase)

    def insert(self, analysis: PhraseAnalysis) -> None:

        """
        Stores a phrase analysis and refreshes analyzers.
        """

        self.number_repository.insert(analysis)
        self._refresh_analyzers()

    def delete(self, analysis: PhraseAnalysis) -> None:

        """
        Deletes a phrase analysis and refreshes analyzers.
        """

        self.number_repository.delete(analysis)
        self._refresh_analyzers()

    def _refresh_analyzers(self) -> None:

        """
        Refreshes derived research files.
        """

        self.analysis_pipeline.run_all(
            self.number_repository.get_all()
        )

    @staticmethod
    def _validate_phrase(input_phrase: str) -> None:

        """
        Validates the input phrase.
        """

        if not isinstance(input_phrase, str):
            raise InvalidPhraseError(
                "The input phrase must be a string."
            )

        if not input_phrase.strip():
            raise InvalidPhraseError(
                "The input phrase cannot be empty."
            )
