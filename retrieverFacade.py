# Name: Michael McBride
# Student number: A01394787
# Name: Parham Abdolmohammadi
# Student number: A01356970

from pokeretriever.pokedex_object import PokedexObject
from pokeretriever.request import Request
from pokeretriever.retriever import PokemonRetriever, AbilityRetriever, MoveRetriever, Retriever


class PokedexRetrieverFacade:
    """
    Facade class that simplifies retrieval of various Pokédex objects such as Pokémon, abilities, and moves.
    It delegates the API requests to the appropriate retriever based on the request mode.
    """

    BASE_URL = "https://pokeapi.co/api/v2/"

    RETRIEVERS: dict[str, tuple[Retriever, str]] = {
        "pokemon": (PokemonRetriever(), BASE_URL + "pokemon/"),
        "ability": (AbilityRetriever(), BASE_URL + "ability/"),
        "move": (MoveRetriever(), BASE_URL + "move/")
    }

    retriever: Retriever

    def __init__(self):
        """
        Initializes the PokedexRetrieverFacade with an empty list to store Pokédex data.
        """

        self.__pokedex_data: list[PokedexObject] = []

    async def execute_request(self, requests: list[Request]):
        """
        Executes a list of API requests using the appropriate retriever based on the request mode.

        Args:
            requests (list[Request]): A list of Request objects specifying the type and ID or name to fetch.

        Returns:
            list[PokedexObject]: A list of PokedexObject instances retrieved from the API.
        """

        mode = requests[0].get_mode()
        retriever_information = self.RETRIEVERS[mode]
        self.__retriever = retriever_information[0]
        url = retriever_information[1]

        self.__pokedex_data = await self.__retriever.fetch_data(url, requests)

        return self.__pokedex_data
