# @author lmiguelmh
# @since 20161201
import ast
import codecs
import collections
import os
import pickle

import pycorenlp

import commons


def analize_sentiment(contents):
    nlp = pycorenlp.StanfordCoreNLP('http://127.0.0.1:9000')
    output = nlp.annotate(
        contents,
        properties={
            'annotators': 'sentiment',
            'outputFormat': 'json'
        }
    )
    # http://stanfordnlp.github.io/CoreNLP/sentiment.html#options
    if type(output) is str:
        try:
            # in some cases nlp sends "" instead of '', so we need to evaluate
            output = ast.literal_eval(output)
        except BaseException as e:
            pass

    if type(output) is dict and 'sentences' in output:
        # print(type(output))
        # print(output)
        sentiment = [s['sentiment'] for s in output['sentences'] if 'sentiment' in s]

        # # this happens when the corenlp server sends "" instead of ''
        # if type(output) is str:
        #     output = ast.literal_eval(output)
        #
        # sentiment = []
        # for sent in output['sentences']:
        #     if 'sentiment' in sent:
        #         sentiment.append(sent['sentiment'])
        # if not sentiment or len(sentiment) == 0:
        #     print(output)
        #     raise AssertionError
        return collections.Counter(sentiment)
    else:
        # CoreNLP request timed out. Your document may be too long.
        print(output)
        if "timed out" in output:
            counter = collections.Counter()
            sentences = contents.split()
            print("splitting in %d sentences" % len(sentences))
            for sentence in sentences:
                cnt = analize_sentiment(sentence)
                counter += cnt
            return counter

        else:
            raise AssertionError
            # return collections.Counter()


in_dir = '../../data/corpus/links_contents_clean'
pkz_dir = '../../data/sentiment/corpus'

files = commons.get_files(in_dir)
corpus_sentiment = {}
date_sentiment = None
old_date = None
for file in files:
    # calculating or retrieving the sentiment for one file
    pkz_file = "%s/%s.pkz" % (pkz_dir, file)
    print("sentiment for %s" % file)
    if not os.path.exists(pkz_file):
        in_file = os.path.join(in_dir, file)
        contents = commons.get_content_file(in_file)
        sentiment = analize_sentiment(contents)
        pkz = codecs.encode(pickle.dumps(sentiment), 'zlib_codec')
        with open(pkz_file, 'wb') as f:
            f.write(pkz)
    else:
        with open(pkz_file, 'rb') as f:
            compressed_content = f.read()
        sentiment = pickle.loads(codecs.decode(compressed_content, 'zlib_codec'))
    print(sentiment)

    # sumarizing by date
    date = file.split('-')[0]  # 20161001-207b1e7fe196e9c4-Venezuela_Set_For_Mass_Bitcoin_Adoption_As_China_Cuts_Off.txt
    if old_date is not None and old_date != date:
        corpus_sentiment[old_date] = date_sentiment
        date_sentiment = None
        # print(corpus_sentiment)
        # break

    if date_sentiment is None:
        date_sentiment = {}

    for k, v in sentiment.items():
        if k in date_sentiment:
            date_sentiment[k] += v
        else:
            date_sentiment[k] = v

    old_date = date

# print(corpus_sentiment)
pkz_file = '../../data/sentiment/all.pkz'
pkz = codecs.encode(pickle.dumps(corpus_sentiment), 'zlib_codec')
with open(pkz_file, 'wb') as f:
    f.write(pkz)
