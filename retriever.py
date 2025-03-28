import abc
import requests


class Retriever(abc.ABC):
    @abc.abstractmethod
    def fetch_data(self, session, id):
        pass

    @abc.abstractmethod
    def parse(self, json):
        pass


class PokemonRetriever(Retriever):
    def fetch_data(self, session, id):
        pass

    def parse(self, json):
        pass


class AbilityRetriever(Retriever):
    def fetch_data(self, session, id):
        pass

    def parse(self, json):
        pass


class MoveRetriever(Retriever):
    def fetch_data(self, session, id):
        pass

    def parse(self, json):
        pass


class StatRetriever(Retriever):

    def fetch_data(self, session, id):
        pass

    def parse(self, json):
        pass
