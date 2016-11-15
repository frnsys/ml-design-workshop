import json

articles = json.load(open('data/articles_processed.json', 'r'))
docs = ['\n'.join([a['title'], a['text']]) for a in articles]

import spacy
from spacy.parts_of_speech import VERB, NUM, NOUN
nlp = spacy.load('en')

def extract_keywords(doc):
    # here we run spacy on the text
    # it will identify named entities and tag parts-of-speech
    doc = nlp(doc)
    ents = [ent.text for ent in doc.ents]
    toks = [tok.text for tok in doc
            if not tok.is_stop and tok.pos in [VERB, NUM, NOUN]]
    return [t.lower() for t in ents + toks]

docs = ['||'.join(extract_keywords(d)) for d in docs]

with open('data/docs_processed.json', 'w') as f:
    json.dump(docs, f)

def tokenize(doc):
    return doc.split('||')

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(
    strip_accents='ascii', # remove accents from characters
    lowercase=False,       # don't make things lowercase, this will mess up the NER step
    use_idf=True,          # we want to use IDF
    smooth_idf=True,       # we want to "smooth" the IDF (avoiding division by 0)
    max_df=1.0, # ignore terms w/ DF higher than this (int=absolute, float=percent)
    min_df=1,   # ignore terms w/ DF lower than this (int=absolute, float=percent)
    stop_words='english',  # remove very common English words (e.g. the, a, an)
    tokenizer=tokenize     # use our tokenization function
)

vecs = vectorizer.fit_transform(docs)

from scipy import io
io.mmwrite('data/vecs.mtx', vecs)

from sklearn.externals import joblib
joblib.dump(vectorizer, 'data/vectorizer.pkl')
print('done')
