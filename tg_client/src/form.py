import requests
from functools import lru_cache
import os
from dotenv import load_dotenv


load_dotenv()
KINOPOISK_API_KEY = os.getenv('KINOPOISK_API_KEY')
OMDB_API_KEY = os.getenv('OMDB_API_KEY')      

@lru_cache(maxsize=100)
def get_movie_info(title: str):
    """
    Умный поиск информации о фильме: КиноПоиск → OMDB → Fallback
    """
    normalized_title = title.strip()
    
    kp_result = get_kinopoisk_info(normalized_title)
    if kp_result and kp_result.get('rating') not in [None, "N/A", 0]:
        return kp_result

    omdb_result = get_omdb_info(normalized_title)
    if omdb_result and omdb_result.get('rating') not in [None, "N/A", 0]:
        return omdb_result
    
    return {
        'title': normalized_title,
        'overview': "no",
        'poster_url': "no",
        'rating': "no",
        'source': "no"
    }

def get_kinopoisk_info(title: str):
    """Получение информации с КиноПоиск API"""
    try:
        headers = {
            'X-API-KEY': KINOPOISK_API_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={title}',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('films') and len(data['films']) > 0:
                film = data['films'][0]
                
                return {
                    'title': film.get('nameRu', title),
                    'original_title': film.get('nameEn', ''),
                    'overview': film.get('description', 'Описание отсутствует'),
                    'poster_url': film.get('posterUrl'),
                    'rating': float(film.get('rating', 0)) if film.get('rating') else 0,
                    'year': film.get('year', ''),
                    'source': 'kinopoisk'
                }
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Kinopoisk API error for '{title}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error with Kinopoisk for '{title}': {e}")
        return None

def get_omdb_info(title: str):
    """Получение информации с OMDB API"""
    try:
        response = requests.get(
            f'http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}&plot=full',
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                
                rating = 0
                if data.get('imdbRating') and data['imdbRating'] != 'N/A':
                    try:
                        rating = float(data['imdbRating'])
                    except ValueError:
                        rating = 0
                
                return {
                    'title': data.get('Title', title),
                    'original_title': data.get('Title', ''),
                    'overview': data.get('Plot', 'Описание отсутствует'),
                    'poster_url': data.get('Poster'),
                    'rating': rating,
                    'year': data.get('Year', ''),
                    'source': 'omdb'
                }
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"OMDB API error for '{title}': {e}")
        return None
    
    except Exception as e:
        print(f"Unexpected error with OMDB for '{title}': {e}")
        return None
    