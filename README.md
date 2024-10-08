# Lexarithmos

`Lexarithmos`, is a console-based Python program that allows users to convert Greek words and phrases (modern or ancient) into numbers and store them in a **JSON** dictionary. The program provides the ability to analyze and uncover connections between words through their numerical representations.

### Core idea💡

Although this idea may seem simple at first, the results are impressive! The project demonstrates how **mathematics** — and specifically numbers — define the **Greek** language. Every word, phrase, or even idea created within the Greek language can be numerically related to other concepts! To uncover these associations, one must be willing to question, think critically, and use their imagination. This creates an atmosphere of discovery throughout the process🙂.

### Features⚙️

 * `Phrase to number`: Convert any Greek phrase into its numerical equivalent using a specific letter-to-number mapping.
 * `Dictionary format`: Store phrases and their numerical forms in a JSON file, which updates after every insertion or deletion.
 * `Basic operations`: Perform key operations like addition, deletion, and search within the dictionary.

**NOTE: The letter-to-number map isn't arbitrary! It's based on a recent historical discovery at an archaeological site in Greece, adding an intriguing aspect to the project.**

### DataFormat📄

The phrases and their numerical values are stored in a **JSON** file located under the folder `code/Data/` with the name `numberFile.json`. Each entry in this dictionary has the following structure:

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

 * `key`: The **integer** representation of each phrase `sM`.
 * `divisions`: An **array** of integer subdivisions `dN` of the key.
 * `phrases`: An **array** of all phrases that correspond to the same key.
 * `N, M`: The integer **indices** defining the lengths of the arrays.

**NOTE: The subdivisions of a number `n` are the sums of its digits repeated, until a single-digit number is obtained (e.g., 996 → 9+9+6 = 24 → 2+4 = 6).**

### Usage🪛

The program offers the following operations, passed as arguments to the `resolve_number()` function in its field `userOption`:

```python
self.userOptions = {
    "search_by_key": 0,
    "search_by_phrase": 1,
    "insert_phrase": 2,
    "delete_phrase": 3
}
```

 1. `Search by key`: This option is denoted by the integer `0`. 
    * Input a key to retrieve all phrases associated with that key.
 2. `Search by phrase`: This option is denoted by the integer `1`.
    * Input a phrase to find the phrases associated with the same key.
 4. `Insert a phrase`: This option is denoted by the integer `2`.
    * Input a phrase to convert it into its numeric form and insert it into the JSON dictionary.
 6. `Delete a phrase`: This option is denoted by the integer `3`.
    * Input a phrase to delete it from the dictionary if it exists.

### Example💭

Let's say you want to insert the phrase `"πληροφορική"`. The program converts this phrase into its numerical form, `996`, and computes its subdivisions as `24`(9+9+6) and `6`(2+4). If 996 is not already in the dictionary, it creates a new entry:

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

If the key already exists, the phrase is added to the existing entry:

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

The main future goal is to develop a **GUI** version of the application to make it more user-friendly, allowing users to interact with the dictionary more easily without needing to use the command line🙂.

### Contributions🫴

Contributions are welcome! If you'd like to contribute, feel free to fork the repository and submit a pull request. I appreciate all forms of contributions!
