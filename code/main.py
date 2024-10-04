# -*- coding: utf-8 -*-

from Public.Research.WordNumber.Utility.Transformer import *
from Public.Research.WordNumber.Utility.NumberFile import *

class Solution:

    """
    A class that is used, in order to
    solve the problem, presented.

    ...

    Attributes
    ----------
    transformer: Transformer
        An object, used to transform
        a string message.

    numberFile: NumberFile
        An object, used to update or
        retrieve information from a
        .json file.
    """

    """
    Constructor definition
    """
    def __init__(self):

        self.transformer = Transformer()
        self.numberFile = NumberFile()

    """ 
    Function definition
    """
    def resolve_flag(self, message: str, userOption: int) -> list:

        """
        Solves the main problem.

        ...

        Parameters
        ----------
        message: str
            The message, to be processed.

        userOption: int
            The user's choice, of how to
            update the stored numberFile.

        Returns
        -------
        list
            Contains the problem's solution.
        """

        numberList = self.transformer.transform(message)
        information = (message, numberList)
        self.numberFile.update(information, userOption)
        self.numberFile.preview()

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
