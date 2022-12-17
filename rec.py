import joblib
import re
import string
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

nb_saved = joblib.load("vk_nb.joblib")
vec_saved = joblib.load("vk_vec.joblib")

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


import csv
from pathlib import Path


categories = [
    "athletics",
    "autosport",
    "basketball",
    "boardgames",
    "esport",
    "extreme",
    "football",
    "hockey",
    "martial_arts",
    "motosport",
    "tennis",
    "volleyball",
    "winter_sport"
]

d = {}
with open('test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        

        clean_sample_text = process_text([row[1]])
        sample_vec = vec_saved.transform([clean_sample_text])
        pr = nb_saved.predict(sample_vec)
        pr1 = nb_saved.predict_proba(sample_vec)
        score = 0

        for k in pr1:
            i = 0
            for v in k:
                if categories[i] == pr[0]:
                    score = round(v, 4)
                i += 1
        

        if row[0] in d:
            dd = d[row[0]]
            if pr[0] in dd:
                sc = d[row[0]][pr[0]]["score"]
                ct = d[row[0]][pr[0]]["count"]
                d[row[0]][pr[0]]["score"] += score
                d[row[0]][pr[0]]["count"] += 1
                d[row[0]][pr[0]]["result"] = round(sc/ct, 4)
                d[row[0]][pr[0]]["text"].append(row[1])
            else:
                d[row[0]][pr[0]] = {"result": score, "count": 1, "score": score, "text": [row[1]]}
        else:
            d[row[0]] = {pr[0]: {"result": score, "count": 1, "score": score, "text": [row[1]]}}

import pickle

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

save_object(d, "d.pkl")