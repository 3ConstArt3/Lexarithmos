from typing import List

from Research.Lexarithmos.Utility.Transformer import Transformer
from Research.Lexarithmos.Utility.NumberFile import NumberFile

class Orchestrator:

    """
    Orchestrates the phrase -> number processing
    and updates the .json storage files, accordingly.
    To do that, it follows the logic given below:

    - It converts the phrase to its numeric subdivisions
    via the Transformer utility class.
    - It inserts | deletes the phrase in, by using the
    NumberFile utility class, based on the user's option.
    - It refreshes the derived .json files efficiently.
    """

    def __init__(self) -> None:

        """
        Initializes the core components of the app.
        """

        self.transformer = Transformer()
        self.number_file = NumberFile()

    def process(self, input_phrase: str, user_option: int) -> List[int]:

        """
        Processes a phrase according to the user's
        option and updates the storage accordingly.
        The supported actions are the following:

        - 2: Inserts a phrase and its numeric subdivisions.
        - 3: Deletes the phrase from the storage, if present.
        - Any input: No operation performed.

        :param input_phrase: The phrase to be processed.
        :param user_option: The operation selector.
        :return: A list of subdivisions for the input_phrase.
        :raises ValueError: If the input_phrase is not a string.
        """

        if not isinstance(input_phrase, str):
            raise ValueError("The input phrase, must be a string.")

        phrase = input_phrase.strip()
        if not phrase: return []

        try: subdivisions = self.transformer.transform_message(phrase)
        except Exception: return []

        if user_option not in (2, 3): return subdivisions

        try:

            self.number_file.update((phrase, subdivisions), insert=(user_option == 2))
            for generator in (
                self.number_file.generate_permutations_file,
                self.number_file.generate_variations_file,
            ):
                generator()
        except Exception: pass

        return subdivisions