import requests
import os
from PIL import Image
from io import BytesIO
from app import app,db,Movies
import json
import re


#AAA.jpg - иозображение по умолчанию

#короче захуярить так чтобы находило в процессе передачи обьекта в html код 
#и одновремеено передавало png картинку
title = 'Snow White and the Huntsman'




API_KEY = '4a27dc2'

url = f'http://www.omdbapi.com/?i=tt3896198&apikey=4a27dc2&t={title}'


response = requests.get(url).json()
print(response)
image_url=response['Poster']
movie_name=response['Title']
print(image_url,movie_name)


def sanitize_filename(filename):
    sanitized = filename.replace(" ", "_")
    sanitized = re.sub(r'[<>:"/\\|?*]', '', sanitized)
    return sanitized


def count_files_in_directory(directory):
    return len(next(os.walk(directory))[2])


def download_movies():
    with app.app_context():
        movies = Movies.query.all()
        api_key = '4a27dc2'
        base_url = 'http://www.omdbapi.com/'
        base_url = f'http://www.omdbapi.com/?i=tt3896198&apikey=4a27dc2'

        media_folder = 'media'
        os.makedirs(media_folder, exist_ok=True)
        count=0
        for movie in movies:
            count+=1
            
            if count < 2000:
                continue
            
            
            title = movie.title
            url = f'{base_url}&t={title}'
            response = requests.get(url).json()
            directory_path = 'media'
            print(f"Количество файлов в папке: {count_files_in_directory(directory_path)}")
            
            if response.get('Response') == 'True':
                movie_name = response['Title']
                poster_url = response.get('Poster')
                if poster_url and poster_url != 'N/A':
                    poster_response = requests.get(poster_url, stream=True)
                    if poster_response.status_code == 200:
                        sanitized_title = sanitize_filename(movie_name.replace(" ", "_").replace(":", "").replace("/", ""))
                        poster_path = os.path.join(media_folder, f'{sanitized_title}.jpg')
                        with open(poster_path, 'wb') as f:
                            for chunk in poster_response.iter_content(1024):
                                f.write(chunk)
                    else:
                        print(f'Error downloading poster for {title}')
                else:
                    print(f'No poster available for {title}')
            else:
                print(f'Error fetching data for {title}: {response.get("Error")}')

        return "Movies data and posters downloaded and saved."

download_movies()




# Пример использования
