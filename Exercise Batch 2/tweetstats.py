#ming

import json
from langdetect import detect
from langid import classify
import re
from collections import Counter

results_langdetect = []
results_langid = []
tweet_lang = []

with open('tweets.json', 'r') as f:
    for line in f:
        try:
            tweet = json.loads(line)
            results_langdetect.append(detect(json.dumps(tweet['text'])))
            results_langid.append(classify(json.dumps(tweet['text']))[0])
            tweet_lang.append(json.dumps(tweet['lang']))
        except Exception:
            results_langdetect.append('')
            results_langid.append(classify(json.dumps(tweet['text']))[0])
            tweet_lang.append(json.dumps(tweet['lang']))

detect_correct = 0
id_correct = 0
for i in range(len(tweet_lang)):
    if results_langdetect[i] == tweet_lang[i].strip('""'):
        detect_correct += 1
    if results_langid[i] == tweet_lang[i].strip('""'):
        id_correct += 1

print("total data: " + str(len(tweet_lang)))
print("langdetect library correct: " + str(detect_correct))
print("langid library correct: " + str(id_correct))

language_text = {}
with open('tweets.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        if json.dumps(tweet['lang'].strip('""')) not in language_text:
            language_text[json.dumps(tweet['lang'].strip('""'))] = json.dumps(tweet['text'].strip('""'))
        else:
            language_text[json.dumps(tweet['lang'].strip('""'))] += ' ' + json.dumps(tweet['text'].strip('""'))
# print(language_text)

def wordfreq(text):
    words = re.findall(r'\w+', text)
    cap_words = [word.upper().encode('utf-8') for word in words]
    word_counts = Counter(cap_words).most_common(10)
    return word_counts

for key in language_text:
    print(key, wordfreq(language_text[key]))