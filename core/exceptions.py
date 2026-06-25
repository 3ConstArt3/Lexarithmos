# -*- coding: utf-8 -*-


class LexarithmosError(Exception):

    """
    Base exception for the Lexarithmos application.
    """

    pass


class InvalidPhraseError(LexarithmosError):

    """
    Raised when the provided phrase is invalid.
    """

    pass


class PhraseStorageError(LexarithmosError):

    """
    Raised when phrase storage operations fail.
    """

    pass


class PhraseNotFoundError(LexarithmosError):

    """
    Raised when a phrase does not exist in storage.
    """

    pass


class AnalysisError(LexarithmosError):

    """
    Raised when an analysis operation fails.
    """

    pass
