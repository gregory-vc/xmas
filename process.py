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
    words = text.split(" ")
    new_words = []
    for w in words:
        if ("token" not in w) or ("id" not in w):
            new_words.append(w)

    text = " ".join(new_words)
    return text


print(process_text("Прямые трансляции волейбольных матчей на сегодня 16ф января Мужчины. Чемпионат России. Суперлига. Тринадцатый тур. Расписание тура 16 00 Нефтяник Оренбург Динамо Москва tokentokenoid tokentokenoid 16 00 Урал Уфа Белогорье Белгород tokentokenoid tokentokenoid Время начала всех матчей указано московское."))