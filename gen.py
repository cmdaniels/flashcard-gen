from openai import OpenAI
from wiktionaryparser import WiktionaryParser
from dotenv import load_dotenv
import os, re, sys

load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
parser = WiktionaryParser()

def main():
    user_lang = input("Target Language: ").lower()
    parser.set_default_language(user_lang)

    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = 'flashcards.tsv'

    while True:
        user_input = input("Enter new word: ")

        if user_input.lower() == 'exit':
            break

        pos, definition, etymology, ipa = wiki_lookup(user_input)
        if pos is None:
            continue

        # Call the OpenAI GPT API with the user input
        response = generate_example(user_input, definition, user_lang)
        example = response.choices[0].message.content.replace('"', '').strip()
        example = re.sub(r'\([^)]*\)', '', example).strip()

        # Print the flashcard
        print('-' * 50)
        print(f"Word: {user_input}")
        print(f"Definition: {definition}")
        print(f"Part of Speech: {pos}")
        print(f"Etymology: {etymology}")
        print(f"IPA: {ipa}")
        print(f"Example: {example}")
        print('-' * 50)
        
        with open(output, 'a') as f:
            f.write(f'{user_input}\t{pos}\t{definition}\t{example}\t{etymology}\t{ipa}\n')

def wiki_lookup(word):
    resp = parser.fetch(word)
    
    if len(resp[0]['definitions']) == 0:
        print("No results found.")
        return None, None, None, None

    # PART OF SPEECH
    if len(resp) == 1:
        pos = resp[0]['definitions'][0]['partOfSpeech']
        entry_idx = 0
    else:
        for i, entry in enumerate(resp):
            print(f"{i}: {entry['definitions'][0]['partOfSpeech']} - {entry['definitions'][0]['text'][1:]}")
        entry_idx = int(input("Select part of speech: "))
        pos = resp[entry_idx]['definitions'][0]['partOfSpeech']

    # DEFINITION
    if len(resp[entry_idx]['definitions'][0]['text'][1:]) == 1:
        definition = resp[0]['definitions'][0]['text'][1:][0]
    else:
        for i, definition in enumerate(resp[entry_idx]['definitions'][0]['text'][1:]):
            print(f"{i}: {definition}")
        definition_idx = int(input("Select definition: "))
        definition = resp[entry_idx]['definitions'][0]['text'][1:][definition_idx]

    # ETYMOLOGY
    etymology = resp[entry_idx]['etymology'].strip()
    etymology = ''.join(c for c in etymology if c.isprintable())

    # IPA
    ipa = resp[entry_idx]['pronunciations']['text']
    filtered_ipa = list(filter(lambda x: 'IPA' in x, ipa))

    if len(filtered_ipa) == 1:
        ipa = filtered_ipa[0]
    elif len(filtered_ipa) == 0:
        ipa = ''
    else:
        for i, key in enumerate(filtered_ipa):
            print(f"{i}: {key}")
        ipa_idx = int(input("Select IPA: "))
        ipa = filtered_ipa[ipa_idx]

    ipa = ipa.replace('IPA: ', '').strip()
    
    return pos, definition, etymology, ipa

def generate_example(word, definition, lang):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # gpt-4-1106-preview ($0.01 / 1K) or gpt-3.5-turbo ($0.001 / 1K)
        messages=[
            {"role": "system", "content": f'Give an example sentence in {lang} for the word and definition I provide without explanation.'},
            {"role": "user", "content": f'"{word}" meaning "{definition}"'}
        ],
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response

if __name__ == "__main__":
    main()
