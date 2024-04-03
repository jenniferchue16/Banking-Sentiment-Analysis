# Summary: Returns the top 5 associated words and each one's frequency. 
# However, every one of them has the same frequency.
import csv
import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaModel
from pprint import pprint
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter
from collections import defaultdict
nltk.download('stopwords')
nltk.download('punkt')

csv_file = r'D:\Documents\NUS\Y3 S2\DSA3101\Project\all_app_reviews.csv'

df = pd.read_csv(csv_file)

text_data = df['title'].astype(str)  # Replace 'column_name' with the name of the column containing text data

# Define preprocessing functions
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stop_words and token not in punctuation and len(token) > 3]
    return tokens

processed_text_data = [preprocess_text(text) for text in text_data]

# Create a dictionary mapping of word IDs to words
dictionary = corpora.Dictionary(processed_text_data)

corpus = [dictionary.doc2bow(doc) for doc in processed_text_data]

# Load the trained LDA model
lda_model = LdaModel(corpus=corpus,
                     id2word=dictionary,
                     num_topics=3,  # Specify the number of topics
                     passes=10)     # Number of passes through the corpus during training  # Replace 'your_lda_model' with the path to your trained LDA model

def preprocess_text(text):
    if isinstance(text, str):
        tokens = nltk.word_tokenize(text.lower())
        tokens = [token for token in tokens if token not in stop_words and token not in punctuation and len(token) > 3]
        return tokens
    else:
        return []

df = df.drop(df.columns[[1, 2, 3]], axis=1)

def get_associated_words(text):
    tokens = preprocess_text(text)
    associated_words = []
    for token in tokens:
        topic_scores = lda_model.get_term_topics(token)
        if topic_scores:
            topic_id, _ = max(topic_scores, key=lambda x: x[1])
            top_words = lda_model.show_topic(topic_id)
            associated_words.extend([word for word, _ in top_words])
    return associated_words

df['associated_words'] = df['title'].apply(lambda x: get_associated_words(x))

###############################################################################

word_document_count = defaultdict(set)
word_counts = defaultdict(int)
for i, word_list in enumerate(df['associated_words']):
    for word in word_list:
        if i not in word_document_count[word]:
            word_document_count[word].add(i)
            word_counts[word] += 1

# Get the top 5 associated words
top_associated_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:5]

# Create a DataFrame from the top associated words
top_associated_words_df = pd.DataFrame(top_associated_words, columns=['Associated Word', 'Frequency'])

# Print out the top 5 associated words
print(top_associated_words_df)