# @author lmiguelmh
# @since 20161201

import os
import commons
import collections
import pycorenlp

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
    sentiment = [s['sentiment'] for s in output['sentences']]
    return collections.Counter(sentiment)


in_dir = 'links_contents_clean'
files = commons.get_files(in_dir)
for file in files:
    in_file = os.path.join(in_dir, file)
    contents = commons.get_content_file(in_file)
    print("sentiment for %s" % in_file)
    sentiment = analize_sentiment(contents)
    print(sentiment)
    break