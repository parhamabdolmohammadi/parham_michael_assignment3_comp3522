import abc


class PokedexObject(abc.ABC):
    def __init__(self, **kwargs):
        self._name = kwargs["name"]
        self._id = kwargs["id"]

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id


class Move(PokedexObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._generation = kwargs["kwargs"]
        self._accuracy = kwargs["accuracy"]
        self._pp = kwargs["pp"]
        self._power = kwargs["power"]
        self._type = kwargs["type"]
        self._damage_class = kwargs["damage class"]
        self._effect = kwargs["effect"]

    @property
    def generation(self):
        return self._generation

    @property
    def accuracy(self):
        return self._accuracy

    @property
    def pp(self):
        return self._pp

    @property
    def power(self):
        return self._power

    @property
    def type(self):
        return self._type

    @property
    def damage_class(self):
        return self._damage_class

    @property
    def effect(self):
        return self._effect


class Stat(PokedexObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._is_battle_only = kwargs["is battle only"]

    @property
    def is_battle_only(self):
        return self._is_battle_only


class Pokemon(PokedexObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._height = kwargs["height"]
        self._weight = kwargs["weight"]
        self._stats = kwargs["stats"]  # Should be a list of Stat objects
        self._types = kwargs["types"]  # Should be a list of String
        self._abilities = kwargs["abilities"]  # Should be a list of Ability objects
        self._moves = kwargs["moves"]  # Should be a list of Move objects

    @property
    def height(self):
        return self._height

    @property
    def weight(self):
        return self._weight

    @property
    def stats(self):
        return self._stats

    @property
    def types(self):
        return self._types

    @property
    def abilities(self):
        return self._abilities

    @property
    def moves(self):
        return self._moves


class Ability(PokedexObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._generation = kwargs["generation"]
        self._effect = kwargs["effect"]
        self._effect_short = kwargs["effect_short"]
        self._pokemon = kwargs["pokemon"]  # Should be a list of Strings

    @property
    def generation(self):
        return self._generation

    @property
    def effect(self):
        return self._effect

    @property
    def effect_short(self):
        return self._effect_short

    @property
    def pokemon(self):
        return self._pokemon

    def __str__(self):
        return f"""
Name: {self.name}
ID: {self.id}
Generation: {self.generation}
Effect: {self.effect}
Effect(Short): {self.effect_short}
Pokemon: {", ".join(self.pokemon)}
"""
