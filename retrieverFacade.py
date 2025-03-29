import requests

from pokedex_object import PokedexObject
from request import Request
from retriever import PokemonRetriever, AbilityRetriever, MoveRetriever, Retriever


class PokedexRetrieverFacade:

    BASE_URL = "https://pokeapi.co/api/v2"

    RETRIEVERS: dict[str, tuple[str, str]] = {
        "pokemon": (PokemonRetriever(), BASE_URL + "pokemon/{}"),
        "ability": (AbilityRetriever(), BASE_URL + "ability/{}"),
        "move": (MoveRetriever(), BASE_URL + "move/{}")
    }


    def __init__(self, requests: list[Request]):
        self.requests = requests
        self.pokedex_data: list[PokedexObject] = []
        self.retriever : Retriever = None



    def execute_request(self, requests: list[Request]):

        mode = requests[0].mode
        retriever_information =  self.RETRIEVERS[mode]
        self.retriever = retriever_information[0]
        url = retriever_information[1]


        self.pokedex_data =  self.retriever.fetch_data(url, requests)


    def output_data(self, file_name):
        pass








