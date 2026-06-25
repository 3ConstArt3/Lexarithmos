# -*- coding: utf-8 -*-
from typing import Tuple

from core.actions import Action
from services.phrase_service import PhraseService
from core.models import PhraseResult

from core.exceptions import LexarithmosError


class LexarithmosCLI:

    """
    Handles the command-line interaction
    of the Lexarithmos application.
    """

    def __init__(self) -> None:

        """
        Initializes the CLI dependencies.
        """

        self.phrase_service = PhraseService()

    def run(self) -> int:

        """
        Runs the command-line application.

        :return: The process exit code.
        """

        self._print_welcome_message()

        try:

            while True:

                phrase, action = self._read_user_input()

                if not phrase:
                    self._print_exit_message()
                    break

                result = self.phrase_service.process(phrase, action)

                self._print_result(result)

        except KeyboardInterrupt:

            print("\nProcess aborted by the user.")
            return 130

        except LexarithmosError as error:

            print(f"\n[Lexarithmos Error]: {error}")
            return 1

        except Exception as error:

            print(f"\n[Unexpected Error]: {error}")
            return 1

        return 0

    @staticmethod
    def _parse_action(action: str) -> Action:

        """
        Converts user action text into an Action value.
        """

        normalized_action = action.strip().lower()

        if normalized_action in {"i", "insert", "2"}:
            return Action.INSERT

        if normalized_action in {"d", "delete", "3"}:
            return Action.DELETE

        return Action.COMPUTE_ONLY

    def _read_user_input(self) -> Tuple[str, Action]:

        """
        Reads phrase and action from the user.

        :return: A tuple containing the phrase and selected action.
        """

        print("\nType your phrase (or 'quit' to exit): ")
        phrase = input("--> ").strip()

        if phrase.lower() == "quit":
            return "", Action.COMPUTE_ONLY

        if not phrase:

            print("\n!!! Warning !!!")
            print("The phrase cannot be empty!")
            return "", Action.COMPUTE_ONLY

        self._print_action_menu()

        action_text = input("--> ").strip()
        action = self._parse_action(action_text)

        return phrase, action

    @staticmethod
    def _print_result(result: PhraseResult) -> None:

        """
        Prints the produced phrase processing result.
        """

        analysis = result.analysis

        print(f"\n[Status]: {'Success' if result.success else 'Failed'}")
        print(f"[Action]: {result.action.value}")
        print(f"[Message]: {result.message}")
        print(f"[Phrase]: {analysis.original_text}")
        print(f"[Normalized Words]: {analysis.normalized_words}")
        print(f"[Total Value]: {analysis.total_value}")
        print(f"[Subdivisions]: {analysis.subdivisions}")

    @staticmethod
    def _print_welcome_message() -> None:

        """
        Prints the welcome message.
        """

        print("\n#################################")
        print("# Welcome to my application! :) #")
        print("#################################\n")

        print("#################################################################")
        print("# Notes                                                         #")
        print("# -----                                                         #")
        print("#                                                               #")
        print("# Here you can type words, letters, phrases, or even entire     #")
        print("# sentences, in order to translate them into numbers. The       #")
        print("# word -> number transformation process is called 'lexarithmos'. #")
        print("# Each transformation you make has a meaning behind it, which   #")
        print("# makes the Greek language unique!                              #")
        print("#################################################################")

    @staticmethod
    def _print_action_menu() -> None:

        """
        Prints the available action menu.
        """

        print("\n#############################################")
        print("# Action list                               #")
        print("# -----------                               #")
        print("#                                           #")
        print("# => Insert: [i] [insert] [2].              #")
        print("# => Delete: [d] [delete] [3].              #")
        print("# => Enter: Computes only.                  #")
        print("#############################################\n")

    @staticmethod
    def _print_exit_message() -> None:

        """
        Prints the exit message.
        """

        print("\n###############################")
        print("# Thanks for using my app ^_^ #")
        print("###############################")
