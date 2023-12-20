
class QueryFilter:
    """Фильтр для получения тайтлов по фильтру"""
    def __init__(self):
        self._start_year = None
        self._end_year = None
        self._genre = None
        self.exact_year = None

    def set_exact_year(self, year):
        self.exact_year = year

    def set_start_year(self, year):
        self._start_year = year

    def set_end_year(self, year):
        self._end_year = year

    def get_start_year(self):
        return self._start_year

    def get_end_year(self):
        return self._end_year

    def set_genre(self, genre):
        self._genre = genre


class QueryDetails:
    """Класс для указания базовой информации о тайтле для поиска"""
    def __init__(self, details):
        self.details = details


class Query:
    """Класс хранит в себе информацию о том, что искать"""
    def __init__(self):
        self._title = None
        self._title_type = None
        self._title_name = None
        self._details = None
        self._filter = None
        pass

    def set_title(self, _title):
        self._title = _title

    def get_title(self):
        return self._title

    def set_details(self, _details):
        self._details = QueryDetails(_details)

    def get_details(self):
        return self._details.details

    def set_filter(self, _filter):
        self._filter = _filter

    def get_filter(self):
        return self._filter

    def set_title_name(self, _title_name):
        self._title_name = _title_name

    def get_title_name(self):
        return self._title_name

    def set_title_type(self, _title_type):
        self._title_type = _title_type

    def get_title_type(self):
        return self._title_type
