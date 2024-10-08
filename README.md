# Lexarithmos

`Lexarithmos`, is a console program made in Python, which allows the user to convert words (and therefore phrases) of the Greek language (ancient or modern) into numbers and store them in a **JSON** dictionary, from which he can draw various conclusions about our world!

### Core idea💡

As simplistic as this thought may seem, the result of this research is so far impressive! What anyone can observe, is that **mathematics** - and specifically numbers - define the **Greek** language, and therefore every word, phrase, or even idea created within it is related to similar (or seemingly unrelated) concepts! Of course, in order to find beautiful associations, one must be willing to **question**, think and imagine, which gives a pleasant atmosphere of **discovery** during the whole process🙂.

### Features⚙️

 * `Phrase to number`: Convert any Greek phrase into its numerical form, using a specific letter map.
 * `Dictionary format`: Store the phrase and its numerical information, in a **JSON** file, which updates after each insertion or deletion.
 * `Basic operations`: Addition, Deletion and Search.

**NOTE**: The map isn't random as it may seem! On the contrary, it is a recent historical discovery at an archaeological site in Greece, which makes it even more intriguing!

### DictionaryForm📄

The main **data**(aka phrases, numerical divisions) is stored in a **JSON** file, which can be found under the folder `code/Data/` with name `numberFile.json` -, where each entry of that dictionary, has the following structure:

```json
{
    "key": {
        "divisions": [
            "d1",
            "d2",
            "...",
            "dN"
        ],
        "phrases": [
            "s1",
            "s2",
            "...",
            "sM"
        ]
    }
}
```

where

 * `N, M`: The integer **indices**, which define the length of each array.
 * `key`: The **integer** representation of each phrase sM.
 * `divisions`: An **array**, containing every integer subdivision dN of the key.
 * `phrases`: An **array**, containing all the phrases that have the same key.

**NOTE**: The `subdivisions` of a natural number n, are the numbers that result each time from adding up all the digits of the number we currently have, until the number of digits in the result is 1.

### Usage🪛

In this section, we're going to see the main `operations` the program has to offer, where each one is passed as a number in the function resolve_number(), in its field **userOption**. Being more specific, we have the following operations:

```python
self.userOptions = {
    "search_by_key": 0,
    "search_by_phrase": 1,
    "insert_phrase": 2,
    "delete_phrase": 3
}
```

 1. `Search by key`: This option is denoted by the integer `0`. 
    * The user inputs a key and the program returns the phrases that have that same **key**.
 2. `Search by phrase`: This option is denoted by the integer `1`.
    * The user inputs a phrase and the program returns the phrases that lie within the same [] of the attribute "phrases".
 4. `Insert a phrase`: This option is denoted by the integer `2`.
    * The user inputs a phrase and the program inserts the related **information** to the dictionary.
 6. `Delete a phrase`: This option is denoted by the integer `3`.
    * The user inputs a phrase and the program **checks** for its existence. If it exists it deletes it, otherwise it returns.

### Example💭

Now let's run through an example, in order for us to understand what the program actually does. Let's say that we want to insert the phrase "πληροφορική". The phrase, is converted to its numerical form 996, where its subdivisions are 9+9+6 = 24 and 2+4=6. So now the information which contains both the phrase, the key and its subdivisions, is going to be inserted in the dictionary. Obviously if there's not a key with value 996 already in the dictionary, then a new object is created with key = 996.:

```json
"996": {
    "divisions": [
        24,
         6
    ],
    "phrases": [
        "πληροφορική"
    ]
}
```

Otherwise, the program just inserts the phrase in the object, under the attribute **phrases**:

```json
"996": {
    "divisions": [
        24,
         6
    ],
    "phrases": [
        "α' πρόβλεψη",
        "η β' εξακτύς",
        "πληροφορική"
    ]
}
```

### FutureGoals🔮

The main goal is to create a GUI application, so that anyone can experiment with the dictionary with more ease, without dealing with the hardships of the console application🙂.

### Contributions🫴

If you'd like to contribute, feel free to fork the repository and submit a pull request. I'd be really grateful to any contribution!
