import requests

class Poster:

    def __init__(self, name):
        self.url = requests.get('https://api.themoviedb.org/3/search/'
                                'movie?api_key=15d2ea6d0dc1d476efbca3e'
                                'ba2b9bbfb&query={}'.format(name))
        self.name = name

        self.data = self.url.json()

    def print_data(self):
        print(self.data)

    def get_data_results(self, key='poster_path'):
        return self.data['results'].pop().get(key, None)

    def exists(self):
        return self.data.get('total_results', 0) > 0

    def poster_path(self):
        if self.exists():
            return "http://image.tmdb.org/t/p/w500/" + self.get_data_results()
        else:
            return None

