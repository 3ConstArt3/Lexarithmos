# Lexarithmos

Lexarithmos is a console program made in Python, which allows the user to convert words (and therefore phrases) of the Greek language (ancient or modern) into numbers and store them in a JSON dictionary, from which he can draw various conclusions. In addition, the user can delete phrases, search for them through a numerical key or find phrases by entering other phrases with the same numerical key.

## Core Idea

As simplistic as this thought may seem, the result of this research is so far impressive! What anyone using this program can observe is that mathematics - and specifically numbers - define the Greek language, and therefore every word, phrase, or even idea created within it is related to similar (or seemingly unrelated) concepts! Of course, in order to find beautiful associations, one must be willing to question, think and imagine, which gives a pleasant atmosphere of discovery during the whole process :)

## Features

 * Phrase to arithmetic conversion: Convert any Greek phrase into its numerical form.
 * Persistent storage: Store the phrase along with its numerical information, in a JSON file, that updates after each insertion or deletion.
 * Key operations: Add, delete or search phrases.

## File structure

The data is stored in a JSON file(code/Data/numberFile.json) -, where each entry of that dictionary, has the following structure:

```json
{
    "key": {
        "divisions": ["d1", "d2", "...", "dN"],
        "phrases": ["s1", "s2", "...", "sM"]
    }
}
```

where 
 * key: The integer representation of each phrase sM.
 * divisions: An integer array, containing the subdivisions of the key.
 * phrases: A string array, containing all the phrases that have the same key.

## Usage

 * Search by key(0): This option tells the program, to run through the dictionary and then output the phrases that have a key equal to the one given by the user.
 * Search by phrase(1): This option tells the program, to run through the dictionary, spot where the phrase is, and then output all the phrases that are within the same list.
 * Insert a phrase(2): This option tells the program, to insert the phrase in the dictionary after it has been converted to its numerical form.
 * Delete a phrase(3): This option tells the program, to delete the phrase(if it exists) from the dictionary, while maintaining the integrity of the dictionary.

where the numbers inside the parenthesis() correspond to the parameter userOption, of the main resolve_flag() function.

## Example

Now let's run through some examples, in order for us to understand what the program actually does. Let's say that we want to insert the phrase "πληροφορική". This phrase, is converted to its numerical form which is 996, and its number divisions are (24, 6). Thus - considering the simplest case where an object with key = 996 doesn't exist - we insert into the dictionary the following object:

```json
"996": {
    "divisions": [24, 6],
    "phrases": ["πληροφορική"]
}
```

## Future improvements

My main goal is to create a graphical user interface, so that anyone can access and experiment with the dictionary, without having to deal with the code aspect of the console application :)

## Contributing

Contributions are welcome! If you'd like to contribute, feel free to fork the repository and submit a pull request!
