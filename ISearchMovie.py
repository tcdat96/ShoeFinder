import abc

class ISearchMovie(abc.ABC):
    @abc.abstractmethod
    def getMovies(self, title):
    	raise NotImplementedError
