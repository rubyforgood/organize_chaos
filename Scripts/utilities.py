import pandas as pd
import docx
import os
from os import listdir
from os.path import isfile, join
import nltk
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()

# One Time Downloads
# nltk.download('words')
# nltk.download('vader_lexicon')

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def get_country_year(file):
    temp = file.split("_")
    country = temp[1].lower()
    year = temp[2]
    year = year.replace(".docx", "")
    return country, year

def filter_wordlist(word_list):
    return [word.lower() for word in word_list if word not in stopwords.words('english') and len(word) > 3 and word not in ['tax','VAT','ODA', 'SDG', 'aid', 'CSO', 'FDI']]

def clean_keywords(word_list):
    word_list = filter_wordlist(word_list)
    cleaned_keywords = stemming_lemming(word_list)
    return cleaned_keywords

def tokenize(text, exclude_words, type="word"):
    for spec_char in '''!()-[]{};:'"\,<>/.?@#$%^&*_~''':
        text = text.replace(spec_char, "")
    exclude_words.extend(["also"])
    # exclude_words.extend(["countri", "develop", "nation", "intern", "national", "sustain", "global", "sdg", "implement", "govern", "percent", "public", "cooper", "darussalam", "brunei", "herzegovina", "danish", "czech"])
    # If this becomes too slow, try nltk tokenizer
    if type != '\n':
        text = text.replace('\n', "")
    if type == "word":
        lang_list = text.split()
        lang_list = filter_wordlist(lang_list)
        lang_list = stemming_lemming(lang_list)
        final_list = [word for word in lang_list if word not in exclude_words]
    elif type == "sentence":
        # final_list = []
        final_list = text.split(".")
        # for sentence in lang_list:
        #     word_list = sentence.split()
        #     lang_list = filter_wordlist(word_list)
        #     lang_list = stemming_lemming(lang_list)
        #     lang_list = [word for word in lang_list if word not in exclude_words]
        #     final_list.extend(lang_list)
        # [word for sent in lang_list for word in sent]
    # print(f"read in {len(word_list)} words")
    return final_list

def stemming_lemming(word_list, stem=True):
    if stem:
        words = [porter_stemmer.stem(word) for word in word_list]
    else:
        words = [wordnet_lemmatizer.lemmatize(word) for word in word_list]
    return words


def get_top_n_words(file_name, word_list, output, n=10):
    vocab_d = {}
    filtered_words = filter_wordlist(word_list)
    for word in filtered_words:
        if word not in vocab_d:
            vocab_d[word] = 1
        else:
            vocab_d[word] += 1
    df = pd.DataFrame(vocab_d.items(), columns=['Word', 'Count'])
    df = df.sort_values(by='Count', ascending=False)
    df = df.head(n)
    print(df)
    df.to_csv(f"{output}/{file_name}_top_{n}_word_list.csv")

def get_word_files(path):
    files = [f for f in listdir(path) if isfile(join(path, f)) and ".docx" in f]
    return files

def get_countries(files_list):
    countries_list = []
    for file in files_list:
        temp = file.split("_")
        country = temp[1].lower()
        countries_list.append(country)
    return countries_list

def sentiment_analysis(sentence_list):
    sid_obj = SentimentIntensityAnalyzer()
    for sentence in sentence_list:
        sentiment_dict = sid_obj.polarity_scores(sentence)
        results = sentiment_dict
        print("Overall sentiment dictionary is : ", results)
        # EXAMPLE -- FULL AZERBAJIAN REPORT TEXT
        # Overall sentiment dictionary is :  {'neg': 0.023, 'neu': 0.906, 'pos': 0.072, 'compound': 0.999}
        return results

def create_word_cloud(file_name, word_list, output):
    # convert it to dictionary with values and its occurences
    filtered_words = filter_wordlist(word_list)
    word_could_dict = Counter(filtered_words)
    wordcloud = WordCloud(width=1000, height=500).generate_from_frequencies(word_could_dict)
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    # plt.show()
    plt.savefig(f'{output}/{file_name}_word_cloud.png', bbox_inches='tight')
    plt.close()




def run_analysis(output_path):
    files = get_word_files(os.getcwd())
    df_list = []
    for file in files:
    # for file in ["VNR_Azerbaijan_2021.docx"]:
        txt = getText(file)
        #### MOST COMMON WORDS
        # word_list = tokenize(txt, type="word")
        # get_top_n_words(file, word_list, output_path, n=5)
        # print(len(txt))

        #### SENTIMENT ANALYSIS
        country, year = get_country_year(file)
        sent_list = tokenize(txt, [], type="sentence")

        results = sentiment_analysis(sent_list)
        df_list.append([country, year, results])
    df = pd.DataFrame(df_list, columns=['country', 'year', 'results'])
    df.to_csv("Sentiment_Analysis_by_Country")

        #### WORD CLOUD
        # word_list = tokenize(txt, type="word")
        # create_word_cloud(file, word_list, output_path)
