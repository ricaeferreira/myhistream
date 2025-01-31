#Core Pkgs
from textblob import TextBlob
import streamlit as st
st.set_page_config(page_title="Refe Web App", page_icon="🐸", layout="centered", initial_sidebar_state="collapsed" )

#NLP Pkgs
from textblob import TextBlob
import spacy
import neattext as nt

from deep_translator import GoogleTranslator

from collections import Counter
import re

def summarize_text(text, num_sentences=3):
    
    clean_text = re.sub('^a-zA-Z', ' ', text).lower()

    words = clean_text.split(' ')

    word_freq = Counter(words)

    sorted_words = sorted(word_freq, key=word_freq.get, reverse=True)

    top_words = sorted_words[:num_sentences]

    summary = ' '.join(top_words)

    return summary


@st.cache_data
def text_analyzer(text):
    
    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)

    allData = [('"Token":{},\n"Lemma":{}'.format(token.text,token.lemma_)) for token in doc]
    
    return allData

#Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from wordcloud import WordCloud


def main():
    """NLP App with Streamlit"""

    title_template = """
    <div style="background-color:blue;padding:8px;">
    <h1 style="color:cyan">NLP Web App</h1>
    </div>
    """  
    
    #st.title("NLPiffy with Streamlit")
    st.markdown(title_template, unsafe_allow_html=True)

    subheader_template = """
    <div style="background-color:cyan;padding:8px;">
    <h3 style="color:blue">Powered by streamlit</h3>
    </div>
    """
    st.markdown(subheader_template, unsafe_allow_html=True)

    st.sidebar.image("nlp.jpg", use_container_width=True)

    activity = ["Text Analysis", "Translation", "Sentiment Analysis", "About"]
    choice = st.sidebar.selectbox("Menu", activity)

    if choice == "Text Analysis":
        st. subheader ("Text Analysis")
        st.write("")

        raw_text = st.text_area("Write something","Hello Everybody",height=300)

        if st.button("Analyze"):
            if len(raw_text) == 0:
                st.warning("Please enter a text")
            else:  
                blob = TextBlob(raw_text)
                st.write("Basic Functions")

                col1, col2 = st.columns(2)

                with col1:
                    with st.expander("Basic Info"):
                        st.info("Text Stats")
                        word_desc = nt.TextFrame(raw_text).word_stats()
                        result_desc = {
                            "Length of text":word_desc['Length of Text'],
                            "Num of vowels":word_desc['Num of Vowels'],
                            "Num of consonants":word_desc['Num of Consonants'],
                            "Num of stopwords":word_desc['Num of Stopwords']
                        }
                        
                        st.write(result_desc)

                    with st.expander("Stopwords"):
                        st.success("Stop words list")
                        stop_w = nt.TextExtractor(raw_text).extract_stopwords()
                        st.error(stop_w)

                
                with col2:
                    with st.expander("Processed Info"):
                        st.success("Stopwords Excluded Text")
                        processed_text = str(nt.TextFrame(raw_text).remove_stopwords())
                        st.write(processed_text)
                    
                    with st.expander("Plot Wordcloud"):
                        wordcloud = WordCloud().generate(processed_text)
                        fig = plt.figure(1,figsize=(20,10))
                        plt.imshow(wordcloud,interpolation='bilinear')
                        plt.axis('off')
                        st.pyplot(fig)



                st.write("")
                st.write("")
                st.info("Advanced Features")


                col3, col4 = st.columns(2)

                with col3:
                    with st.expander("Tokens & Lemmas"):
                        st.write("T&K")
                        processed_text_mid =  str(nt.TextFrame(raw_text).remove_stopwords())
                        processed_text_mid =  str(nt.TextFrame(processed_text_mid).remove_puncts())
                        processed_text_fin =  str(nt.TextFrame(processed_text_mid).remove_special_characters())

                        tandl = text_analyzer(processed_text_fin)
                        st.json(tandl)
                
                with col4:
                    with st.expander("Summarize"):
                        st.success("Summarize")
                        summary = summarize_text(raw_text)
                        st.success(summary)

    if choice == "Translation":
        st. subheader ("Translation" )
        st.write("")
        st.write("")

        raw_text = st.text_area("Original Text", "Write something to be translated",height=300)
        if len(raw_text) < 3:
            st.warning("Please provide a text with at least 3 characters")  
        else:
            target_lan = st.selectbox("Select Language", ["German", "Spanish", "French", "Italian"])
            if target_lan == "German":
                target_lan = "de"
            elif target_lan == "Spanish":
                target_lan = "es"
            elif target_lan == "French":
                target_lan = "fr" 
            elif target_lan == "Italian":
                target_lan = "it"

            if st.button("Translate"):
                translator = GoogleTranslator(source='auto', target=target_lan)
                translated_text = translator.translate(raw_text)
                st.write(translated_text)
                



    if choice == "Sentiment Analysis":
        st. subheader ("Sentiment Analysis")
        st.write("")
        st.write("")

        raw_text = st.text_area("Texto to analyze","Enter text here...",height=300)
        if st.button("Analyze"):
            if len(raw_text) == 0:
                st.warning("Please enter a text")
            else:
                blob = TextBlob(raw_text)
                st.info("Sentiment Analysis")
                st.write(blob.sentiment)
                st.write("")

    if choice == "About":
        st. subheader ("About" )
        st.write("")

        st.markdown("""
                    ### NLP App made with Streamlit
                    for info:
                    
                    - [Streamlit](https://www.streamlit.io/)
                    """)

if __name__ == '__main__':
    main()



