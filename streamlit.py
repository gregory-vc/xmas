import streamlit as st
import os.path
import pathlib
import tika
import joblib
import pymorphy2
import nltk
import string
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from tika import parser

st.write("""
# File Picker
""")

tika.initVM()

stop_words = set(stopwords.words('russian')) # множество стоп слов

morph = pymorphy2.MorphAnalyzer() # для постановки слова в начальную форму


def lemmatize_words(text):
    '''Функция для лемматизации отдельных слов.'''
    final_text = []
    for i in text.lower().split():
        if i not in stop_words:
            parse = morph.parse(i)[0]
            if ('Abbr' not in parse.tag):
                final_text.append(parse.normal_form)               
    return " ".join(final_text)

def text_preprocessing(text):
    data = text

    # удаляем пунктуацию
    data['content_punct'] = data['content'].translate(str.maketrans('', '', string.punctuation))
    # Приводим к начальной форме
    data['content_punct_lemm'] = lemmatize_words(data['content_punct'])
    
    return data

uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = parser.from_buffer(bytes_data)
    

    lr = joblib.load("LR_trained_classifier.joblib")
    tf = joblib.load("tf.joblib")

    sample_text = text_preprocessing(data)
    # Process the text in the same way you did when you trained it!
    sample_vec = tf.transform(sample_text)

    pr = lr.predict(sample_vec)
    pr1 = lr.predict_proba(sample_vec)


    predict = st.text_area("Predict", pr, key="predict")
    st.json(data)

upload_state = st.text_area("Upload State", "", key="upload_state")


def upload():
    if uploaded_file is None:
        st.session_state["upload_state"] = "Upload a file first!"
    else:
        data = uploaded_file.getvalue().decode('utf-8')
        parent_path = pathlib.Path(__file__).parent.parent.resolve()
        save_path = os.path.join(parent_path, "data")
        complete_name = os.path.join(save_path, uploaded_file.name)
        destination_file = open(complete_name, "w")
        destination_file.write(data)
        destination_file.close()
        st.session_state["upload_state"] = "Saved " + \
            complete_name + " successfully!"


st.button("Upload file to Sandbox", on_click=upload)
