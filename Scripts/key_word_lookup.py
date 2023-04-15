import os
from Scripts.utilities import get_word_files, getText, tokenize, clean_keywords, get_country_year
from collections import Counter
from nltk import ngrams
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import json
import pandas as pd
from tqdm import tqdm

def get_ngrams(words):
    bi = [words[i:i + 2] for i in range(len(words) - 2 + 1)]
    tri = [words[i:i + 3] for i in range(len(words) - 3 + 1)]
    quad = [words[i:i + 4] for i in range(len(words) - 4 + 1)]
    return bi, tri, quad

def get_n_gram_counts(word_list, n_range=3, top_n=10):
    for nn in range(1, (n_range+1)):
        print(" ")
        print(f"Processing {nn} ...")
        print(" ")
        ngram_counts = Counter(ngrams(word_list, nn))
        print(ngram_counts.most_common(top_n))

# def get_CountVectorizer(type='CV'):
#     if type == "CV":
#         vect = CountVectorizer(ngram_range=(n, n), lowercase=False, vocabulary=vocab_list, max_features=len(vocab_list)*2)
#     else:
#         vect = TfidfVectorizer(ngram_range=(n, n), lowercase=False, vocabulary=vocab_list, max_features=len(vocab_list)*2)

def get_sdg_17_words(word_list, bi, tri, quad):
    # lex = open('../resources/lexicon.json')
    with open('../Resources/lexicon.json', 'r') as j:
        lex = json.loads(j.read())
    trade_words = get_key_gram_count(lex['Trade'], word_list, bi, tri, quad)
    finance_words = get_key_gram_count(lex['Finance'], word_list, bi, tri, quad)
    tech_words = get_key_gram_count(lex['Technology'], word_list, bi, tri, quad)
    sys_issues_words = get_key_gram_count(lex['Systemic Issues'], word_list, bi, tri, quad)
    cap_building_words = get_key_gram_count(lex['Capacity Building'], word_list, bi, tri, quad)
    return trade_words, finance_words, tech_words, sys_issues_words, cap_building_words

def get_key_gram_count(key_words, nvr_uni, nvr_bi, nvr_tri, nvr_quad):
    kw_unigrams = clean_keywords(key_words)
    kw_bigrams = [word.split() for word in kw_unigrams if len(word.split()) == 2]
    kw_trigrams = [word.split() for word in kw_unigrams if len(word.split()) == 3]
    kw_quadgrams = [word.split() for word in kw_unigrams if len(word.split()) == 4]
    uni_count = 0
    bi_count = 0
    tri_count = 0
    quad_count = 0
    for word in kw_unigrams:
        temp = nvr_uni.count(word)
        uni_count = uni_count + temp
    # print(f"There are a total of {uni_count} UNIGRAM MATCHES")
    for bigram in kw_bigrams:
        temp = nvr_bi.count(bigram)*2
        bi_count = bi_count + temp
    # print(f"There are a total of {bi_count} BIGRAM MATCHES")
    for trigram in kw_trigrams:
        temp = nvr_tri.count(trigram)*3
        tri_count = tri_count + temp
    # print(f"There are a total of {tri_count} TRIGRAM MATCHES")
    for quad in kw_quadgrams:
        temp = nvr_quad.count(quad)*4
        quad_count = quad_count + temp
    # print(f"There are a total of {tri_count} TRIGRAM MATCHES")
    return uni_count+bi_count+tri_count+quad_count

def get_top_keywords(n_range=4, top_n=15):
    files = get_word_files(os.getcwd())
    all_documents_word_list = []
    for file in tqdm(files):
        txt = getText(file)
        w_list = tokenize(txt, [], type="word")
        all_documents_word_list.extend(w_list)
    get_n_gram_counts(all_documents_word_list, n_range, top_n)

def run_analysis(output_path):
    files = get_word_files(os.getcwd())
    df_list = []
    for file in tqdm(files):
        print(f"Processing {file} ...")
        txt = getText(file)
        w_list = tokenize(txt, [], type="word")
        bi, tri, quad = get_ngrams(w_list)
        country, year = get_country_year(file)
        trade_words, finance_words, tech_words, sys_issues_words, cap_building_words = get_sdg_17_words(w_list, bi, tri, quad)
        df_list.append([country, year, len(w_list), trade_words, finance_words, tech_words, sys_issues_words, cap_building_words ])
    df = pd.DataFrame(df_list, columns=['country','year', 'nvp_17_word_count','trade_words','finance_words','tech_words', 'sys_issues_words', 'cap_building_words'])
    df['trade_word_perc'] = df['trade_words']/df['nvp_17_word_count']
    df['finance_word_perc'] = df['finance_words']/df['nvp_17_word_count']
    df['tech_word_perc'] = df['tech_words']/df['nvp_17_word_count']
    df['sys_issues_word_perc'] = df['sys_issues_words']/df['nvp_17_word_count']
    df['cap_building_word_perc'] = df['cap_building_words']/df['nvp_17_word_count']

    print(df.shape)
    print(df)
    df.to_csv(output_path + "/COUNTRY_RESULTS.csv")


if __name__ == "__main__":
    local_path = '/Users/bcard/projects/air/organize_chaos/Documents'
    os.chdir(local_path)
    output_path = '/Users/bcard/projects/air/organize_chaos/Output'
    run_analysis(output_path)
    get_top_keywords()