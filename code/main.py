from typing import Tuple
from Research.Lexarithmos.Utility.Orchestrator import Orchestrator

class MainPipeline:

    def __init(self):
        pass

    @staticmethod
    def _interactive_prompt() -> Tuple[str, int]:

        """
        Prompts the user repeatedly for a phrase
        and a desired action (insert, delete or
        a default print), until he types "quit".

        :return: A (phrase, user_option) tuple.
        """

        print("\nEnter a phrase (or 'quit' to exit): ")
        phrase = input("--> ").strip()
        if phrase.lower() in {"quit"}: return "", -1

        if not phrase:
            print("Phrase cannot be empty. Please try again.")
            return "", -1

        print("\n=========================================")
        print("Action list:\n")
        print("=> Insert: [i] [I] [insert] [Insert] [2].")
        print("=> Delete: [d] [D] [delete] [Delete] [3].")
        print("=> Enter: Computes only.")
        print("=========================================\n")

        action = input("--> ").strip().lower()
        if action in ("i", "I", "insert", "Insert", "2"):
            user_option = 2
        elif action in ("d", "D", "delete", "Delete", "3"):
            user_option = 3
        else:
            user_option = -1

        return phrase, user_option

    def run(self) -> int:

        """
        The entry point of the CLI.

        :return: The process's exit code.
        """

        print("\nInteractive mode — type your phrase, or 'quit' to exit.")
        solution = Orchestrator()
        try:

            while True:

                phrase, user_option = self._interactive_prompt()
                if not phrase:
                    print("Thanks for using my app ^_^")
                    break

                subdivisions = solution.process(phrase, user_option)
                if subdivisions:

                    print(f"Phrase: {phrase}")
                    print(f"Subdivisions: {subdivisions}")
                else:
                    print("No subdivisions produced.")
        except KeyboardInterrupt:

            print("\nProcess aborted by the user.")
            return 130

        return 0

if __name__ == "__main__":

    pipeline = MainPipeline()
    raise SystemExit(pipeline.run())
