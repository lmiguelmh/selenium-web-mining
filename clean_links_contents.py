# @author lmiguelmh
# @since 20161126

import os
import re
import nltk


def get_files(dir):
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


def clean_lines(lines, preprocess=True):
    if not preprocess:
        return lines
    else:
        preprocessed_lines = []
        for line in lines:
            # TODO make a NN to recognize the type of word? NUMBER, PERCENT, HOUR, DATE, ABBR, (y corregir errores en twitter!)
            # standardize perc values  --  remember ?: non capturing group
            # line = re.sub('(?:\d*[.,]?\d+|\d+[.,]?\d*)%', 'PERCENTAGE', line)
            line = re.sub('[+\-]?(?:\d*[.,]?\d+|\d+[.,]?\d*)%', 'PERCENTAGE', line)
            # standardize monetary values
            line = re.sub('\$\d*(?:\d*[.,]?\d+|\d+[.,]?\d*)[Mm]?', 'MONEY', line)
            # standardize num values - not by now too many false positives
            # line = re.sub('\d*(?:\d*[.,]?\d+|\d+[.,]?\d*)', 'NUMBER', line)
            # standardize abbreviations
            # line = re.sub('\s([A-Z][a-z]{1,2})\.\s', ' \g<1> ', line)
            preprocessed_lines.append(line)
        return preprocessed_lines


def clean_file(in_file, out_file, preprocess=True):
    # min words per paragraph
    min_words_per_paragraph = 7
    with open(in_file, 'r', encoding='utf8') as f:
        lines = [line.rstrip('\n') for line in f if len(line.split()) > min_words_per_paragraph]

    # cleaning and preprocessing files
    if preprocess:
        lines = clean_lines(lines)

    with open(out_file, 'wb') as f:
        lines = "\n".join(lines)
        f.write(bytes(lines, encoding='utf8'))


in_dir = 'links_contents'
out_dir = 'links_contents_clean'
files = get_files(in_dir)
for file in files:
    in_file = os.path.join(in_dir, file)
    out_file = os.path.join(out_dir, file)
    clean_file(infile, outfile)
