import chardet
import os
import json


DIR_PATH = os.path.dirname(os.path.abspath(__name__))
JSON_FILES = [i for i in os.listdir(DIR_PATH) if i.endswith("json")]


def determine_encoding(data):
    return chardet.detect(data)["encoding"]


def get_descrtiption_items_from_json(json_dict):
    return json_dict["rss"]["channel"]["items"]


def get_text_from_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
        decoded_data = data.decode(determine_encoding(data))
        items = [news["description"] for news in get_descrtiption_items_from_json(json.loads(decoded_data))]

        return " ".join(items)


def get_words_longer(text, word_len):
    res = {}

    for word in text.replace("\n", "").split():
        if len(word) > word_len:
            if word in res:
                res[word] += 1
            else:
                res[word] = 1

    return res


def print_top_words(words, limit):
    for key in sorted(words, key=words.get, reverse=True)[:limit]:
        print(key, words[key])


def concat_text_from_files(files):
    text = ""

    for file in files:
        text += get_text_from_file(file).lower()

    return text


if __name__ == "__main__":
    print_top_words(get_words_longer(concat_text_from_files(JSON_FILES), 6), 10)
