# vim: set ts=4 sw=4 et: coding=UTF-8

from .. import probabilities

class Planet(object):
    """
    Object containing all information and
    getters for Planets
    """

    # FIXME: read this from game configuration
    mineral_rich=False
    organic_rich=False

    # Default planet identifiers
    # type of planet: normal, asteroids, gas giant, ...
    setup = None
    # size of the planet Tiny -> Huge
    size = None
    # minerals of the planet Ultra rich -> Ultra poor
    minerals = None
    # radiated/Toxic -> Gaia
    biology = "Barren"
    # gravitation of planet
    gravity = None
    # have native inhabitants?
    natives = False
    # have ancient artefacts?
    artefacts = False
    # have gold deposits?
    gold_deposits = False
    # have gem deposits?
    gem_deposits = False
    # homeworld?
    homeworld = False

    def __determine_planet_type(self):
        """
        Figure out what type the planet wil be
        """

        # well we can't have homewrold on asteroids, can we
        if self.homeworld:
            return "Normal"

        # We can be 3 types: normal, asteroids or gas giant
        """
        30% asteroids/gas-giant
        70% planet
        """
        if determine_probability(30):
            # Asteroids/Gas giant
            return get_50_50("Asteroids", "Gas giant")
        return "Normal"

    def __determine_planet_size(self):
        """
        Figure out size for the planet
        """

        # Homeworld value
        if self.homeworld:
            # FIXME: user can specify different values when creating race
            return "Medium"

        """
        We can have following types:
        Huge, Large, Medium, Small, tiny
        Using normal distribtuion:
        68.2 Medium
        27.2 Large/Small
        4.6 Huge/Tiny
        """
        if determine_probability(4.6):
            # Huge/Tiny
            return get_50_50("Huge", "Tiny")
        if determine_probability(27.2):
            # Large/Small
            return get_50_50("Large", "Small")
        return "Normal"

    def __determine_planet_minerals(self):
        """
        Figure out minerals for the planet
        """

        # Determine unverse layout
        penalty = 0
        if self.mineral_rich:
            penalty = -15
        if self.organic_rich:
            penalty = 15

        # Homeworld value
        if self.homeworld:
            # FIXME: user can specify different values when creating race
            return "Abundant"

        """
        We can have following types:
        Ultra rich, Rich, Abundant, Poor, Ultra poor
        We will use normal distribution, but can skew in/out depending
        on game settings for the play:
        68.2 Abundant
        27.2 Rich/Poor
        4.6 Ultra rich/Ultra poor
        """
        if determine_probability(4.6):
            # Huge/Tiny
            return get_50_50("Rich", "Poor", penalty)
        if determine_probability(27.2):
            # Large/Small
            return get_50_50("Ultra rich", "Ultra poor", penalty)
        return "Abundant"

    def __determine_planet_biology(self):
        """
        Figure out minerals for the planet
        """

        # Homeworld value
        if self.homeworld:
            # FIXME: user can specify different values when creating race
            return "Terran"

        """
        We can have following types:
        Gaia/Terran/(Swamp/Ocean)/(Tundra/Dessert)/(Barren/Radiated)/Toxic
        We will use normal distribution, but can skew in/out depending
        on game settings for the play:
        TODO
        """

    def __init__(self, user_planet=False):
        """
        Generate new planet
        param: user_planet bool wether to create race homeworld
        """

        self.homeworld = user_planet

        self.setup = self.__determine_planet_type()
        # we determine size/minerals for future create planet tech
        self.size = self.__determine_planet_size()
        self.minerals = self.__determine_planet_minerals()
        self.biology = self.__determine_planet_biology()
