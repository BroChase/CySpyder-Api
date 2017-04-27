from collections import Counter
import spacy
from difflib import SequenceMatcher

class Analyzer():
    nlp = None

    def __init__(self):
        nlp = None
        self.exclude_words = {
        '’s':1, 'krebsonsecurity':1, 'threatpost':1, 'darkreading':1, 'reading':1, 'chris gonsalves':1,
        'mike mimoso':1, 'chris brook':1, 'dennis fisher':1, 'dark reading':1, 'reuters':1
    }

    def loadSpacy(self):
        import spacy
        Analyzer.nlp = spacy.load('en')

    def getMostCommonNounPhrases(self, maxphrases, articles):
        indivMostCommon = Counter()
        totalMostCommon = Counter()
        for article in articles:
            indivMostCommon.clear()
            doc = Analyzer.nlp(article)
            unique = set()

            for phrase in doc.noun_chunks:
                foundproper = False
                propphrase = ''

                for word in phrase:
                    if word.pos_ == "PROPN" and word.pos_ != "DET" and word.text != "'s" \
                            and word.ent_type_ not in "DATE TIME PERSON PART" \
                            and word.text.lower() not in self.exclude_words:
                        foundproper = True
                        propphrase = (propphrase + ' ' + word.text).strip()
                if foundproper == True:
                    foundsimilar = False

                    for commonphrase in indivMostCommon.elements():
                        if propphrase == self.getpropns(commonphrase):
                            indivMostCommon.update([commonphrase])
                            unique.add(commonphrase)
                            foundsimilar = True
                            break

                    if not foundsimilar:
                        indivMostCommon.update([propphrase])
                        unique.add(propphrase)

            totalMostCommon.update(unique)

        if len(articles) == 1:
            return [phrase for phrase in indivMostCommon.most_common(maxphrases)]
        else:
            return [phrase for phrase in totalMostCommon.most_common(maxphrases)]

    def getpropns(self, phrase):
        doc = Analyzer.nlp(phrase)
        string = ''
        for word in doc:
            if word.pos_ == "PROPN":
                string = (string + ' ' + word.text).strip()

        return string