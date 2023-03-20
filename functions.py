from datetime import date
from random import randint
from config import X_MAL_CLIENT_ID
import requests


def get_random_anime():
    year = randint(1989, date.today().year)
    season = (['winter', 'spring', 'summer', 'fall'][randint(0, ((date.today().month - 1) % 12) // 3)] 
              if year == date.today().year else ['winter', 'spring', 'summer', 'fall'][randint(0, 3)])
    url = f'https://api.myanimelist.net/v2/anime/season/{year}/{season}?limit=100&fields=main_picture,title,start_season,media_type,rating,mean,num_episodes,genres'
    response = requests.get(url, headers={'X-MAL-CLIENT-ID': X_MAL_CLIENT_ID})
    anime_lst = []
    for d in response.json().get('data'):
        if ((not(d.get('node').get('mean') is None) and d.get('node').get('mean') >= 6)
            and (d.get('node').get('num_episodes') != '?' and d.get('node').get('num_episodes') > 0)):
            anime_lst.append(d)
    return anime_lst[randint(0, len(anime_lst) - 1)] if not(anime_lst is None) else get_random_anime()


def get_picture_url(random_anime):
    return random_anime.get('node').get('main_picture').get('medium')


def get_name(random_anime):
    return random_anime.get('node').get('title')


def get_premiered(random_anime):
    return f'{random_anime.get("node").get("start_season").get("season")} {random_anime.get("node").get("start_season").get("year")}'.title()


def get_type(random_anime):
    return (str(random_anime.get('node').get('media_type')).upper() 
            if len(random_anime.get('node').get('media_type')) <= 3 
            else str(random_anime.get('node').get('media_type')).title())


def get_rating(random_anime):
    return str(random_anime.get('node').get('rating')).upper()


def get_score(random_anime):
    return random_anime.get('node').get('mean')


def get_episodes(random_anime):
    return random_anime.get('node').get('num_episodes')


def get_genres(random_anime):
    genres = []
    try:
        for genre in random_anime.get('node').get('genres'):
            genres.append(genre.get('name'))
        return ', '.join(genres)
    except Exception:
        return genres