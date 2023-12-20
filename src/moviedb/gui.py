from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook, Combobox

from .queue import Query
from .queue.queue import MovieDetailsRetriever


class DetailsWindow:
    def __init__(self, parent, title_name, query_result):
        self.root = Toplevel(parent)
        self.root.title(f'{title_name} details')
        self.query_result = query_result

    def draw_widgets(self):
        key_lst = list(self.query_result.keys())
        for key in key_lst:
            if key == 'creators':
                Label(self.root, text=key, font=('Arial 18')).pack(anchor=N)
                for creator in self.query_result[key]:
                    Label(self.root, text=creator, font=('Arial 14')).pack(anchor=N)
            elif key == 'revenue_budget':
                Label(self.root, text=key, font=('Arial 18')).pack(anchor=N)
                budget_text = f'Production budget = {self.query_result[key]["productionBudget"]} USD\n'  \
                              f'Worldwide Gross = {self.query_result[key]["worldwideGross"]} USD'
                Label(self.root, text=budget_text, font=('Arial 14')).pack(anchor=N)
            elif key == 'principalCast':
                Label(self.root, text=key, font=('Arial 18')).pack(anchor=N)
                actors_lst = self.query_result[key]
                roles_lst = self.query_result['roles']
                actors_text = ""
                if len(actors_lst) == len(roles_lst):
                    for i in range(len(actors_lst)):
                        actors_text += f'{actors_lst[i]} as {roles_lst[i]}, '
                else:
                    for i in range(len(actors_lst)):
                        actors_text += f'{actors_lst[i]}, '
                Label(self.root, text=actors_text[0:-2], font=('Arial 14')).pack(anchor=N)
            elif key == 'genres':
                Label(self.root, text=key, font=('Arial 18')).pack(anchor=N)
                g_lst = self.query_result[key]
                genres_text = ""
                for g in g_lst:
                    genres_text += g + ', '
                Label(self.root, text=genres_text[0:-2], font=('Arial 14')).pack(anchor=N)
            elif key == 'roles':
                continue
            elif key == 'ratingsSummary':
                Label(self.root, text=key, font=('Arial 18')).pack(anchor=N)
                ratings_summary_text = f'Agregate rating = {self.query_result[key]["aggregateRating"]}, number of votes ={self.query_result[key]["voteCount"]}'
                Label(self.root, text=ratings_summary_text, font=('Arial 14')).pack(anchor=N)
            else:
                Label(self.root, text=key, font=('Arial 18')).pack(anchor=N)
                Label(self.root, text=self.query_result[key], font=('Arial 14')).pack(anchor=N)



class GuiQueryResultVisitor:
    """Этот класс получает хэндл (например) окна, чтобы иметь возможность"""
    """отрисовывать результаты по мере их получения"""
    def __init__(self, window):
        self._window = window
        self._counter = 0
        self._subwindow = None
        self._frame = None
        self._pack = { 'expand': 1, 'side': TOP, 'fill': X, 'anchor': N }
        self._may_have_no_actors = False

    def begin(self, name):
        if self._subwindow is None:
            self._subwindow = Toplevel(self._window)
            self._subwindow.title(name)
            self._subwindow.minsize(300, 400)
            self._subwindow.columnconfigure(0, weight=1)
            self._subwindow.rowconfigure(0, weight=1)
            self._subwindow.rowconfigure(1, weight=1)
            canvas = Canvas(self._subwindow)
            canvas.grid(column=0, row=0, sticky='news')
            scrollbar = Scrollbar(self._subwindow, orient='vertical')
            scrollbar.grid(column=1, row=0, sticky='nes')
            scrollbar.config(command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
            self._frame = Frame(canvas)
            self._frame.pack(**self._pack)

    def _make_new_section(self):
        self._counter = self._counter + 1
        section = LabelFrame(self._frame, text=f'Query results #{self._counter}')
        section.pack(**self._pack)
        return section

    def _actor_info(self, parent, actor):
        Label(parent, text=actor.full_name()).pack()

    def _movie_info(self, parent, movie):
        titleframe = LabelFrame(parent, text='Title')
        titleframe.pack(expand=1, fill=X, side=TOP, anchor=N)

        Label(titleframe, text=movie.name()).pack(**self._pack)

        released = LabelFrame(parent, text='Release date')
        released.pack(**self._pack)
        if movie.released():
            Label(released, text=movie.released()).pack(expand=1, fill=X)
        else:
            Label(released, text='Release date unknown').pack(expand=1, fill=X)

        if self._may_have_no_actors and len(movie.actors()) == 0:
            return

        actorinfo = LabelFrame(parent, text='Actors')
        actorinfo.pack(**self._pack)

        for actor in movie.actors():
            self._actor_info(actorinfo, actor)
        if len(movie.actors()) == 0:
            Label(actorinfo, text='There are no actors info for this movie').pack(expand=1)
        Button(parent, text=f'Подробнее', command=lambda id=movie.id(), details=movie.query_details(), title_name = movie.name()
        : self.show_details(id, details, title_name)).pack()

    def show_details(self, id, details, title_name):
        movie_details_retriever = MovieDetailsRetriever()
        result =  movie_details_retriever.summary_movie_query(details, id)

        self.create_details_window(self._window, title_name, result)

    def create_details_window(self, parent, title_name, result):
        details_window = DetailsWindow(parent, title_name, result)
        details_window.draw_widgets()


    def _series_info(self, parent, series):
        titleframe = LabelFrame(parent, text='Title')
        titleframe.pack(expand=1, fill=X, side=TOP, anchor=N)

        Label(titleframe, text=series.name()).pack(**self._pack)

        released = LabelFrame(parent, text='Release date')
        released.pack(**self._pack)
        if series.released():
            Label(released, text=series.released()).pack(expand=1, fill=X)
        else:
            Label(released, text='Release date unknown').pack(expand=1, fill=X)

        if self._may_have_no_actors and len(series.actors()) == 0:
            return

        actorinfo = LabelFrame(parent, text='Actors')
        actorinfo.pack(**self._pack)

        for actor in series.actors():
            self._actor_info(actorinfo, actor)
        if len(series.actors()) == 0:
            Label(actorinfo, text='There are no actors info for this movie').pack(expand=1)
        Button(parent, text=f'Подробнее',
               command=lambda id=series.id(), details=series.query_details(), title_name=series.name()
               : self.show_details(id, details, title_name)).pack()

    def movie(self, movie):
        self._may_have_no_actors = False
        section = self._make_new_section()
        self._movie_info(section, movie)

    def series(self, series):
        self._may_have_no_actors = False
        section = self._make_new_section()
        self._series_info(section, series)

    def actor(self, actor):
        self._may_have_no_actors = False
        section = self._make_new_section()
        actorinfo = LabelFrame(section, text='Actor')
        actorinfo.pack(**self._pack)
        self._actor_info(actorinfo, actor)

    def error(self, error):
        section = self._make_new_section()
        Label(section, text=f'Query returned error: \'{error}\'')

    def end(self):
        if self._counter == 0:
            Label(self._frame, text='Query returned no results :(').pack(**self._pack)
        self._subwindow = None


class Gui:
    """Класс связывает вместе пользовательский ввод и очереди"""
    def __init__(self):
        self._queue = None
        self._window = Tk()
        self._window.title("MovieDb")
        self._window.geometry(f'600x700')

        self.tabs_control = Notebook(self._window)
        self.tab_film_search = Frame(self.tabs_control)
        self.tab_series_search = Frame(self.tabs_control)
        self.tab_title_filter = Frame(self.tabs_control)

        self.tabs_control.add(self.tab_film_search, text='Film search')
        self.tabs_control.add(self.tab_series_search, text='Series search')
        self.tabs_control.add(self.tab_title_filter, text='Title filter')

        self.entry_film_name = Entry(self.tab_film_search, font='Arial 18')
        self.film_additional_information = (
        ('Rating IMDb', IntVar()), ('Awards', IntVar()), ('Creators', IntVar()), ('Budget', IntVar()),
        ('Synopsis', IntVar()), ('Actors', IntVar()), ('Genre', IntVar()), ('Duration', IntVar()))

        self.entry_series_name = Entry(self.tab_series_search, font='Arial 18')
        self.series_additional_information = (
        ('Rating IMDb', IntVar()), ('Awards', IntVar()), ('Creators', IntVar()), ('Budget', IntVar()),
        ('Synopsis', IntVar()), ('Actors', IntVar()), ('Genre', IntVar()), ('Duration', IntVar()),
        ('Seasons and episodes', IntVar()))

        self.title_filter_exact_year_spinbox = Entry(self.tab_title_filter, font='Arial 18')
        # initially no genres, will push more later
        self.title_filter_genre_combobox = Combobox(self.tab_title_filter, values=[], state='readonly', font='Arial 18')
        self.title_filter_start_year_spinbox = Entry(self.tab_title_filter, font='Arial 18')
        self.title_filter_end_year_spinbox = Entry(self.tab_title_filter, font='Arial 18')
        self.title_filter_type_combobox = Combobox(self.tab_title_filter, values=['Movie', 'Series'], state='readonly', font='Arial 18')
        self.title_filter_type_combobox.current(0)

    def set_queue(self, queue):
        self._queue = queue
        self.title_filter_genre_combobox['values'] = tuple(queue.query_all_genres())

    def draw_widgets(self):
        self.tabs_control.pack(fill=BOTH, expand=0)

        Label(self.tab_film_search, text='Enter film name:', font='Arial 20').pack(anchor=N + W)
        self.entry_film_name.pack(anchor=N+W)
        Label(self.tab_film_search, text='Show additional information:', font='Arial 20').pack(anchor=N + W)
        for name, var in self.film_additional_information:
            Checkbutton(self.tab_film_search, text=name, variable=var, font='Arial 18').pack(anchor=N+W)
        Button(self.tab_film_search, text='Search', font='Arial 18', command=self._film_search).pack(anchor=S)

        Label(self.tab_series_search, text='Enter series name:', font='Arial 20').pack(anchor=N + W)
        self.entry_series_name.pack(anchor=N + W)
        Label(self.tab_series_search, text='Show additional information:', font='Arial 20').pack(anchor=N + W)
        for name, var in self.series_additional_information:
            Checkbutton(self.tab_series_search, text=name, variable=var, font='Arial 18').pack(anchor=N + W)
        Button(self.tab_series_search, text='Search', font='Arial 18', command=self._series_search).pack(anchor=S)

        Label(self.tab_title_filter, text='Filter parameters:', font='Arial 20').pack(anchor=N + W)
        Label(self.tab_title_filter, text='Exact year:', font='Arial 18').pack(anchor=N + W)
        self.title_filter_exact_year_spinbox.pack(anchor=N + W)
        Label(self.tab_title_filter, text='Genre:', font='Arial 18').pack(anchor=N + W)
        self.title_filter_genre_combobox.pack(anchor=N + W)
        Label(self.tab_title_filter, text='Start year:', font='Arial 18').pack(anchor=N + W)
        self.title_filter_start_year_spinbox.pack(anchor=N + W)
        Label(self.tab_title_filter, text='End year:', font='Arial 18').pack(anchor=N + W)
        self.title_filter_end_year_spinbox.pack(anchor=N + W)
        Label(self.tab_title_filter, text='Title type:', font='Arial 18').pack(anchor=N + W)
        self.title_filter_type_combobox.pack(anchor=N + W)
        Button(self.tab_title_filter, text='Search', font='Arial 18', command=self._title_filter_search).pack(anchor=S)


    def run(self):
        """Метод запускает цикл обработки графики и завершается при закрытии окна"""
        if self._queue is None:
            raise Exception('Queue is not set')

        self.draw_widgets()
        self._window.mainloop()

    def _film_search(self):
        name = self.entry_film_name.get()
        if not name or len(name) == 0:
            messagebox.showerror('Error!', 'Movie name is not provided')
            return

        parameters = {'title_type':'movie', 'name':name, 'details':{}, 'filter':None}
        for name, var in self.film_additional_information:
            parameters['details'].update({name: var.get()})
        if not parameters['details']:
            parameters['details'] = None
        self.on_search(parameters)

    def _series_search(self):
        name = self.entry_series_name.get()
        if not name or len(name) == 0:
            messagebox.showerror('Error!', 'Series name is not provided')
            return

        parameters = {'title_type': 'series', 'name': self.entry_series_name.get(), 'details': {}, 'filter': None}
        for name, var in self.series_additional_information:
            parameters['details'].update({name: var.get()})
        if not parameters['details']:
            parameters['details'] = None
        self.on_search(parameters)

    def _title_filter_search(self):
        genre = self.title_filter_genre_combobox.get()
        start_year = self.title_filter_start_year_spinbox.get()
        end_year = self.title_filter_end_year_spinbox.get()
        exact_year = self.title_filter_exact_year_spinbox.get()
        title_type = self.title_filter_type_combobox.get()

        if start_year and end_year and exact_year:
            if start_year != end_year and start_year != exact_year:
                messagebox.showerror('Error!', 'Start year, end year and exact year do not match')
                return
            start_year = None
            end_year = None

        if start_year and exact_year or end_year and exact_year:
            messagebox.showerror('Error!', 'Exact year and start/end year are specified simultaneously')
            return

        parameters = {'title_type': None, 'name': None, 'details': None, 'filter': {}}
        parameters['filter'] = {'exact year': exact_year, 'genre': genre, 'start year': start_year, 'end year': end_year, 'title type': title_type}
        self.on_search(parameters)

    def on_search(self, parameters):
        """Эта функция вызывается в обработчике ввода, например когда"""
        """пользователь нажал 'поиск'"""
        query = self.build_query(parameters)
        results = self._queue.submit(query, sync=False)

        visitor = GuiQueryResultVisitor(self._window)
        results.receive(visitor)

    def build_query(self, parameters):
        """Эта функция создает Query из пользовательских данных"""
        query = Query()
        query.set_title_type(parameters['title_type'])
        query.set_title_name(parameters['name'])
        query.set_details(parameters['details'])
        query.set_filter(parameters['filter'])
        return query

