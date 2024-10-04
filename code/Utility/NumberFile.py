import json
from itertools import permutations

class NumberFile:

    """
    A class that is used in order to represent
    the dictionary, containing all the phrases
    that are stored from the user, along with
    their word number values.

    ...

    Attributes
    ----------
    userOptions : dict
        A dictionary containing available user options.
        Here the options are insert | delete, which
        correspond to 1 | 0 respectively.

    fileName: str
        A string, that contains the name of the file,
        that the dictionary is going to be saved | loaded.

    numberFile: dict
        The dictionary, containing, all the unique
        word numbers, along with the phrases, that
        result to its arithmetic value.
    """

    """
    Constructor definition
    """
    def __init__(self):

        self.userOptions = {
            "search_by_key": 0,
            "search_by_phrase": 1,
            "insert_phrase": 2,
            "delete_phrase": 3
        }

        self.fileName = 'Data/numberFile.json'
        self.numberFile = self.load_from(self.fileName)

    """
    Function definition
    """
    def update(self, information: tuple, userOption: int) -> None:

        """
        Updates self.numberFile's structure.

        Parameters
        ----------
        information: tuple
            The information for which an insertion or
            search of deletion is going to happen.
        userOption: int
            The user's choice for managing the passing
            information. He can either search by a key
            | search by a phrase | insert a phrase |
            delete a phrase.
        """

        if userOption == self.userOptions["search_by_key"]:

            print("\nPlease provide the key:")
            key = int(input())
            self.search_by_key(key)
        elif userOption == self.userOptions["search_by_phrase"]:

            print("\nPlease provide the phrase:")
            phrase = str(input())
            self.search_by_phrase(phrase)
        elif userOption == self.userOptions["insert_phrase"]:

            print("\nInserting information...")
            self.insert(information)
        elif userOption == self.userOptions["delete_phrase"]:

            print("\nDeleting information...")
            self.delete(information)
        else:

            print("\nInput error!\n")
            return

        self.numberFile = {k: self.numberFile[k]
                           for k in sorted(self.numberFile, key=int)}

        self.clean_file()
        self.save_to(self.numberFile, self.fileName)

    def preview(self) -> None:

        """
        Creates a specific preview, of the
        self.numberFile dictionary.
        """

        keys = sorted(int(key) for key in self.numberFile.keys())
        previewFile = {}

        while keys:

            key = keys[0]
            stringKey = str(key)
            divisions = self.numberFile[stringKey]['divisions']
            previewFile[stringKey] = {"divisions": divisions, "anagrams": {}}

            for newKey in self.permutations_of(key):

                newStringKey = str(newKey)
                if newKey in keys:

                    phrases = self.numberFile[newStringKey]['phrases']
                    previewFile[stringKey]['anagrams'][newKey] = phrases
                    del self.numberFile[newStringKey]
                    keys.remove(newKey)

        for key in previewFile.keys():
            anagrams = previewFile[key]['anagrams']
            previewFile[key]['anagrams'] = {
                k: anagrams[k]
                for k in sorted(anagrams, key=int)
            }

        fileName = "Data/previewFile.json"
        self.save_to(previewFile, fileName)

    def search_by_key(self, key: int) -> None:

        """
        Searches in the dictionary
        for a specific object.

        ...

        Parameters
        ----------
        key: int
            The object's key, to search for.
        """
        try:

            print(f"\nPhrases found for key ({key}):")
            print(self.numberFile[str(key)]['phrases'])
        except KeyError:

            print("\nKeyError:")
            print(f"Key '{key}' doesn't exist.")

    def search_by_phrase(self, phrase: str) -> None:

        """
        Searches in the dictionary
        for a specific key.

        ...

        Parameters
        ----------
        phrase: str
            The object's phrase to search for.
        """
        for key in self.numberFile.keys():

            phrases = self.numberFile[key]['phrases']
            if phrase in phrases:

                print(f"\nPhrases found for phrase ({phrase}):")
                print(phrases)
                break

    def insert(self, information: tuple) -> None:

        """
        Inserts information in self.numberFile.

        ...

        Parameters
        ----------
        information: tuple
            The necessary information, for the insertion.
        """

        phrase, numberList = information
        key, divisions = numberList[0], numberList[1:]
        infoExists = (str(key) in self.numberFile)

        if infoExists:
            self.add_phrase(phrase, key)
            return

        self.add_object((divisions, phrase), key)

    def add_object(self, objectInfo: tuple, key: int) -> None:

        """
        Adds a new object, to self.numberFile
        with the specified key.

        ...

        Parameters
        ----------
        objectInfo: tuple
            Contains the information of the object.

        key: int
            The key, where the object is stored.
        """

        divisions, phrase = objectInfo
        self.numberFile[str(key)] = {
            "divisions": divisions,
            "phrases": [phrase]
        }

    def add_phrase(self, phrase: str, key: int) -> None:

        """
        Adds a new phrase, to the attribute 'phrases',
        of self.numberFile's key value.

        ...

        Parameters
        ----------
        phrase: str
            The phrase to be inserted.

        key: int
            The key where the phrase is
            going to be stored at.
        """

        dictionary = self.numberFile[str(key)]
        dictionary['phrases'].append(phrase)
        phrases = dictionary['phrases'].copy()
        dictionary['phrases'] = list(set(phrases))
        dictionary['phrases'].sort()

    def delete(self, information: tuple) -> None:

        """
        Deletes information in self.numberFile.

        ...

        Parameters
        ----------
        information: tuple
            The necessary information, for the deletion.
        """

        phrase, numberList = information
        key = numberList[0]

        try:

            self.delete_phrase(phrase, key)
        except KeyError:

            print("\nKeyError:")
            print(f"Key '{key}' doesn't exist.")

    def delete_phrase(self, phrase: str, key: int) -> None:

        """
        Deletes the given phrase.

        ...

        Parameters
        ----------
        phrase: str
            The phrase to be deleted.

        key: int
            The key, where the deletion occurs.
        """
        try:

            self.numberFile[str(key)]['phrases'].remove(phrase)
        except ValueError:

            print("\nValueError:")
            print(f"Phrase '{phrase}' doesn't exist.")

    def clean_file(self) -> None:

        """
        Removes the file's objects
        that don't have any phrases.
        """

        keysToDelete = [key for key, value in self.numberFile.items()
                        if len(value['phrases']) == 0]
        for key in keysToDelete:
            del self.numberFile[str(key)]

    @staticmethod
    def permutations_of(number: int) -> list:

        """
        Finds the integer permutations of number.

        ...

        Parameters
        ----------
        number: int
            The number necessary, to find his
            permutation list.

        Returns
        -------
        list
            The list containing number's permutations.
        """

        return list(set(int(''.join(p))
                        for p in permutations(str(number))))

    @staticmethod
    def save_to(data: dict, fileName: str) -> None:

        """
        Saves the data, in a .json file.

        ...

        Parameters
        ----------
        data: dict
            The data, to store in the file.

        fileName: str
            The name of the file, to store
            the data.
        """

        with open(fileName, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_from(fileName: str) -> dict:

        """
        Loads the data from a .json file.

        ...

        Parameters
        ----------
        fileName: str
            The name of the file, the user wants
            to use, to load the data from it.

        Returns
        -------
        dict
            The dictionary stored in the file.

        """

        with open(fileName, 'r', encoding='utf-8') as file:
            return json.load(file)