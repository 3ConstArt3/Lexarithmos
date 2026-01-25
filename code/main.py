from typing import Tuple

from Research.Lexarithmos.Utility.Orchestrator import Orchestrator

class MainPipeline:

    def __init__(self) -> None:
        pass

    @staticmethod
    def _parse_action(action: str) -> int:

        a = action.strip().lower()
        if a in {"i", "insert", "2"}: return 2
        if a in {"d", "delete", "3"}: return 3
        return -1

    def _interactive_prompt(self) -> Tuple[str, int]:

        """
        Prompts the user repeatedly for a phrase
        and a desired action (insert, delete or
        a default print), until he types "quit".

        :return: A (phrase, user_option) tuple.
        """

        print("\nType your phrase (or 'quit' to exit): ")
        phrase = input("--> ").strip()
        if phrase.lower() in {"quit"}: return "", -1

        if not phrase:

            print("\n!!! Warning !!!")
            print("The phrase cannot be empty!")
            return "", -1

        print("\n#############################################")
        print("# Action list                               #")
        print("# -----------                               #")
        print("#                                           #")
        print("# => Insert: [i] [I] [insert] [Insert] [2]. #")
        print("# => Delete: [d] [D] [delete] [Delete] [3]. #")
        print("# => Enter: Computes only.                  #")
        print("#############################################\n")

        action = input("--> ").strip().lower()
        user_option = self._parse_action(action)
        return phrase, user_option

    def run(self) -> int:

        """
        The entry point of the CLI.

        :return: The process's exit code.
        """

        print("\n#################################")
        print("# Welcome to my application! :) #")
        print("#################################\n")

        print("#################################################################")
        print("# Notes                                                         #")
        print("# -----                                                         #")
        print("#                                                               #")
        print("# Here you can type words, letters, phrases, or even entire     #\n"
              "# sentences, in order to translate them into numbers. The       #\n"
              "# word -> number transformation process is called \'lexarithmos\' #\n"
              "# , which is named after the greek words \'lexis\' (word) and     #\n"
              "# \'arithmos\' (number). Each transformation you make, has a      #\n"
              "# meaning behind it, which makes the Greek language unique!     #")
        print("#################################################################")

        orchestrator = Orchestrator()
        try:

            while True:

                phrase, user_option = self._interactive_prompt()
                if not phrase:

                    print("\n###############################")
                    print("# Thanks for using my app ^_^ #")
                    print("###############################")
                    break

                subdivisions = orchestrator.process(phrase, user_option)
                if subdivisions:

                    print(f"[Phrase]: {phrase}")
                    print(f"[Subdivisions]: {subdivisions}")
                else:
                    print("No subdivisions produced.")
        except KeyboardInterrupt:

            print("\nProcess aborted by the user.")
            return 130

        return 0

if __name__ == "__main__":

    pipeline = MainPipeline()
    raise SystemExit(pipeline.run())
