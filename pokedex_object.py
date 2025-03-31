# Name: Michael McBride
# Student number: A01394787
# Name: Parham Abdolmohammadi
# Student number: A01356970

import abc


class PokedexObject(abc.ABC):
    """
    Abstract base class for all Pokédex domain objects, such as Pokemon, Move, Stat, and Ability.
    """

    def __init__(self, **kwargs):
        """
        Initializes a PokedexObject with a name and ID.

        Args:
            **kwargs: Dictionary containing 'name' and 'id' keys.
        """

        self._name = kwargs["name"]
        self._id = kwargs["id"]

    @property
    def name(self):
        """
        Returns the name of the object.

        Returns:
            str: The name of the object.
        """

        return self._name

    @property
    def id(self):
        """
        Returns the ID of the object.

        Returns:
            int: The ID of the object.
        """

        return self._id


class Move(PokedexObject):
    """
    Represents a Pokémon move, including its type, power, PP, accuracy, and related metadata.
    """

    def __init__(self, **kwargs):
        """
        Initializes a Move object with data from keyword arguments.

        Args:
            **kwargs: Dictionary containing move attributes.
        """

        super().__init__(**kwargs)
        self._generation = kwargs["generation"]
        self._accuracy = kwargs["accuracy"]
        self._pp = kwargs["pp"]
        self._power = kwargs["power"]
        self._type = kwargs["type"]
        self._damage_class = kwargs["damage_class"]
        self._effect = kwargs["effect"]

    @property
    def generation(self):
        """Returns the generation in which the move was introduced."""

        return self._generation

    @property
    def accuracy(self):
        """Returns the accuracy of the move."""

        return self._accuracy

    @property
    def pp(self):
        """Returns the Power Points (PP) of the move."""

        return self._pp

    @property
    def power(self):
        """Returns the power of the move."""

        return self._power

    @property
    def type(self):
        """Returns the type of the move (e.g., fire, water, etc.)."""

        return self._type

    @property
    def damage_class(self):
        """Returns the damage class of the move (e.g., physical, special)."""

        return self._damage_class

    @property
    def effect(self):
        """Returns the short effect description of the move."""

        return self._effect

    def __str__(self):
        return f"""
Name: {self.name}
ID: {self.id}
Generation: {self.generation}
Accuracy: {self.accuracy}
PP: {self.pp}
Power: {self.power}
Type: {self.type}
Damage Class: {self.damage_class}
Effect(Short): {self.effect}
"""


class Stat(PokedexObject):
    """
    Represents a Pokémon stat, such as HP, Attack, or Defense.
    """

    def __init__(self, **kwargs):
        """
        Initializes a Stat object with data from keyword arguments.

        Args:
            **kwargs: Dictionary containing stat attributes.
        """

        super().__init__(**kwargs)
        self.__is_battle_only = kwargs["is_battle_only"]

    @property
    def is_battle_only(self):
        """
        Indicates whether the stat is used exclusively in battle.

        Returns:
            bool: True if stat is battle-only, False otherwise.
        """

        return self.__is_battle_only

    def __str__(self):
        return f"""
Name: {self.name}
ID: {self.id}
Is_Battle_Only: {self.is_battle_only}
    """


class Pokemon(PokedexObject):
    """
    Represents a Pokémon entity with its stats, abilities, types, and moves.
    """

    def __init__(self, **kwargs):
        """
        Initializes a Pokemon object with data from keyword arguments.

        Args:
            **kwargs: Dictionary containing Pokémon attributes.
        """

        super().__init__(**kwargs)
        self.__height = kwargs["height"]
        self.__weight = kwargs["weight"]
        self.__stats = kwargs["stats"]  # Should be a list of Stat objects
        self.__types = kwargs["types"]  # Should be a list of String
        self.__abilities = kwargs["abilities"]  # Should be a list of Ability objects
        self.__moves = kwargs["moves"]  # Should be a list of Move objects

    def __str__(self):

        types = ""
        for pk_type in self.__types:
            types += pk_type + " "

        stats = "\n".join([str(stat) for stat in self.__stats])
        abilities = "\n".join([str(ability) for ability in self.__abilities])
        moves = "\n".join([str(move) for move in self.__moves])


        string = f"""
Name: {self.name}
ID: {self.id}
Height: {self.height}
Weight: {self.weight}
Types:  {types}

Stats: 
"------"
{stats}

Abilities:
"------"
{abilities}

Moves:
"------"
{moves}
   
        """

        return string

    @property
    def height(self):
        """Returns the height of the Pokémon."""

        return self.__height

    @property
    def weight(self):
        """Returns the weight of the Pokémon."""

        return self.__weight

    @property
    def stats(self):
        """Returns the stats of the Pokémon."""
        return self.__stats

    @property
    def types(self):
        """Returns the types of the Pokémon."""
        return self.__types

    @property
    def abilities(self):
        """Returns the abilities of the Pokémon."""
        return self.__abilities

    @property
    def moves(self):
        """Returns the moves of the Pokémon."""
        return self.__moves

class Ability(PokedexObject):
    """
    Represents a Pokémon ability, including its effects and applicable Pokémon.
    """

    def __init__(self, **kwargs):
        """
        Initializes an Ability object with data from keyword arguments.

        Args:
            **kwargs: Dictionary containing ability attributes.
        """

        super().__init__(**kwargs)
        self.__generation = kwargs["generation"]
        self.__effect = kwargs["effect"]
        self.__effect_short = kwargs["effect_short"]
        self.__pokemon = kwargs["pokemon"]  # Should be a list of Strings

    @property
    def generation(self):
        """Returns the generation in which the ability was introduced."""
        return self.__generation

    @property
    def effect(self):
        """Returns the full effect description of the ability."""
        return self.__effect

    @property
    def effect_short(self):
        """Returns the short effect description of the ability."""
        return self.__effect_short

    @property
    def pokemon(self):
        """Returns the list of Pokémon that can have this ability."""
        return self.__pokemon

    def __str__(self):
        return f"""
Name: {self.name}
ID: {self.id}
Generation: {self.generation}
Effect: {self.effect}
Effect(Short): {self.effect_short}
Pokemon: {", ".join(self.pokemon)}
"""
