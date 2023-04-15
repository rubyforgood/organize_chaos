from pprint import pprint
from gensim import corpora, models
import os
from gensim.corpora.dictionary import Dictionary
import pyLDAvis
# import pyLDAvis.gensim_models
from Scripts.utilities import get_countries, getText, tokenize, get_word_files



def get_corpus_dict(files):
    list_of_document_words = []
    countries = get_countries(files)
    countries.extend(['develop','countri'])
    for file in files:
        temp = getText(file)
        word_list = tokenize(temp, countries, type="word")
        list_of_document_words.append(word_list)
    dict = Dictionary(list_of_document_words)
    corpus = [dict.doc2bow(text) for text in list_of_document_words]
    # Translate ID to a word
    # [[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]
    return corpus, dict

def topic_model(corpus, dict, n_topics=10):
    # gensim model
    lda_model = models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=dict,
                                                num_topics=n_topics,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=False)
    pprint(lda_model.print_topics())
    # doc_lda = lda_model[corpus]
    # pyLDAvis.enable_notebook()
    # vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dict)
    # vis


def run_topic_model():
    files = get_word_files(os.getcwd())
    # files = ["VNR_Azerbaijan_2021.docx", "VNR_Brazil_2017.docx"]
    corpus, dictionary = get_corpus_dict(files)
    model = topic_model(corpus, dictionary, n_topics=5)
    """
    SDG 17: Strength the means of implemention ($$) and revitalize the global partnership for sustainable development
    Expected Topics
    - International Trade
    - Remittances 
    - FDI (Foreign Direct Investment)
    - Official Development Assistance (ODA)
    - Internet 
    - Debt 
    - Gross National Income
    https://sdgs.un.org/goals/goal17
    """

if __name__ == "__main__":
    os.chdir('/Users/bcard/projects/nlp_vnr/Text')
    output_path = '/Users/bcard/projects/nlp_vnr/Output'
    run_topic_model()


# Questions
# Do I have enough data
# Can hyper-parameter tuning help?
# What other methods might work better?

# Try N topics
# Filter out common words using WordFreak
# Increase the number of passes
# Spacy rules (increasing within 5 words)
# ChatGBt - summarizing text
# Why & the How
