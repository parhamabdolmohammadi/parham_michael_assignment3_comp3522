import requests

from pokedex_object import PokedexObject
from request import Request
from retriever import PokemonRetriever, AbilityRetriever, MoveRetriever, Retriever


class PokedexRetrieverFacade:

    BASE_URL = "https://pokeapi.co/api/v2/"

    RETRIEVERS: dict[str, tuple[Retriever, str]] = {
        "pokemon": (PokemonRetriever(), BASE_URL + "pokemon/"),
        "ability": (AbilityRetriever(), BASE_URL + "ability/"),
        "move": (MoveRetriever(), BASE_URL + "move/")
    }


    def __init__(self):
        self.pokedex_data: list[PokedexObject] = []
        self.retriever : Retriever = None
        pokedex_object = []


    async def execute_request(self, requests: list[Request]):

        mode = requests[0].mode
        retriever_information =  self.RETRIEVERS[mode]
        self.retriever = retriever_information[0]
        url = retriever_information[1]

        self.pokedex_data = await self.retriever.fetch_data(url, requests)
        [print(pk_object) for pk_object in self.pokedex_data]


    def output_data(self, file_name):
        pass








