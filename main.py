from tqdm import tqdm
from os.path import join, isfile, isdir

import os
import json
import sys

[_, DOCUMENTS] = sys.argv
MISC_FILE_EXT = [
    "xlsx",
    "html",
    # "pdf",
    "png",
    # "docx",
    "jpg",
    "jpeg",
    "zip",
    "pptx",
    "xls",
    "pages",
    # "csv",
    "m4a",
    # MAYBE GET TXT
    "txt",
    "conf",
    "mp4",
    "doc",
]

import sys

sys.path.append("./Scripts")
import os
from os.path import isfile, join, isdir
import docx
from collections import Counter
from nltk import ngrams
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import json
import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords
from collections import Counter
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()


def get_ngrams(words):
    bi = [words[i : i + 2] for i in range(len(words) - 2 + 1)]
    tri = [words[i : i + 3] for i in range(len(words) - 3 + 1)]
    quad = [words[i : i + 4] for i in range(len(words) - 4 + 1)]
    return bi, tri, quad


def get_n_gram_counts(word_list, n_range=3, top_n=10):
    for nn in range(1, (n_range + 1)):
        print(" ")
        print(f"Processing {nn} ...")
        print(" ")
        ngram_counts = Counter(ngrams(word_list, nn))
        print(ngram_counts.most_common(top_n))


def find_cat_words(word_list, bi, tri, quad):
    # lex = open('../resources/lexicon.json')
    with open(
        "C:/Users/ramosv/Desktop/MileHighHack/organize_chaos/Resources/lexicon.json",
        "r",
    ) as j:
        lex = json.loads(j.read())

    motel_words = get_key_gram_count(lex["Motel"], word_list, bi, tri, quad)
    bso_words = get_key_gram_count(
        lex["Business Support Office"], word_list, bi, tri, quad
    )
    edo_words = get_key_gram_count(
        lex["Equity Development Office"], word_list, bi, tri, quad
    )
    rso_issues_words = get_key_gram_count(
        lex["Resident Support Office"], word_list, bi, tri, quad
    )
    comm_words = get_key_gram_count(lex["Communication"], word_list, bi, tri, quad)
    admin_words = get_key_gram_count(lex["Admin"], word_list, bi, tri, quad)
    # thefax_words = get_key_gram_count(lex['The Fax'], word_list, bi, tri, quad)
    return motel_words, bso_words, edo_words, rso_issues_words, comm_words, admin_words


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
        temp = nvr_bi.count(bigram) * 2
        bi_count = bi_count + temp
    # print(f"There are a total of {bi_count} BIGRAM MATCHES")
    for trigram in kw_trigrams:
        temp = nvr_tri.count(trigram) * 3
        tri_count = tri_count + temp
    # print(f"There are a total of {tri_count} TRIGRAM MATCHES")
    for quad in kw_quadgrams:
        temp = nvr_quad.count(quad) * 4
        quad_count = quad_count + temp
    # print(f"There are a total of {tri_count} TRIGRAM MATCHES")
    return uni_count + bi_count + tri_count + quad_count


def classify_on_model(output_path, files):
    # files = get_word_files(os.getcwd(),[])
    files = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(os.getcwd())
        for f in filenames
        if f in files
    ]
    df_list = []
    for file in tqdm(files):
        print(f"Processing {file} ...")
        txt = getText(file)
        w_list = tokenize(txt, [], type="word")
        bi, tri, quad = get_ngrams(w_list)
        (
            motel_words,
            bso_words,
            edo_words,
            rso_issues_words,
            comm_words,
            admin_words,
        ) = find_cat_words(w_list, bi, tri, quad)
        df_list.append(
            [
                file,
                len(w_list),
                motel_words,
                bso_words,
                edo_words,
                rso_issues_words,
                comm_words,
                admin_words,
            ]
        )
    df = pd.DataFrame(
        df_list,
        columns=[
            "Filename",
            "doc_word_count",
            "motel_words",
            "bso_words",
            "edo_words",
            "rso_issues_words",
            "comm_words",
            "admin_words",
        ],
    )
    # df['motel_words_perc'] = df['motel_words']/df['doc_word_count']
    # df['bso_words_perc'] = df['bso_words']/df['doc_word_count']
    # df['edo_words_perc'] = df['edo_words']/df['doc_word_count']
    # df['rso_issues_perc'] = df['rso_issues_words']/df['doc_word_count']
    # df['comm_words_perc'] = df['comm_words']/df['doc_word_count']
    # df['admin_perc'] = df['admin_words']/df['doc_word_count']
    # df['thefax_perc'] = df['thefax_words']/df['doc_word_count']

    print(df.shape)
    print(df)
    df.to_csv(output_path + "/RESULTS.csv")
    folderList = []
    for index, row in df.iterrows():
        # print(row['motel_words'],row['bso_words'],row['edo_words'], row['rso_issues_words'], row['comm_words'],row['admin_words'])
        isMax = max(
            row["motel_words"],
            row["bso_words"],
            row["edo_words"],
            row["rso_issues_words"],
            row["comm_words"],
            row["admin_words"],
        )
        # folder = ""
        if isMax == 0:
            folder = "misc"
        elif isMax == row["motel_words"]:
            folder = "motel"
        elif isMax == row["bso_words"]:
            folder = "bso"
        elif isMax == row["rso_issues_words"]:
            folder = "rso"
        elif isMax == row["comm_words"]:
            folder = "comm"
        elif isMax == row["admin_words"]:
            folder = "admin"
        elif isMax == row["edo_words"]:
            folder = "edo"
        else:
            breakpoint()

        folderList.append([row["Filename"], folder])
    return dict(folderList)
    # pd.DataFrame(folderList, columns=['Filename','Folder'])
    # finalOutput.to_csv(output_path + "/FinalOutput.csv")


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return "\n".join(fullText)


def filter_wordlist(word_list):
    return [word.lower() for word in word_list]


def clean_keywords(word_list):
    word_list = filter_wordlist(word_list)
    cleaned_keywords = stemming_lemming(word_list)
    return cleaned_keywords


def tokenize(text, exclude_words, type="word"):
    for spec_char in """!()-[]{};:'"\,<>/.?@#$%^&*_~""":
        text = text.replace(spec_char, "")
    exclude_words.extend(["also"])
    if type != "\n":
        text = text.replace("\n", "")
    if type == "word":
        lang_list = text.split()
        lang_list = filter_wordlist(lang_list)
        lang_list = stemming_lemming(lang_list)
        final_list = [word for word in lang_list if word not in exclude_words]
    elif type == "sentence":
        final_list = text.split(".")
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
    df = pd.DataFrame(vocab_d.items(), columns=["Word", "Count"])
    df = df.sort_values(by="Count", ascending=False)
    df = df.head(n)
    print(df)
    df.to_csv(f"{output}/{file_name}_top_{n}_word_list.csv")


def run_analysis():
    output_path = "C:/Users/ramosv/Desktop/MileHighHack/organize_chaos/Output"
    local_path = DOCUMENTS
    os.chdir(local_path)
    files = [
        os.path.join(dir_path, f)
        for dir_path, dir_names, filenames in os.walk(os.getcwd())
        for f in filenames
    ]

    matched_files_level_1 = []
    unmatched_files_level_1 = []

    # Filter by file name
    for file in tqdm(files):
        classify_on_file_name(file, matched_files_level_1, unmatched_files_level_1)

    matched_files_level_2 = []
    unmatched_files_level_2 = []
    # Filter by extension
    for file in tqdm(unmatched_files_level_1):
        classify_on_ext(files, matched_files_level_2, unmatched_files_level_2)

    matched_files_level_3 = classify_on_model(output_path, unmatched_files_level_2)

    all_matched_files = (
        matched_files_level_1 + matched_files_level_2 + matched_files_level_3
    )

    print(all_matched_files)


def classify_on_file_name(file, unmatched, matched):
    lexicon_dict: dict = readDir()

    # Boolean to tell us whether we found a match
    found_match = False
    # Assign a dictionary to the file we are sorting
    sorted_file_dict = {"file": file}

    # For every category...
    for category in lexicon_dict.keys():
        # For every keyword in out lexicon array for the category...
        for keyword in lexicon_dict[category]:
            # If the keyword is in the file name, we have a match
            if keyword.lower() in file.lower():
                found_match = True
                # If the category key isn't in the matches, then assign it
                if not "folder" in sorted_file_dict:
                    sorted_file_dict["folder"] = category
            # If no match, don't do shit
            else:
                continue

    if found_match:
        matched.append(sorted_file_dict)
    else:
        unmatched.append(file)


def classify_on_ext(file, unmatched, matched):
    if "." in file:
        extension = file.split(".").pop()
        if extension in MISC_FILE_EXT:
            matched.append({"file": file, "folder": "misc"})
        else:
            unmatched.append(file)
    else:
        unmatched.append(file)


def readDir():
    with open(
        "C:/Users/ramosv/Desktop/MileHighHack/organize_chaos/Resources/lexicon.json",
        "r",
    ) as j:
        lex = json.loads(j.read())
    return lex


if "__main__" == __name__:
    run_analysis()
