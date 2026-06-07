import pandas as pd
import ast

def filter_genres(genre_raw):
    try:
        if genre_raw.startswith('['):
            genres_list = ast.literal_eval(genre_raw)
        else:
            genres_list = [g.strip() for g in genre_raw.split(',')]
            
        genres_list = [g.lower() for g in genres_list]
        
        matches = [g for g in genres_list if g in target_genres]
        
        return matches[0] if len(matches) == 1 else None
    except:
        return None
    

needed_cols = ['title', 'description', 'genres']
df = pd.read_csv('books.csv', usecols=needed_cols)

df = df.dropna(subset=['description', 'genres'])

target_genres = {'history', 'thriller', 'romance', 'fantasy', 'crime','science', 'psychology','travel','sports','horror'}



df['genre_filtered'] = df['genres'].apply(filter_genres)

df_final = df.dropna(subset=['genre_filtered']).copy()

df_final = df_final[['title', 'description', 'genre_filtered']]
print("FILTERED_BIGGER:")
print(df_final['genre_filtered'].value_counts())


df_smaller = pd.read_csv('data.csv')
df_mala_temp = df_smaller.rename(columns={
    'genre': 'genre_filtered', 
    'summary': 'description',
    'title': 'title'
})
cols_to_keep = ['title', 'description', 'genre_filtered']
df_combined = pd.concat([df_final[cols_to_keep], df_mala_temp[cols_to_keep]], ignore_index=True)
df_combined['title_lower'] = df_combined['title'].str.lower().str.strip()

df_final = df_combined.drop_duplicates(subset=['title_lower'], keep='first').copy()


df_final.to_csv('joined.csv', index=False)
df_final = df_final.drop(columns=['title_lower'])

# sum outputs
print("JOINED:")

print(df_final['genre_filtered'].value_counts())
df_final = df_final.dropna(subset=['description', 'genre_filtered'])
print(df_final['genre_filtered'].value_counts())
