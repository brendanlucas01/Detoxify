import streamlit as st
import time
import numpy as np
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import speech_recognition as sr
from pydub import AudioSegment
import os

nltk.download('punkt')
nltk.download('stopwords')
st.set_page_config(page_title="Detoxify", page_icon="🤝")

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model-etc.pkl','rb'))

ps = PorterStemmer()

def recognise_audio(audio):
    #Initiаlize  reсоgnizer  сlаss  (fоr  reсоgnizing  the  sрeeсh)
    r = sr.Recognizer()

    if (audio.type == 'audio/mpeg'):
        # convert mp3 file to wav file
        sound = AudioSegment.from_mp3(audio.name)
        audio = "{}.wav".format(audio.id)
        sound.export(audio, format="wav")

    with sr.AudioFile(audio) as source:
        #r.adjust_for_ambient_noise(source)
        audio_text = r.listen(source)
    try:
        # using google speech recognition
        text = r.recognize_google(audio_text)
        #text = r.recognize_google(audio_text, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")
        print('Converting audio transcripts into text ...')
        print(text)
        st.write(text)
    except:
        print('Sorry.. run again...')
    return text
    #return "sorry"

def transform_text(text):
    
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


st.markdown("# Let's detect Hate/Offensive Speech")
st.markdown(" <br/> ",True)
st.markdown("### _Input your tweet/sentence here :_")
#sentence = st.text_area("")
audio_file = st.file_uploader("Upload Images", type=["wav","mp3","mp4"])

st.write(audio_file)


# if audio_file is not None:

#     audio_file_name = audio_file.name

if st.button("Detect"):
    #1. preprocess
    sentence = recognise_audio(audio_file)
    transform_hate = transform_text(sentence)
    print(transform_hate)
    #2. Vectorize
    vector_input = tfidf.transform([transform_hate])
    print(vector_input)
    #3. Predict
    output = model.predict(vector_input)[0]

    #4. Display

    if output == 0:
        st.header("Hate Speech")
    elif output==1:
        st.header("Offensive Language")
    else :
        st.header("Good Speech")

# if st.button("Predict"):
#     if sentence != "":
#         output = predict_mail(sentence)
#         if output == 1:
#             st.markdown('### It\'s a SPAM Email')
#         else:
#             st.markdown('### It\'s NOT a SPAM Email')

st.markdown(""" 
<br/><br/>
<p align="center"> Developed with ❤ by Brendan, Candida & Aditya</p>

""", True)
