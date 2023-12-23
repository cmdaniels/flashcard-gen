# Flashcard Generator
`gen.py` is a Python script that generates flashcards complete with example sentences, etymology, and pronunciation keys for given words in any language. The resulting TSV file can be imported into Anki or any other flashcard software that supports TSV imports.

## Dependencies
- openai
- wiktionaryparser
- python-dotenv

## Environment Variables
You need to set the `OPENAI_API_KEY` environment variable in a `.env` file in the same directory as `gen.py`.

## Functions
- `main()`: The main function that runs when the script is executed. It prompts the user for new words and disambiguates which definition they prefer.
- `wiki_lookup(word)`: This function takes a word as input and returns its part of speech, definition, etymology, and IPA pronunciation by parsing the response from the Wiktionary API.
- `generate_example(word, definition, lang)`: This function takes a word, its definition, and a language as input. It sends a request to the OpenAI API to generate an example sentence for the given word and definition in the specified language.

## Usage
To run the script, use the following command:

```bash
python3 gen.py [output_filepath]
```

Please note that the script is currently set to run the main() function when executed. You may need to modify the script to suit your specific needs.

## Example
```
$ python3 gen.py
Target Language: Finnish
Enter new word: pannukakku
0: a thick (~ 1-2 cm, 1/2–3/4 in) pancake baked in oven, eaten as dessert and often served with whipped cream and/or jam
1: (broadly) pancake
2: (idiomatic) failure, fiasco
Select definition: 2
--------------------------------------------------
Word: pannukakku
Definition: (idiomatic) failure, fiasco
Part of Speech: noun
Etymology: pannu + kakku; calque of Swedish pannkaka (“pancake”) (both words of which, panna and kaka, are furthermore related to the Finnish counterparts). The figurative sense "failure, fiasco" (which is also found in Swedish) may refer to how a cake that fails to rise in the oven stays flat like a pancake.
IPA: /ˈpɑnːuˌkɑkːu/, [ˈpɑ̝nːuˌkɑ̝kːu]
Example: Koko projekti oli yksi suuri pannukakku.
--------------------------------------------------
Enter new word:
```