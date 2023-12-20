import json
from threading import Thread
import requests
import sys

RAPIDAPI_MOVIESDB_URL = 'https://movie-database-imdb.p.rapidapi.com'
RAPIDAPI_KEY = '7f22180744msh05c8687466b0564p10d8a6jsn371b1d20bfcf'

MOVIESDB_KNOWN_GENRES = [
    "", 'Action', 'Adult', 'Adventure',
    'Animation', 'Biography', 'Comedy', 'Crime',
    'Documentary', 'Drama', 'Family', 'Fantasy',
    'Film-Noir', 'Game-Show', 'History', 'Horror',
    'Music', 'Musical', 'Mystery', 'News', 'Reality-TV',
    'Romance', 'Sci-Fi', 'Short', 'Sport',
    'Talk-Show', 'Thriller', 'War', 'Western'
]


class Movie:
    def __init__(self):
        self._id = None
        self._title_name = None
        self._poster_url = None
        self._release_date = None
        self._actors = []
        self._query_details = []

    def set_name(self, name):
        self._title_name = name

    def set_poster_url(self, poster_url):
        self._poster_url = poster_url

    def set_release_date(self, release_date):
        self._release_date = release_date

    def set_actors(self, actors):
        self._actors = actors

    def set_id(self, id):
        self._id = id

    def actors(self):
        return self._actors

    def name(self):
        return self._title_name

    def released(self):
        return self._release_date

    def id(self):
        return self._id

    def set_query_details(self, query_details):
        self._query_details = query_details

    def query_details(self):
        return self._query_details


class Series:
    def __init__(self):
        self._title_name = None
        self._poster_url = None
        self._release_date = None
        self._actors = []
        self._id = None
        self._query_details = []

    def set_name(self, name):
        self._title_name = name

    def set_poster_url(self, poster_url):
        self._poster_url = poster_url

    def set_release_date(self, release_date):
        self._release_date = release_date

    def set_actors(self, actors):
        self._actors = actors

    def set_id(self, id):
        self._id = id

    def actors(self):
        return self._actors

    def name(self):
        return self._title_name

    def released(self):
        return self._release_date

    def id(self):
        return self._id

    def set_query_details(self, query_details):
        self._query_details = query_details

    def query_details(self):
        return self._query_details


class MovieInfoRetriever:
    def __init__(self):
        # Заголовки для авторизации в API
        self.headers = {
            'X-RapidAPI-Key': RAPIDAPI_KEY,
            'X-RapidAPI-Host': "moviesdatabase.p.rapidapi.com"
        }

    def format_query(self, query):
        # Замена пробелов на "%20"
        formatted_query = query.replace(" ", "%20")
        return formatted_query

    def get_movie_info(self, query):
        # Формирование URL запроса с учетом параметров
        url = f"https://moviesdatabase.p.rapidapi.com/titles/search/title/{query}"
        # Параметры запроса
        querystring = {
            "exact": "false",
            "titleType": "movie"
        }
        try:
            # Отправка GET-запроса
            response = requests.get(url, headers=self.headers, params=querystring)
            # Проверка успешности запроса
            response.raise_for_status()
            # Получение текстового содержимого ответа
            data = response.text
            # Возвращение данных
            return data
        except requests.exceptions.RequestException as error:
            # Обработка и вывод ошибки, если запрос неудачен
            print(f"Ошибка запроса: {error}")
            return None

    def display_movie_result(self, result, query):
        if not result:
            raise Exception('Query returned an error')

        movies = []
        # Преобразование JSON-строки в словарь
        data = json.loads(result)
        # Извлечение данных элементов списка results
        for result in data.get("results"):
            # Извлечение нужной информации
            titleType = result.get("titleType", {}).get("text")
            title = result.get("originalTitleText", {}).get("text")
            #poster_url = result.get("primaryImage", {}).get("url")
            release_date_info = result.get("releaseDate", {})
            title_id = result.get("id", {})

            movie = Movie()
            movie.set_query_details(query.get_details())
            movie.set_id(title_id)
            movie.set_name(title)
            if release_date_info:
                day = release_date_info.get("day")
                month = release_date_info.get("month")
                year = release_date_info.get("year")
                movie.set_release_date(f'{day}.{month}.{year}')
            #movie.set_poster_url(poster_url)
            movies.append(movie)

        # Вывод информации
        return movies

    def summary_movie_query(self, query):
        # Форматирование запроса для использования в URL
        formatted_result = self.format_query(query.get_title_name())
        # Получение информации о фильме по отформатированному запросу
        result = self.get_movie_info(formatted_result)
        # Инференс краткой информации о фильме
        return self.display_movie_result(result, query)


class SeriesInfoRetriever:
    def __init__(self):
        # Заголовки для авторизации в API
        self.headers = {
            'X-RapidAPI-Key': RAPIDAPI_KEY,
            'X-RapidAPI-Host': "moviesdatabase.p.rapidapi.com"
        }

    def format_query(self, query):
        # Замена пробелов на "%20"
        formatted_query = query.replace(" ", "%20")
        return formatted_query

    def get_series_info(self, query):
        # Формирование URL запроса с учетом параметров
        url = f"https://moviesdatabase.p.rapidapi.com/titles/search/title/{query}"
        # Параметры запроса
        querystring = {
            "exact": "false",
            "titleType": "tvSeries"
        }
        try:
            # Отправка GET-запроса
            response = requests.get(url, headers=self.headers, params=querystring)
            # Проверка успешности запроса
            response.raise_for_status()
            # Получение текстового содержимого ответа
            data = response.text
            # Возвращение данных
            return data
        except requests.exceptions.RequestException as error:
            # Обработка и вывод ошибки, если запрос неудачен
            print(f"Ошибка запроса: {error}")
            return None

    def display_series_result(self, result, query):
        if not result:
            raise Exception('Query returned an error')

        series_lst = []
        # Преобразование JSON-строки в словарь
        data = json.loads(result)
        # Извлечение данных элементов списка results
        for result in data.get("results"):
            # Извлечение нужной информации
            title = result.get("originalTitleText", {}).get("text")
            release_date_info = result.get("releaseDate", {})
            title_id = result.get("id", {})

            series = Series()
            series.set_name(title)
            series.set_id(title_id)
            series.set_query_details(query.get_details())
            if release_date_info:
                day = release_date_info.get("day")
                month = release_date_info.get("month")
                year = release_date_info.get("year")
                series.set_release_date(f'{day}.{month}.{year}')
            series_lst.append(series)

        # Вывод информации
        return series_lst

    def summary_series_query(self, query):
        # Форматирование запроса для использования в URL
        formatted_result = self.format_query(query.get_title_name())
        # Получение информации о фильме по отформатированному запросу
        result = self.get_series_info(formatted_result)
        # Инференс краткой информации о фильме
        return self.display_series_result(result, query)


class FilterInfoRetriever:
    def __init__(self):
        # Заголовки для авторизации в API
        self.headers = {
            'X-RapidAPI-Key': RAPIDAPI_KEY,
            'X-RapidAPI-Host': "moviesdatabase.p.rapidapi.com"
        }

    def get_title_info(self, query):
        # Формирование URL запроса с учетом параметров
        url = "https://moviesdatabase.p.rapidapi.com/titles"
        # Параметры запроса
        querystring = {
            'titleType': 'movie' if query['title type'] == 'Movie' else 'tvSeries'
        }
        if query['exact year']:
            querystring['year'] = query['exact year']
        if query['start year']:
            querystring['startYear'] = query['start year']
        if query['end year']:
            querystring['endYear'] = query['end year']
        if query['genre']:
            querystring['genre'] = query['genre']
        try:
            # Отправка GET-запроса
            response = requests.get(url, headers=self.headers, params=querystring)
            # Проверка успешности запроса
            response.raise_for_status()
            # Получение текстового содержимого ответа
            data = response.text
            # Возвращение данных
            return data
        except requests.exceptions.RequestException as error:
            # Обработка и вывод ошибки, если запрос неудачен
            print(f"Ошибка запроса: {error}")
            return None

    def display_title_result(self, result, query):
        if not result:
            raise Exception('Query returned an error')

        titles = []
        # Преобразование JSON-строки в словарь
        data = json.loads(result)
        # Извлечение данных элементов списка results
        for result in data.get("results"):
            # Извлечение нужной информации
            title_name = result.get("originalTitleText", {}).get("text")
            release_date_info = result.get("releaseDate", {})
            if query['title type'] == 'Movie':
                title = Movie()
            else:
                title = Series()
            title.set_name(title_name)
            if release_date_info:
                day = release_date_info.get("day")
                month = release_date_info.get("month")
                year = release_date_info.get("year")
                title.set_release_date(f'{day}.{month}.{year}')
            titles.append(title)

        # Вывод информации
        return titles

    def summary_title_query(self, query):
        result = self.get_title_info(query)
        return self.display_title_result(result, query)


class MovieDetailsRetriever:
    def __init__(self):
        # Заголовки для авторизации в API
        self.headers = {
            'X-RapidAPI-Key': RAPIDAPI_KEY,
            'X-RapidAPI-Host': "moviesdatabase.p.rapidapi.com"
        }
        self.details_lst = []
        self.formated_details = ['ratingsSummary', 'awards', 'creators', 'revenue_budget', 'synopses', 'principalCast', 'genres', 'runtime']
        self.not_custom_detail = ['awards', 'revenue_budget', 'synopses']

    def format_query(self, query):
        query_keys = list(query.keys())
        for i in range(len(query_keys)):
            if query[query_keys[i]]:
                self.details_lst.append(self.formated_details[i])


    def get_movie_info(self, title_id):
        url = f"https://moviesdatabase.p.rapidapi.com/titles/{title_id}"
        querystring = {
            "info":"custom_info"
        }
        try:
            # Отправка GET-запроса
            response = requests.get(url, headers=self.headers, params=querystring)
            # Проверка успешности запроса
            response.raise_for_status()
            # Получение текстового содержимого ответа
            data = response.text
            # Возвращение данных
            result = json.loads(data)['results']
        except requests.exceptions.RequestException as error:
            print(f"Ошибка запроса: {error}")
            return None
        for detail in self.not_custom_detail:
            if detail in self.details_lst:
                try:
                    # Отправка GET-запроса
                    response = requests.get(url, headers=self.headers, params={'info':detail})
                    # Проверка успешности запроса
                    response.raise_for_status()
                    # Получение текстового содержимого ответа
                    data = response.text
                    # Возвращение данных
                    result.update(json.loads(data)['results'])
                except requests.exceptions.RequestException as error:
                    # Обработка и вывод ошибки, если запрос неудачен
                    print(f"Ошибка запроса: {error}")
                    return None
        return result

    def display_movie_result(self, data):
        if not data:
            raise Exception('Query returned an error')
        result = {}
        if 'ratingsSummary' in self.details_lst and data.get('ratingsSummary', {}):
            result.update({"ratingsSummary": data.get('ratingsSummary', {})})
        if 'awards' in self.details_lst and data.get('nominations', {}):
            result.update({"awards": data.get('nominations', {}).get('total', {})})
        if 'creators' in self.details_lst and data.get('directors', {}):
            credits_lst = data.get('directors', {})[0].get('credits', {})
            result.update({"creators": [director.get('name', {}).get('nameText', {}).get('text', {}) for director in credits_lst]    })
        if 'revenue_budget' in self.details_lst and data.get('productionBudget', {}):
            result.update({"revenue_budget": {'productionBudget': data.get('productionBudget', {}).get('budget', {}).get('amount', {})  ,
                                              'worldwideGross': data.get('worldwideGross', {}).get('total', {}).get('amount', {})}})
        if 'synopses' in self.details_lst and data.get('synopses', {}).get('edges', {}):
            result.update({"synopses": data.get('synopses', {}).get('edges', {})[0].get('node', {}).get('plotText', {}).get('plaidHtml', {})})
        if 'principalCast' in self.details_lst and data.get('principalCast', {}):
            actor_credits = data.get('principalCast', {})[0].get('credits', {})
            result.update({'principalCast' : [actor.get('name', {}).get("nameText", {}).get('text', {}) for actor in actor_credits]})
            result.update({'roles':[actor.get('characters', {})[0].get("name", {}) for actor in actor_credits] })
        if 'genres' in self.details_lst and data.get('genres', {}):
            genres_lst = data.get('genres', {}).get('genres', {})
            result.update({'genres': [genre.get('text', {}) for genre in genres_lst]})
        if 'runtime' in self.details_lst and data.get('runtime', {}):
            result.update({"runtime": f"{round(data.get('runtime', {}).get('seconds', {})/3600 , 2)}h"})
        return result

    def summary_movie_query(self, query, title_id):
        self.format_query(query)
        result = self.get_movie_info(title_id)
        return self.display_movie_result(result)


def moviedb_query_sync(endpoint):
    baseurl = 'moviesdatabase.p.rapidapi.com'
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': baseurl,
    }
    url = f'https://{baseurl}{endpoint}'
    response = requests.get(url, headers=headers)
    return response.json()['results']


class SyncQueueResults:
    """Класс для синхронной выдачи результатов запроса"""

    def __init__(self, name):
        self._name = name
        self._movies = []
        self._series = []
        self._actors = []
        self._error = None

    def add_movie(self, movie):
        self._movies.append(movie)

    def add_series(self, series):
        self._series.append(series)

    def set_error(self, error):
        self._error = error

    def receive(self, visitor):
        visitor.begin(self._name)
        if self._error:
            visitor.error(self._error)
            visitor.end()
            return
        for movie in self._movies:
            visitor.movie(movie)

        for series in self._series:
            visitor.series(series)

        for actor in self._actors:
            visitor.actor(actor)
        visitor.end()


class AsyncQueueResults:
    """Класс для асинхронной выдачи результатов запроса"""
    def __init__(self, queue, query):
        self._queue = queue
        self._query = query
        self._thread = None

    def receive(self, visitor):
        self._visitor = visitor
        self._thread = Thread(target=self._receive, args=[visitor])
        self._thread.start()

    def _receive(self, visitor):
        results = self._queue.submit(self._query, sync=True)
        results.receive(visitor)

class MoviesDbQueryQueue:
    """Класс очереди запросов к MoviesDb RapidAPI"""

    def __init__(self, url=RAPIDAPI_MOVIESDB_URL):
        self._url = url

    def set_base_url(self, url):
        raise NotImplementedError()

    def query_all_genres(self):
        try:
            genres = moviedb_query_sync('/titles/utils/genres')
            return genres
        except Exception as e:
            print(f'Failed to retrieve genres: {e}', file=sys.stderr)
            print('falling back to predefined list...', file=sys.stderr)
            return MOVIESDB_KNOWN_GENRES

    def submit(self, query, sync):
        if not sync:
            results = AsyncQueueResults(self, query)
            return results

        if query.get_title_type() == 'movie':
            results = SyncQueueResults('Searching for movies...')
            info_retriever = MovieInfoRetriever()

            try:
                movies = info_retriever.summary_movie_query(query)
                for movie in movies:
                    results.add_movie(movie)
            
            except Exception as e:
                print(f'Error while querying: {e}', file=sys.stderr)
                results.set_error(e)
            return results

        elif query.get_title_type() == 'series':
            results = SyncQueueResults('Searching for series...')
            info_retriever = SeriesInfoRetriever()

            try:
                series_lst = info_retriever.summary_series_query(query)
                for series in series_lst:
                    results.add_series(series)

            except Exception as e:
                print(f'Error while querying: {e}', file=sys.stderr)
                results.set_error(e)
            return results

        elif query.get_title_type() is None:
            results = SyncQueueResults('Searching for titles...')
            info_retriever = FilterInfoRetriever()

            try:
                query_filter = query.get_filter()
                if query_filter['title type'] == 'Series':
                    series_lst = info_retriever.summary_title_query(query.get_filter())
                    for series in series_lst:
                        results.add_series(series)
                else:
                    movies = info_retriever.summary_title_query(query.get_filter())
                    for movie in movies:
                        results.add_movie(movie)

            except Exception as e:
                print(f'Error while querying: {e}', file=sys.stderr)
                results.set_error(e)
            return results

