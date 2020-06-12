# News TF-IDF

Indexes a dataset of news articles and provides a search tool to navigate
through them. I used the
[TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) algorithm to parse the
search query and rank documents based on their similarity to the search.
Additionally, I cleaned and stemmed the search terms and document content to
extract their root meaning so that documents could be matched more
accurately.

## Demo

This project is hosted on Heroku at https://newstfidf.herokuapp.com/
**Please note that startup times for the app may vary depending on the
availability of the free tier of Heroku servers at that time.** Wait for at least 1 minute so that the app can index through articles. Subsequent searches should be much faster.

## Data

The data used for this project comes from the Kaggle dataset found
[here](https://www.kaggle.com/snapcrack/all-the-news).
