import string
import sys

input_file = 'sorted_converted_3-grams_vg_aftenposten_output.txt'

def get_first2words_3rdword_count(line):
    words = line.split()
    if len(words) != 4:
        return "error","error",1
    for i in range(len(words)-1):
        words[i]=remove_leading_and_trailing_punctuation(words[i])
    try:
        count = int(words[3])
    except:
        count = 1
    return words[0]+' '+words[1], words[2], count

def remove_leading_and_trailing_punctuation(word):
    n = len(word)
    for i in range(n):
        if word[i] not in string.punctuation:
            word = word[i:]
            break
    n = len(word)
    for j in range(-1, -n-1, -1):
        if word[j] not in string.punctuation:
            word = word[:j+1]
            break
    if len(word) == 1:
        if word in string.punctuation:
            return ''
    return word 

dict_first2words_total_counts = {}
dict_first2words_3rdword_counts = {}
with open(input_file, encoding='utf-8') as f:
    for line in f:
        first2words, thirdword, count = get_first2words_3rdword_count(line)
        if first2words not in dict_first2words_total_counts:
            dict_first2words_total_counts[first2words] = count
            dict_first2words_3rdword_counts[first2words] = {}
            dict_first2words_3rdword_counts[first2words][thirdword] = count
        else:
            dict_first2words_total_counts[first2words] = dict_first2words_total_counts[first2words] + count
            if thirdword not in dict_first2words_3rdword_counts[first2words]:
                if len(dict_first2words_3rdword_counts[first2words]) < 3:
                    dict_first2words_3rdword_counts[first2words][thirdword] = count
            else: 
                dict_first2words_3rdword_counts[first2words][thirdword] = dict_first2words_3rdword_counts[first2words][thirdword]+count

for key in dict_first2words_3rdword_counts:
    for k in dict_first2words_3rdword_counts[key]:
        dict_first2words_3rdword_counts[key][k] = dict_first2words_3rdword_counts[key][k]/dict_first2words_total_counts[key]

with open("language_model_from_trigrams.txt", "w") as w:
    for key in dict_first2words_3rdword_counts:
        try:
            w.write("'"+key +"'"+ ' => ' + str(dict_first2words_3rdword_counts[key])+'\n')
        except: 
            pass

