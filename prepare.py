import csv
from pathlib import Path
import re
import string


def process_text(text):
    text = str(text).lower()
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text) 
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    text = re.sub(r'^b\s+', '', text)
    text = re.sub(
        f"[{re.escape(string.punctuation)}]", " ", text
    )
    text = " ".join(text.split())
    # words = text.split(" ")
    # new_words = []
    # for w in words:
    #     if ("token" not in w) or ("id" not in w):
    #         new_words.append(w)

    # text = " ".join(new_words)
    return text


with open('train.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line_count += 1
        Path("data/"+ row[1]).mkdir(parents=True, exist_ok=True)
        with open("data/"+ row[1] + '/file_' + row[0] + '_' + str(line_count) + '.txt', 'w') as f:
            f.write(process_text(row[2]))