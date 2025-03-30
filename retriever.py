import abc
import aiohttp
import asyncio

from pokedex_object import Ability, Pokemon, Move, Stat


class Retriever(abc.ABC):

    def __init__(self):
        self.is_expanded = None

    async def fetch_data(self, url, requests):
        async with aiohttp.ClientSession() as session:
            self.is_expanded = requests[0].expanded

            #list of couroutines prepared to be called
            pokedex_object_coroutines = [self.get_request(url, request, session) for request in requests]
            # print(pokedex_object_coroutines)

            # responses in list of [json_dict, jsondict, .... ]  format (the big json that you see in https://pokeapi.co/api/v2/ability/drizzle for each request
            pokedex_object_dict = await asyncio.gather(*pokedex_object_coroutines)
            # print("pokedex_object_dict:")
            # print(pokedex_object_dict)
            # print("")


            pokedex_object_separated = [pk_object for pk_object in pokedex_object_dict]
            # print("pokedex_object_separated:")
            # print(pokedex_object_separated)
            # print("")

            #coroutine (of calls to parse()
            kwargs_coroutines = [self.parse(pk_object) for pk_object in pokedex_object_separated]
            # print("kwargs_coroutines:")
            # print(kwargs_coroutines)
            # print("")

            # dict of w (extracting the things we want from the fetched json from the specified api
            kwargs_all = await asyncio.gather(*kwargs_coroutines)
            # print("kwargs_all:")
            # print(kwargs_all)
            # print("")

            #instantiate the corresponding object with the fetched stuff
            #TODO: validate if the dictionary has everytihing that we're looking for, otherwise, get rid of it
            generate_object_coroutines = [self.generate_pokedex_object(**kwargs) for kwargs in kwargs_all]

            return await asyncio.gather(*generate_object_coroutines)

    @staticmethod
    async def fetch_expanded_objects(retriever, urls, session):
        pokedex_object_coroutines = [retriever.get_request(url, None, session) for url in urls]
        pokedex_object_dict = await asyncio.gather(*pokedex_object_coroutines)

        kwargs_coroutines = [retriever.parse(obj) for obj in pokedex_object_dict]
        kwargs_all = await asyncio.gather(*kwargs_coroutines)

        generate_object_coroutines = [retriever.generate_pokedex_object(**kwargs) for kwargs in kwargs_all]
        return await asyncio.gather(*generate_object_coroutines)


    async def get_request(self, url, request, session):

        target_url = ""
        if not request:
            target_url = url

        else:
            id_number_or_name = request.input_data
            # print("id_number_or_name::")
            # print(id_number_or_name) # for debugging only
            # print("")

            target_url = url + id_number_or_name
            # print("target_url::")
            # print(f"getting url: {target_url}") # for debugging only
            # print("")

        response = await session.request(method="GET", url=target_url)
        # print("Response:")
        # print(response)
        # print("")

        json_dict = await response.json()
        # print("response in dict format response.json: ")
        # print(json_dict) # for debugging only
        # print("")

        return json_dict

    @abc.abstractmethod
    async def parse(self, json):
        pass

    @abc.abstractmethod
    async def generate_pokedex_object(self, **kwargs):
        pass


class AbilityRetriever(Retriever):

    async def parse(self, json):
        kwargs = {}
        kwargs["name"] = json["name"]
        kwargs["id"] = json["id"]
        kwargs["generation"] = json["generation"]["name"]
        kwargs["effect"] = json["effect_entries"][1]["effect"]
        kwargs["effect_short"] = json["effect_entries"][1]["short_effect"]
        pokemon_list = json["pokemon"]
        kwargs["pokemon"] = [pokemon["pokemon"]["name"]for pokemon in pokemon_list]
        return kwargs

    @staticmethod
    async def generate_pokedex_object(**kwargs):
        return Ability(**kwargs)


class MoveRetriever(Retriever):

    async def parse(self, json):
        kwargs = {}
        kwargs["name"] = json["name"]
        kwargs["id"] = json["id"]
        kwargs["generation"] = json["generation"]["name"]
        kwargs["accuracy"] = json["accuracy"]
        kwargs["pp"] = json["pp"]
        kwargs["power"] = json["power"]
        kwargs["type"] = json["type"]["name"]
        kwargs["damage_class"] = json["damage_class"]["name"]
        try:
            kwargs["effect"] = json["effect_entries"][0]["short_effect"]
        except IndexError:
            kwargs["effect"] = None



        return kwargs

    @staticmethod
    async def generate_pokedex_object(**kwargs):
        return Move(**kwargs)

class PokemonRetriever(Retriever):
    async def parse(self, json):
        kwargs = {}
        kwargs["name"] = json["name"]
        kwargs["id"] = json["id"]
        kwargs["height"] = json["height"]
        kwargs["weight"] = json["weight"]


        kwargs["types"] = [type["type"]["name"] for type in json["types"]]


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
            moves = [(f"Move Name: {move['move']['name']}", f"Level acquired: {move['version_group_details'][0]['level_learned_at']}") for move in json["moves"]]
        else:
            move_retriever = MoveRetriever()
            urls = [move["move"]["url"] for move in json["moves"]]
            async with aiohttp.ClientSession() as session:
                moves = await Retriever.fetch_expanded_objects(move_retriever, urls, session)

        kwargs["moves"] = moves

        return kwargs



    async def generate_pokedex_object(self, **kwargs):
        return Pokemon(**kwargs)


class StatRetriever(Retriever):

    async def parse(self, json):
        kwargs = {}
        kwargs["name"] = json["name"]
        kwargs["id"] = json["id"]
        kwargs["is_battle_only"] = json["is_battle_only"]
        try:
            kwargs["move_damage_class"] = json["move_damage_class"]["name"]
        except TypeError:
            kwargs["move_damage_class"] = "N/A"

        return kwargs

    async def generate_pokedex_object(self, **kwargs):
        return Stat(**kwargs)
