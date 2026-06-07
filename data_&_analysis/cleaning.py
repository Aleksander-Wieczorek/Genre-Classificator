import nltk
from nltk.corpus import stopwords #for cleaning 
from nltk.stem import LancasterStemmer ##for cleaning 
import re ##for cleaning
import pandas as pd
import string
stemmer = LancasterStemmer()
nltk.download('stopwords')
nltk.download('punkt_tab')

stop_words = set(stopwords.words("english"))

def cleaning_data(text):
    text = text.lower()
    text = re.sub(r'isbn[:\s]*', '', text) 
    text = re.sub(r'@\S+', '', text) 
    text = re.sub(r'http\S+', '', text) # remove URLs
    text = re.sub(r'[^a-zA-Z+]', ' ', text)  # Change to replace non-characters with a space
    
    words = text.split()    
    text = " ".join([i for i in words if i not in stop_words and len(i) > 2])
    cleaned_words = [stemmer.stem(w) for w in words if w not in stop_words and len(w) > 2]
    return " ".join(cleaned_words)

data = pd.read_csv('joined.csv')
data['description'] = (pd.concat([data['description'], data['title_lower']], axis=1).apply(lambda x: ' '.join(x), axis=1)).apply(cleaning_data)
data.to_csv('cleaned.csv', index=False)

data = pd.read_csv('cleaned.csv')
data.drop(columns=['title_lower'], inplace=True)
data.drop(columns=['title'], inplace=True)
data.rename(columns={'description': 'text','genre_filtered': 'label'}, inplace=True)
data.to_csv('train_set.csv', index=False)

statistics = data['label'].value_counts()
print(statistics)

# count number of unique words in the cleaned descriptions
unique_words = set()
for description in data['text']:
    unique_words.update(str(description).split())
print(f"Number of unique words in cleaned descriptions: {len(unique_words)}")


all_words = data['text'].str.split().explode()
word_counts = all_words.value_counts()

valid_words = set(word_counts[word_counts > 1].index)

data['text'] = data['text'].apply(lambda x: ' '.join([w for w in (str(x)).split() if w in valid_words]))
# remove rows with empty descriptions
data = data[data['text'].str.strip() != '']
data.to_csv('reduced.csv', index=False)

statistics = data['label'].value_counts()
print(statistics)

unique_words = set()
for description in data['text']:
    unique_words.update(str(description).split())
print(f"Number of unique words in cleaned descriptions: {len(unique_words)}")