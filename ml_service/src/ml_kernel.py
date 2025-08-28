import pandas as pd
import numpy as np


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
    idx = data_titles[data_titles['original_title'] == title].index[0]
    target_vector = vectors[idx]

    similarities = np.dot(vectors, target_vector) / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(target_vector))

    similar_indices = similarities.argsort()[-(top_n+1):-1][::-1]
    return list(data_titles['original_title'][similar_indices])

data_vectors = pd.read_csv('./eda+baseline/data/vectors.csv')
data_titles = pd.read_csv('./eda+baseline/data/titles.csv')


data_vectors['vectors'] = data_vectors['vectors'].map(lambda x: func(x))

data_vectors['vectors'][0]
vectors = np.stack(list(data_vectors['vectors'].values))
