import pandas as pd
import numpy as np
import pickle
from fuzzywuzzy import process, fuzz


def func(arr: str) -> np.ndarray:
        c = arr
        b = c.split(', ')
        b[0] = b[0][1:]
        b[-1] = b[-1][:-1]
        b = np.array(list(map(float, b)))
        
        return b


def recommend_movies(title: str, top_n=5):
    """
    Function build similarities in runtime
    """
    try:
          idx = data_titles[data_titles['original_title'] == title].index[0]
    except:
          title = find__similar_title(title)
          idx = data_titles[data_titles['original_title'] == title].index[0]
    target_vector = vectors[idx]

    similarities = np.dot(vectors, target_vector) / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(target_vector))

    similar_indices = similarities.argsort()[-(top_n+1):-1][::-1]
    return list(data_titles['original_title'][similar_indices])

def find__similar_title(title: str, threshold=70):
    """
    Function for finding similar title
    """
    all_titles = data_titles['original_title'].tolist()

    matches = process.extract(title, all_titles,
                              scorer=fuzz.token_sort_ratio,
                              limit=5)
    good_matches = [match for match in matches if match[1] >= threshold]


    if not good_matches:
          return matches[0][0]
    
    best_match = good_matches[0]

    return best_match[0]
      

data_titles = pd.read_csv('./eda+baseline/data/titles.csv')

with open('preproccessed_data.pkl', 'rb') as file:
      vectors = pickle.load(file)

print(recommend_movies("Afterburner"))

