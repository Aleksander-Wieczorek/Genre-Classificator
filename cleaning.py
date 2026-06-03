import nltk
from nltk.corpus import stopwords #for cleaning 
from nltk.stem import LancasterStemmer ##for cleaning 
import re ##for cleaning
import pandas as pd
import string
stemmer = LancasterStemmer()
nltk.download('stopwords')
nltk.download('punkt_tab')

stemmer = LancasterStemmer()
stop_words = set(stopwords.words("english"))

def cleaning_data(text):
    text = text.lower()
    text = re.sub(r'isbn[:\s]*', '', text) 
    text = re.sub(r'@\S+', '', text) 
    text = re.sub(r'http\S+', '', text) # remove URLs
    text = re.sub(r'.pic\S+', '', text) # remove image links
    text = re.sub(r'[^a-zA-Z+]', ' ', text)  # Change to replace non-characters with a space
    
    text = "".join([i for i in text if i not in string.punctuation])
    words = nltk.word_tokenize(text)
    # Use the predefined stop_words variable instead of redefining it inside the function
    text = " ".join([i for i in words if i not in stop_words and len(i) > 2])
    text = re.sub(r"\s+", " ", text).strip()  # Replace multiple spaces with a single space
    return text

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
