# -*- coding: utf-8 -*-

import unicodedata
from string import punctuation

class Transformer:

    """
    A class that is used, in order to transform
    the passing phrase || message, into a clean
    version of itself - removing any special accents
    or symbols - and then into a list of numbers,
    called subdivisions.

    ...

    Attributes
    ----------
    letterMap : dict
        A dictionary containing the integer
        values of each greek letter, in the
        alphabet.
    """

    """
    Constructor definition
    """
    def __init__(self):

        self.letterMap = {
            "Α": 1,
            "Β": 2,
            "Γ": 3,
            "Δ": 4,
            "Ε": 5,
            "Ζ": 7,
            "Η": 8,
            "Θ": 9,
            "Ι": 10,
            "Κ": 20,
            "Λ": 30,
            "Μ": 40,
            "Ν": 50,
            "Ξ": 60,
            "Ο": 70,
            "Π": 80,
            "Ρ": 100,
            "Σ": 200,
            "Τ": 300,
            "Υ": 400,
            "Φ": 500,
            "Χ": 600,
            "Ψ": 700,
            "Ω": 800
        }

    """
    Function definition
    """
    def transform(self, message: str) -> list:

        """
        Finds the numerical subdivisions
        of the cleaned message's integer
        representation.

        ...

        Parameters
        ----------
        message: str
            The message, to be processed.

        Returns
        -------
        list
            Contains the message's subdivisions.
        """

        cleanedMessage = self.clean_message(message)
        wordNumber = sum(self.word_number_of(word, self.letterMap)
                         for word in cleanedMessage)
        return self.subdivisions_of(wordNumber)

    def clean_message(self, message: str) -> list:

        """
        Cleans the message, from its
        symbols and accents.

        ...

        Parameters
        ----------
        message: str
            The message to be cleaned.

        Returns
        -------
        list
            The cleaned message's characters.
        """

        noAccentMessage = self.remove_accents(message)
        cleanMessage = self.remove_symbols(noAccentMessage)
        return cleanMessage.upper().split()

    @staticmethod
    def remove_symbols(message: str) -> str:

        """
        Cleans the message from
        symbolic characters.

        ...

        Parameters
        ----------
        message: str
            The message, to be cleaned.

        Returns
        -------
        str
            The final cleaned message.
        """

        return "".join(c for c in message
                       if c not in punctuation)

    @staticmethod
    def remove_accents(message: str) -> str:

        """
        Cleans the message, from accents.

        ...

        Parameters
        ----------
        message: str
            The message to be cleaned.

        Returns
        -------
        str
            The final cleaned message.
        """

        normalizedMessage = unicodedata.normalize('NFD', message)
        messageWithoutAccents = ''.join([c for c in normalizedMessage
                                         if not unicodedata.combining(c)])
        return unicodedata.normalize('NFC', messageWithoutAccents)

    @staticmethod
    def word_number_of(word: str, letterMap: dict) -> int:

        """
        Finds the integer representation
        of the given word.

        ...

        Parameters
        ----------
        word: str
            The phrase to be evaluated.

        letterMap: dict
            The dictionary, that maps every character
            of the given word, to its corresponding
            arithmetic value.

        Returns
        -------
        int
            The word number of the given word.
        """

        return sum([letterMap[letter]
                    for letter in word])

    @staticmethod
    def subdivisions_of(number: int) -> list:

        """
        Finds the subdivisions of
        the given number.

        ...

        Parameters
        ----------
        number: int
            The number, from which the
            subdivisions are found.

        Returns
        -------
        list
            The list containing the subdivisions.
        """

        numberList = [number]
        digitSum = lambda x: sum(int(d) for d in str(x))
        while number >= 10:

            number = digitSum(number)
            numberList.append(number)

        return numberList