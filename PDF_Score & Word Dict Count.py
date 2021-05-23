import textract
import os
import re
from nltk.corpus import words
from tqdm import tqdm


# Binary search
def binary_search(arr, x):
    if not arr:  # list is empty
        return False

    mid = len(arr) // 2
    if arr[mid] == x:  # midpoint elements
        return True

    if x < arr[mid]:  # first half element
        return binary_search(arr[:mid], x)

    # element in second half
    return binary_search(arr[mid + 1:], x)


# pdf file and pdf score return
def pdf_file_scorer(pdf_file_name):
    text = textract.process(pdf_file_name)
    text = text.decode("utf-8")
    text = text.lower()
    text_words = ''.join([chr(i) for i in range(1, 32)])
    text = text.translate(str.maketrans('', '', text_words))
    text = text.replace(u'\xa0', u'')
    clean_string = re.sub(r'[^A-Za-z]+', ' ', text)
    text = list(clean_string.split(" "))

    word_freq = {}
    for word in set(text):
        word_freq[word] = text.count(word)

    eng_dict = words.words()
    eng_dict.sort()

    # matched = 0
    matched_count = 0
    for word, value in tqdm(word_freq.items()):
        result = binary_search(eng_dict, word)
        if result:
            # matched += 1
            matched_count += value

    total_count = 0
    for word, value in word_freq.items():
        total_count += value

    percentage = (matched_count / total_count) * 100
    return percentage


# take a directory and returns each pdf file in directory to function that returns its score
def path_to_pdf_file(dir_path):
    dict_file_and_score = {}
    for path_name in os.listdir(dir_path):
        if path_name.endswith('.pdf'):
            path_name = os.path.join(dir_path, path_name)
            # print(path_name)
            percentage_pdf = pdf_file_scorer(path_name)
            dict_file_and_score[path_name] = percentage_pdf
    return dict_file_and_score

