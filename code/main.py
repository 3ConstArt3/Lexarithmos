# -*- coding: utf-8 -*-
from Utility.Transformer import Transformer
from Utility.NumberFile import NumberFile

class Solution:

    def __init__(self):

        self.transformer = Transformer()
        self.numberFile = NumberFile()

    def resolve_flag(self, message: str, userOption: int) -> list:

        numberList = self.transformer.transform_message(message)

        if userOption == 2: insert = True
        elif userOption == 3: insert = False
        else: return []

        self.numberFile.update((message, numberList), insert)
        self.numberFile.generate_permutations_file()
        self.numberFile.generate_variations_file()

        return numberList

    def solve(self) -> None:

        """
        The main function of the program,
        where all outputs are viewed.
        """

        message = ""
        flag = self.resolve_flag(message, 3)

        if message:

            print(f"\nPhrase: {message}")
            print(f"Subdivisions: {flag}")

if __name__ == "__main__":

    solution = Solution()
    solution.solve()
