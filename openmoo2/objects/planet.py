# vim: set ts=4 sw=4 et: coding=UTF-8

from ..probabilities import determine_probability, get_50_50

class Planet(object):
    """
    Object containing all information and
    getters for Planets
    """

    # FIXME: read this from game configuration
    mineral_rich = False
    organic_rich = False

    # Default planet identifiers
    # type of planet: normal, asteroids, gas giant, ...
    setup = None
    # size of the planet Tiny -> Huge
    size = None
    # minerals of the planet Ultra rich -> Ultra poor
    minerals = None
    # radiated/Toxic -> Gaia
    biology = None
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

        """
        We can be 3 types:
        Normal, Asteroids, Gas giant
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
            return get_50_50("Huge", "Tiny")
        if determine_probability(27.2):
            return get_50_50("Large", "Small")
        return "Normal"

    def __determine_planet_minerals(self):
        """
        Figure out minerals for the planet
        """

        # Determine unverse layout
        penalty = 0
        probability_skew = 0
        if self.mineral_rich:
            probability_skew = 5
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
        if determine_probability(4.6 + probability_skew):
            return get_50_50("Rich", "Poor", penalty)
        if determine_probability(27.2 + probability_skew):
            return get_50_50("Ultra rich", "Ultra poor", penalty)
        return "Abundant"

    def __determine_planet_biology(self):
        """
        Figure out minerals for the planet
        """

        # Determine unverse layout
        probability_skew = 0
        if self.mineral_rich:
            probability_skew = -5
        if self.organic_rich:
            probability_skew = 5

        # Homeworld value
        if self.homeworld:
            # FIXME: user can specify different values when creating race
            return "Terran"

        # For future planet creation we can consider these barren
        if not self.setup == "Normal":
            return "Barren"

        """
        We can have following types:
        0    1      2             3                4                 5
        Gaia/Terran/(Swamp/Ocean)/(Tundra/Dessert)/(Barren/Radiated)/Toxic
        We will use normal distribution, but can skew in/out depending
        on game settings for the play:
        6% 0
        10% 1
        19% 2 or 3 in organic_rich
        36% 3 or 4 in mineral_rich or 2 in organic_rich
        19% 4 or 3 in mineral_rich
        10% 5
        """
        if determine_probability(6 + probability_skew):
            return "Gaia"
        if determine_probability(10 + probability_skew):
            return "Terran"
        if determine_probability(19):
            if self.organic_rich:
                return get_50_50("Tundra", "Dessert")
            else:
                return get_50_50("Swamp", "Ocean")
        if determine_probability(36 + probability_skew):
            if self.mineral_rich:
                return get_50_50("Barren", "Radiated")
            elif self.organic_rich:
                return get_50_50("Swamp", "Ocean")
            else:
                return get_50_50("Tundra", "Dessert")
        if determine_probability(19):
            if self.mineral_rich:
                return get_50_50("Tundra", "Dessert")
            else:
                return get_50_50("Barren", "Radiated")
        if determine_probability(10):
            return "Toxic"

        # If user got here he is not lucky one
        return get_50_50("Barren", "Radiated")

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
