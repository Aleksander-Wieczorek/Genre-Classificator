# Genre-Classificator
ML project for book genre classification

Analysed data comes from 2 different datasets,

Original dataset is in `data_&_analysis/data.csv` - it has clear data, title, description and exactly one genre per book

That dataset was too small so we decidet to join it with way bigger dataser `books.csv` however this dataset is way more chaotic, each book had a **list** of genres. First cleaning left only those records, which contained exactly one genre from genres in `data.csv`, then those datasets were joined and landed into `joined.csv`.

Afterwards that set was *cleaned* - first regexes deleted all symbols other than letters, also it removed some useless words in text (like stopwords) - then the words were stemmed with `LancasterStemmer`, which removed prefixes/sufixes to unify some words. After those operations `reduced.csv` was created.

Then after dropping some columns, and renaming them `train_set.csv` was created. However that set contained over 80.000 different words, so removal of words used only once was necessary - after that operation `reduced.csv` with only 42.000 different stemmed words was created.
