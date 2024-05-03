import streamlit as st
import pandas as pd
from nltk.tokenize import word_tokenize
from collections import defaultdict
import nltk
nltk.download('punkt')


st.set_page_config(layout="wide")
st.title('GSC Data of Dishtv of last 3 Months')
# Load the DataFrame from the downloaded CSV file
# Using raw string
df = pd.read_csv(r'n-grams/search_analytics_data (1).csv', encoding='utf-8')
st.write(df)

# Calculate the total clicks and ctr count for each word
word_clicks = defaultdict(int)
word_ctr_count = defaultdict(int)
for index, row in df.iterrows():
    words = word_tokenize(row['keyword'])
    for word in set(words):  # Use set to count each word only once per keyword
        word_clicks[word.lower()] += row['clicks']
        word_ctr_count[word.lower()] += 1 if row['ctr(in %)'] > 0 else 0  # Count only if ctr > 0

# Create a DataFrame from the word_clicks and word_ctr_count dictionaries
data = {'pattern': [], 'count': [], 'clicks(Sum)': []}
for word, clicks in word_clicks.items():
    data['pattern'].append(word)
    data['count'].append(word_ctr_count[word])
    data['clicks(Sum)'].append(clicks)

unigram_df = pd.DataFrame(data)

# Calculate the total clicks and ctr count for each bigram
word_clicks = defaultdict(int)
word_ctr_count = defaultdict(int)
for index, row in df.iterrows():
    words = word_tokenize(row['keyword'])
    for i in range(len(words) - 1):  # Iterate over word pairs
        bigram = (words[i].lower(), words[i + 1].lower())
        word_clicks[bigram] += row['clicks']
        word_ctr_count[bigram] += 1 if row['ctr(in %)'] > 0 else 0  # Count only if ctr > 0

# Create a DataFrame from the word_clicks and word_ctr_count dictionaries
data = {'pattern': [], 'count': [], 'clicks(Sum)': []}
for bigram, clicks in word_clicks.items():
    data['pattern'].append(' '.join(bigram))
    data['count'].append(word_ctr_count[bigram])
    data['clicks(Sum)'].append(clicks)

bigram_df = pd.DataFrame(data)

# Calculate the total clicks and ctr count for each word
word_clicks = defaultdict(int)
word_ctr_count = defaultdict(int)
for index, row in df.iterrows():
    words = word_tokenize(row['keyword'])
    for i in range(len(words) - 2):  # Iterate over word triplets (trigrams)
        trigram = (words[i].lower(), words[i + 1].lower(), words[i + 2].lower())
        word_clicks[trigram] += row['clicks']
        word_ctr_count[trigram] += 1 if row['ctr(in %)'] > 0 else 0  # Count only if ctr > 0

# Create a DataFrame from the word_clicks and word_ctr_count dictionaries
data = {'pattern': [], 'count': [], 'clicks(Sum)': []}
for trigram, clicks in word_clicks.items():
    data['pattern'].append(' '.join(trigram))
    data['count'].append(word_ctr_count[trigram])
    data['clicks(Sum)'].append(clicks)

trigram_df = pd.DataFrame(data)
# Streamlit app

st.header('N-gram of Data')
# Display DataFrames in a horizontal row
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('Unigram Patterns Analysis')
    st.write(unigram_df)

with col2:
    st.subheader('Bigram Patterns Analysis')
    st.write(bigram_df)

with col3:
    st.subheader('Trigram Patterns Analysis')
    st.write(trigram_df)
