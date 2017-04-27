from CyberSpiders import articlemodel
import pymodm
from collections import Counter
from time import time
import spacy
if __name__ == '__main__':

    pymodm.connection.connect('mongodb://jodo1991:cybernews@ds159220.mlab.com:59220/cybernewsarticles', alias='articledb')


    articles = articlemodel.Article.objects.limit(1)

    counter = Counter()
    counter2 = Counter()
    nlp = spacy.load('en')

    Exclude_Words = {
        'RSS':True, '"':True, 'Security':True, 'Sunshine':True, '-':True, 'Warnings':True, 'Monday':True,
        'Tuesday':True,'Wednesday':True,'Thursday':True,'Friday':True,'Saturday':True,'Sunday':True, 'Web':True,
        'Read':True, '”':True, 'Internet':True, '—':True, 'Latest':True, 'Update':True, "It’s":True, 'January':1,
        'February':1,'March':1,'April':1,'May':1,'June':1, 'July':1, "August":1, 'September':1, 'October':1, 'November':1,
        'December':1, 'Tags':1, '–':1, ']':1, 'New':1, 'Department':1,'IP':1
    }

    exectime = 0
    total = time()
    for article in articles:
        t = time()
        doc = nlp(article.body)
        exectime += time() - t
        unique = set()
        for phrase in doc.noun_chunks:
            foundproper = False
            for word in phrase:
                if word.pos_ == "PROPN" and word.ent_type_ != "DATE":
                    foundproper = True
            if foundproper:
                unique.add(phrase.text.lower())
        counter.update(unique)
        #counter2.update(set(word.text for word in doc if word.pos_ == "PROPN" and word.ent_type_ != "DATE"))
        # for word in doc:
        #     if word.pos_ is "PROPN" and word.ent_type_ is not 'DATE':
        #         print(word)
        #counter.update(set([word[0] for word in TextBlob(article.body).tags if 'NNP' in word[1] and len(word) > 1 and word[0] not in Exclude_Words]))
    print(time() - total)
    print(exectime)
    print(counter.most_common(20))
    # for phrase in counter.most_common(20):
    #     print(phrase)
