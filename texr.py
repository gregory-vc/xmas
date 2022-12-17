import joblib
import re
import string

import numpy as np
import pandas as pd

from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, classification_report
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.naive_bayes import MultinomialNB


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

# news_group_data = fetch_20newsgroups(
#     subset="all", remove=("headers", "footers", "quotes"), categories=categories
# )

data = load_files(r"data/", categories=categories)


df = pd.DataFrame(
    dict(
        text=data["data"],
        target=data["target"]
    )
)
df["target"] = df.target.map(lambda x: categories[x])


def process_text(text):
    text = str(text).lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text) 
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    text = re.sub(r'^b\s+', '', text)
    text = re.sub(
        f"[{re.escape(string.punctuation)}]", " ", text
    )
    text = " ".join(text.split())
    return text

df["clean_text"] = df.text.map(process_text)

df_train, df_test = train_test_split(df, stratify=df.target)

vec = CountVectorizer(
    ngram_range=(1, 3), 
    stop_words="english",
)

X_train = vec.fit_transform(df_train.clean_text)
X_test = vec.transform(df_test.clean_text)

y_train = df_train.target
y_test = df_test.target

nb = MultinomialNB()
nb.fit(X_train, y_train)

preds = nb.predict(X_test)
print(accuracy_score(y_test, preds))

joblib.dump(nb, "vk_nb.joblib")
joblib.dump(vec, "vk_vec.joblib")


nb_saved = joblib.load("vk_nb.joblib")
vec_saved = joblib.load("vk_vec.joblib")


sample_text = ["стественное восстановление после тяжелой тренировки занимает 72 часа. С криокамерой 24 часа. Быстрее в 3 раза из интервью крио физиотерапевта на ютуб канале Khamzat Chtokenoid Заход в криокамеру с температурой минус 87 С равноценен 20 25 минутам восстановления в ледяной ванне. Криокамера ускоряет твое восстановление на 300. При естественном восстановлении организму после тяжелой тренировки требуется обычно 72 часа. Криокамера даст вам полное восстановление за 24 часа нвк"]
# Process the text in the same way you did when you trained it!
clean_sample_text = process_text(sample_text)
sample_vec = vec_saved.transform(sample_text)
y_pred2 = nb_saved.predict(sample_vec)

print(y_pred2)
