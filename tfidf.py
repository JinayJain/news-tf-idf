import pandas as pd
import math
import string
from operator import itemgetter
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from flask import Flask, render_template, request
import os

stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')
punc_table = str.maketrans('', '', string.punctuation)


def tokenize(text):
    # split into tokens
    tokens = word_tokenize(text)
    # convert them to lowercase
    tokens = [w.lower() for w in tokens]
    # remove punctutation marks
    tokens = [w.translate(punc_table)
              for w in tokens]
    # keep only alphabetic words
    tokens = [w for w in tokens if w.isalpha()]
    # remove meaningless words ("the", "and", etc.)
    tokens = [w for w in tokens if not w in stop_words]
    # keep only word stem to make words like drink, drinks, drinking => drink
    tokens = [stemmer.stem(w) for w in tokens]

    return tokens


def get_article_freq(article):
    tokens = tokenize(article)
    article_freq = {}

    for token in tokens:
        if token in article_freq:
            article_freq[token] += 1
        else:
            article_freq[token] = 1

    for token in article_freq:
        article_freq[token] /= len(tokens)

    return article_freq


print("Indexing articles...")

csv_path = './data/articles2.csv'
n_articles = 1000

articles_csv = pd.read_csv(csv_path, nrows=n_articles)

doc_freq = {}
articles = []

for idx, article in articles_csv[['id', 'content']].iterrows():
    article_freq = get_article_freq(article['content'])

    for token in article_freq:
        if token in doc_freq:
            doc_freq[token] += 1
        else:
            doc_freq[token] = 1

    articles.append((article['id'], article_freq))

for token in doc_freq:
    doc_freq[token] /= n_articles


def search(query, n_result):
    query_tokens = tokenize(query)

    article_scores = [[article['id'], 0]
                      for idx, article in articles_csv.iterrows()]

    def tfidf(term, article_freq):
        if term in article_freq:
            return article_freq[term] * math.log(1 / doc_freq[term])
        else:
            return 0.

    for token in query_tokens:
        for i in range(len(articles)):
            article_scores[i][1] += tfidf(token, articles[i][1])

    article_scores = sorted(article_scores, key=itemgetter(1))[::-1]
    return article_scores[:n_result]


print("Done!")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search_page():
    query = request.args['query']
    n_articles = request.args['num_articles']
    results = search(query, int(n_articles))
    res_ids = [article[0] for article in results if article[1] > 0]

    # res_articles = pd.DataFrame(columns=articles_csv.columns)
    res_articles = []
    for article_id in res_ids:
        res_articles.append(
            articles_csv.loc[articles_csv['id'] == article_id].iloc[0].to_dict())

    return render_template('search.html', articles=res_articles)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, host='0.0.0.0')
