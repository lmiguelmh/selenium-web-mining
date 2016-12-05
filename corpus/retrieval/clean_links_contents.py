# @author lmiguelmh
# @since 20161126

import os
import re

import commons


def clean_lines(lines, preprocess=True):
    if not preprocess:
        return lines
    else:
        preprocessed_lines = []
        for line in lines:
            # a n-n to recognize the type of word? NUMBER, PERCENT, HOUR, DATE, ABBR, (y corregir errores en twitter!)
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


def clean_file(in_file, out_file, preprocess=True, min_words_per_paragraph=7, min_size=1 * 1024, max_size=15 * 1024):
    with open(in_file, 'r', encoding='utf8') as f:
        lines = [line.rstrip('\n') for line in f if len(line.split()) > min_words_per_paragraph]
        # lines = []
        # i = 0
        # for line in f:
        #     if i == 1:
        #         lines.append(line)
        #     else:
        #         words = line.split()
        #         for word in words:
        #     i+=1

    # cleaning and preprocessing files
    if preprocess:
        lines = clean_lines(lines)

    # size
    size = sum([len(line) for line in lines])
    if size <= min_size or size >= max_size:
        return

    with open(out_file, 'wb') as f:
        lines = "\n".join(lines)
        f.write(bytes(lines, encoding='utf8'))


in_dir = '../../data/corpus/links_contents'
out_dir = '../../data/corpus/links_contents_clean'
files = commons.get_files(in_dir)
for file in files:
    try:
        in_file = os.path.join(in_dir, file)
        out_file = os.path.join(out_dir, file)
        print("cleaning %s" % in_file)
        clean_file(in_file, out_file, False, min_words_per_paragraph=12)
    except Exception as e:
        print(e)
        pass

    # break
