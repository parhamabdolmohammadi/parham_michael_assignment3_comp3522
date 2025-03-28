import requests

from pokedex_object import PokedexObject
from request import Request


class PokedexRetrieverFacade:

    BASE_URL = "https://pokeapi.co/api/v2"

    RETRIEVERS: dict[str, tuple[str, str]] = {
        "pokemon": ("PokemonRetriever", BASE_URL + "pokemon/{}"),
        "ability": ("AbilityRetriever", BASE_URL + "ability/{}"),
        "move": ("MoveRetriever", BASE_URL + "move/{}")
    }


    def __init__(self, requests: list[Request]):
        self.requests = requests
        self.pokedex_data: list[PokedexObject] = []
        self.retriever = None



    def execute_request(self, request: list[Request]) -> list[PokedexObject]:


        for request in requests:
            retriever_info = PokedexRetrieverFacade.RETRIEVERS.get(request.mode)

            self.retriever = retriever_info[0]
            url = retriever_info[1]



            # current_data = retriever.executerequest(url, request.input_data)
            #self.pokedex_data.apppend(current_data)




