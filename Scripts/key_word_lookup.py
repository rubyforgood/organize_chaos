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

def find_cat_words(word_list, bi, tri, quad):
    # lex = open('../resources/lexicon.json')
    with open('../Resources/lexicon.json', 'r') as j:
        lex = json.loads(j.read())

    motel_words = get_key_gram_count(lex['Motels Work'], word_list, bi, tri, quad)
    bso_words = get_key_gram_count(lex['Business Support Office'], word_list, bi, tri, quad)
    edo_words = get_key_gram_count(lex['Equity Development Office'], word_list, bi, tri, quad)
    rso_issues_words = get_key_gram_count(lex['Resident Support Office"'], word_list, bi, tri, quad)
    comm_words = get_key_gram_count(lex['Communication'], word_list, bi, tri, quad)
    admin_words = get_key_gram_count(lex['Admin'], word_list, bi, tri, quad)
    thefax_words = get_key_gram_count(lex['The Fax'], word_list, bi, tri, quad)
    return motel_words, bso_words, edo_words, rso_issues_words, comm_words, admin_words, thefax_words

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
        motel_words, bso_words, edo_words, rso_issues_words, comm_words, admin_words, thefax_words= find_cat_words(w_list, bi, tri, quad)
        df_list.append([len(w_list), motel_words, bso_words, edo_words, rso_issues_words, comm_words, admin_words, thefax_words])
    df = pd.DataFrame(df_list, columns=['doc_word_count','motel_words','bso_words','edo_words', 'rso_issues_words', 'comm_words', 'admin_words', 'thefax_words'])
    df['motel_words_perc'] = df['motel_words']/df['doc_word_count']
    df['bso_words_perc'] = df['finance_words']/df['doc_word_count']
    df['edo_words_perc'] = df['tech_words']/df['doc_word_count']
    df['rso_issues_perc'] = df['rso_issues_words']/df['doc_word_count']
    df['comm_words_perc'] = df['comm_words']/df['doc_word_count']
    df['admin_perc'] = df['admin_words']/df['doc_word_count']
    df['thefax_perc'] = df['thefax_words']/df['doc_word_count']

    print(df.shape)
    print(df)
    df.to_csv(output_path + "/RESULTS.csv")


if __name__ == "__main__":
    local_path = '/Users/bcard/projects/air/organize_chaos/Documents'
    os.chdir(local_path)
    output_path = '/Users/bcard/projects/air/organize_chaos/Output'
    run_analysis(output_path)
    get_top_keywords()