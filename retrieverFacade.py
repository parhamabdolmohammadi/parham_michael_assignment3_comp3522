# Name: Michael McBride
# Student number: A01394787
# Name: Parham Abdolmohammadi
# Student number: A01356970

from pokedex_object import PokedexObject
from request import Request
from retriever import PokemonRetriever, AbilityRetriever, MoveRetriever, Retriever


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

        self.pokedex_data: list[PokedexObject] = []

    async def execute_request(self, requests: list[Request]):
        """
        Executes a list of API requests using the appropriate retriever based on the request mode.

        Args:
            requests (list[Request]): A list of Request objects specifying the type and ID or name to fetch.

        Returns:
            list[PokedexObject]: A list of PokedexObject instances retrieved from the API.
        """

        mode = requests[0].mode
        retriever_information = self.RETRIEVERS[mode]
        self.retriever = retriever_information[0]
        url = retriever_information[1]

        self.pokedex_data = await self.retriever.fetch_data(url, requests)

        return self.pokedex_data
