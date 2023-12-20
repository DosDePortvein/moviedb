from .queue import MoviesDbQueryQueue, RAPIDAPI_MOVIESDB_URL
from .gui import Gui


class Application:
    def __init__(self):
        self._queue = MoviesDbQueryQueue(RAPIDAPI_MOVIESDB_URL)
        self._gui = Gui()
        self._gui.set_queue(self._queue)
        print('Application::constructor')

    def run(self):
        print('Applcation::run')
        return self._gui.run()
