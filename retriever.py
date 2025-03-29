import abc
import aiohttp
import asyncio

from pokedex_object import Ability, Pokemon, Move, Stat


class Retriever(abc.ABC):
    async def fetch_data(self, url, requests):
        async with aiohttp.ClientSession() as session:
            pokedex_object_coroutines = [self.get_request(url, request, session) for request in requests]
            pokedex_object_dict = await asyncio.gather(*pokedex_object_coroutines)
            pokedex_object_separated = [pk_object for pk_object in pokedex_object_dict]
            kwargs_coroutines = [self.parse(pk_object) for pk_object in pokedex_object_separated]
            kwargs_all = await asyncio.gather(*kwargs_coroutines)
            # print(f"kwargs_all: {kwargs_all}") # for debugging only
            generate_object_coroutines = [self.generate_pokedex_object(**kwargs) for kwargs in kwargs_all]
            return await asyncio.gather(*generate_object_coroutines)

    async def get_request(self, url, request, session):
        id_number = request.input_data
        # print(id_number) # for debugging only
        target_url = url + id_number
        # print(target_url) # for debugging only
        # print(f"getting url: {target_url}") # for debugging only
        response = await session.request(method="GET", url=target_url)
        json_dict = await response.json()
        # print(json_dict) # for debugging only
        return json_dict

    @abc.abstractmethod
    async def parse(self, json):
        pass

    @abc.abstractmethod
    async def generate_pokedex_object(self, **kwargs):
        pass


class PokemonRetriever(Retriever):
    # pokemon_data = request.get(url)
    # if is_expanded:
    #     # i am fetching a pokemon fetch_data
    #     abilities = AbilityRetriever(kwargs)
    #     moves = MoveRetriever(kwargs)
    #
    #     moves_list = for loop (Move(kwargs))
    #
    #     new_pokemon = Pokemon(kwargs)

    async def parse(self, json):
        pass

    async def generate_pokedex_object(self, **kwargs):
        return Pokemon(**kwargs)


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

    async def generate_pokedex_object(self, **kwargs):
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
        kwargs["effect"] = json["effect_entries"][0]["short_effect"]
        return kwargs

    async def generate_pokedex_object(self, **kwargs):
        return Move(**kwargs)


class StatRetriever(Retriever):

    async def parse(self, json):
        kwargs = {}
        kwargs["name"] = json["name"]
        kwargs["id"] = json["id"]
        kwargs["is_battle_only"] = json["is_battle_only"]
        return kwargs

    async def generate_pokedex_object(self, **kwargs):
        return Stat(**kwargs)
