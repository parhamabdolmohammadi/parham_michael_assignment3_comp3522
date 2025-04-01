import abc
import aiohttp
import asyncio
from pokeretriever.pokedex_object import Ability, Pokemon, Move, Stat

# Name: Michael McBride
# Student number: A01394787

# Name: Parham Abdolmohammadi
# Student number: A01356970

class Retriever(abc.ABC):
    """
    Abstract base class for all retrievers that fetch and parse data from the PokéAPI
    and convert it into corresponding PokedexObject instances.
    """

    def __init__(self):
        """
        Initializes the Retriever with a default value for the expanded flag.
        """

        self.is_expanded = None

    async def fetch_data(self, url, requests):
        """
        Fetches and processes data for multiple requests asynchronously.

        Args:
            url (str): Base URL for the API endpoint.
            requests (list[Request]): List of Request objects.

        Returns:
            list[PokedexObject]: List of fully constructed PokedexObject instances.
        """

        async with aiohttp.ClientSession() as session:
            self.is_expanded = requests[0].get_expanded()

            pokedex_object_coroutines = [self.get_request(url, request, session) for request in requests]

            pokedex_object_dict = await asyncio.gather(*pokedex_object_coroutines)

            pokedex_object_separated = [pk_object for pk_object in pokedex_object_dict]

            kwargs_coroutines = [self.parse(pk_object) for pk_object in pokedex_object_separated]

            kwargs_all = await asyncio.gather(*kwargs_coroutines)

            generate_object_coroutines = [self.generate_pokedex_object(**kwargs) for kwargs in kwargs_all]

            return await asyncio.gather(*generate_object_coroutines)

    @staticmethod
    async def fetch_expanded_objects(retriever, urls, session):
        """
        Fetches additional detailed objects (like expanded stats, moves, or abilities).

        Args:
            retriever (Retriever): A retriever instance used to fetch and parse objects.
            urls (list[str]): List of URLs to fetch.
            session (aiohttp.ClientSession): The HTTP session to use.

        Returns:
            list[PokedexObject]: List of parsed and constructed objects.
        """

        pokedex_object_coroutines = [retriever.get_request(url, None, session) for url in urls]
        pokedex_object_dict = await asyncio.gather(*pokedex_object_coroutines)

        kwargs_coroutines = [retriever.parse(obj) for obj in pokedex_object_dict]
        kwargs_all = await asyncio.gather(*kwargs_coroutines)

        generate_object_coroutines = [retriever.generate_pokedex_object(**kwargs) for kwargs in kwargs_all]
        return await asyncio.gather(*generate_object_coroutines)

    async def get_request(self, url, request, session):
        """
        Sends an asynchronous GET request to the API and parses the JSON response.

        Args:
            url (str): Base API endpoint.
            request (Request | None): Request object with input data, or None for expanded objects.
            session (aiohttp.ClientSession): HTTP session for the request.

        Returns:
            dict: Parsed JSON dictionary from the response.
        """

        if not request:
            target_url = url

        else:
            id_number_or_name = request.get_input_data()

            target_url = url + id_number_or_name

        try:
            response = await session.request(method="GET", url=target_url)
            json_dict = await response.json()

        except aiohttp.ContentTypeError:
            return {}

        else:

            return json_dict

    @abc.abstractmethod
    async def parse(self, json):
        """
        Parses a JSON response dictionary into keyword arguments for object construction.

        Args:
            json (dict): JSON dictionary to parse.

        Returns:
            dict: Parsed keyword arguments.
        """

        pass

    @abc.abstractmethod
    async def generate_pokedex_object(self, **kwargs):
        """
        Constructs and returns a PokedexObject using parsed keyword arguments.

        Args:
            **kwargs: Keyword arguments needed to construct the object.

        Returns:
            PokedexObject: The constructed domain object.
        """

        pass


class AbilityRetriever(Retriever):
    """
    Retriever class responsible for fetching and constructing Ability objects.
    """

    async def parse(self, json):
        """
        Parses a JSON dictionary into keyword arguments for an Ability object.

        Args:
            json (dict): API response containing ability data.

        Returns:
            dict: Parsed keyword arguments.
        """

        kwargs = {}
        try:
            kwargs["name"] = json["name"]
            kwargs["id"] = json["id"]
            kwargs["generation"] = json["generation"]["name"]
            kwargs["effect"] = json["effect_entries"][1]["effect"]
            kwargs["effect_short"] = json["effect_entries"][1]["short_effect"]
            pokemon_list = json["pokemon"]
            kwargs["pokemon"] = [pokemon["pokemon"]["name"]for pokemon in pokemon_list]
        except KeyError:
            return {}
        else:
            return kwargs

    @staticmethod
    async def generate_pokedex_object(**kwargs):
        """
        Constructs and returns an Ability object from keyword arguments.

        Args:
            **kwargs: Keyword arguments required for Ability construction.

        Returns:
            Ability: Constructed Ability object or error string on failure.
        """

        try:
            new_ability = Ability(**kwargs)
        except KeyError:
            return "An error occurred. Skipping this request.\n"
        else:
            return new_ability


class MoveRetriever(Retriever):
    """
    Retriever class responsible for fetching and constructing Move objects.
    """

    async def parse(self, json):
        """
        Parses a JSON dictionary into keyword arguments for a Move object.

        Args:
            json (dict): API response containing move data.

        Returns:
            dict: Parsed keyword arguments.
        """

        kwargs = {}
        try:
            kwargs["name"] = json["name"]
            kwargs["id"] = json["id"]
            kwargs["generation"] = json["generation"]["name"]
            kwargs["accuracy"] = json["accuracy"]
            kwargs["pp"] = json["pp"]
            kwargs["power"] = json["power"]
            kwargs["type"] = json["type"]["name"]
            kwargs["damage_class"] = json["damage_class"]["name"]
        except KeyError:
            return {}
        else:
            try:
                kwargs["effect"] = json["effect_entries"][0]["short_effect"]
            except IndexError:
                kwargs["effect"] = None
            return kwargs

    @staticmethod
    async def generate_pokedex_object(**kwargs):
        """
        Constructs and returns a Move object from keyword arguments.

        Args:
            **kwargs: Keyword arguments required for Move construction.

        Returns:
            Move: Constructed Move object or error string on failure.
        """

        try:
            new_move = Move(**kwargs)
        except KeyError:
            return "\nAn error occurred. Skipping this request."
        else:
            return new_move


class PokemonRetriever(Retriever):
    """
    Retriever class responsible for fetching and constructing Pokemon objects.
    """

    async def parse(self, json):
        """
        Parses a JSON dictionary into keyword arguments for a Pokemon object.

        Args:
            json (dict): API response containing Pokémon data.

        Returns:
            dict: Parsed keyword arguments.
        """

        kwargs = {}
        try:
            kwargs["name"] = json["name"]
            kwargs["id"] = json["id"]
            kwargs["height"] = json["height"]
            kwargs["weight"] = json["weight"]
            kwargs["types"] = [pk_type["type"]["name"] for pk_type in json["types"]]
        except KeyError:
            return {}
        else:
            if not self.is_expanded:
                stats = [(stat["stat"]["name"], stat["base_stat"]) for stat in json["stats"]]

            else:
                stat_retriever = StatRetriever()
                urls = [stat["stat"]["url"] for stat in json["stats"]]
                async with aiohttp.ClientSession() as session:
                    stats = await Retriever.fetch_expanded_objects(stat_retriever, urls, session)

            kwargs["stats"] = stats

            if not self.is_expanded:
                abilities = [ability["ability"]["name"] for ability in json["abilities"]]
            else:
                ability_retriever = AbilityRetriever()
                urls = [ability["ability"]["url"] for ability in json["abilities"]]
                async with aiohttp.ClientSession() as session:
                    abilities = await Retriever.fetch_expanded_objects(ability_retriever, urls, session)

            kwargs["abilities"] = abilities

            if not self.is_expanded:
                moves = [(f"Move Name: {move['move']['name']}",
                          f"Level acquired: {move['version_group_details'][0]['level_learned_at']}") for move in json["moves"]]
            else:
                move_retriever = MoveRetriever()
                urls = [move["move"]["url"] for move in json["moves"]]
                async with aiohttp.ClientSession() as session:
                    moves = await Retriever.fetch_expanded_objects(move_retriever, urls, session)

            kwargs["moves"] = moves

            return kwargs

    async def generate_pokedex_object(self, **kwargs):
        """
        Constructs and returns a Pokemon object from keyword arguments.

        Args:
            **kwargs: Keyword arguments required for Pokemon construction.

        Returns:
            Pokemon: Constructed Pokemon object or error string on failure.
        """

        try:
            new_pokemon = Pokemon(**kwargs)
        except KeyError:
            return "\nAn error occurred. Skipping this request."
        else:
            return new_pokemon


class StatRetriever(Retriever):
    """
    Retriever class responsible for fetching and constructing Stat objects.
    """

    async def parse(self, json):
        """
        Parses a JSON dictionary into keyword arguments for a Stat object.

        Args:
            json (dict): API response containing stat data.

        Returns:
            dict: Parsed keyword arguments.
        """

        kwargs = {}
        try:
            kwargs["name"] = json["name"]
            kwargs["id"] = json["id"]
            kwargs["is_battle_only"] = json["is_battle_only"]
        except KeyError:
            return {}
        else:
            try:
                kwargs["move_damage_class"] = json["move_damage_class"]["name"]
            except TypeError:
                kwargs["move_damage_class"] = "N/A"
            return kwargs


    async def generate_pokedex_object(self, **kwargs):
        """
        Constructs and returns a Stat object from keyword arguments.

        Args:
            **kwargs: Keyword arguments required for Stat construction.

        Returns:
            Stat: Constructed Stat object or error string on failure.
        """

        try:
            new_stat = Stat(**kwargs)
        except KeyError:
            return "\nAn error occurred. Skipping this request."
        else:
            return new_stat
