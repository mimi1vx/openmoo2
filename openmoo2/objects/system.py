# vim: set ts=4 sw=4 et: coding=UTF-8

from ..probabilities import determine_probability, get_50_50
from .planet import Planet


class StarSystem(object):

    """
    Object containing all information and getters for Star systems.
    """

    # Default system identifiers
    # position on map
    position_x = 0
    position_y = 0
    # color of system
    color = None
    # have some space beast
    beast = None
    # have some stranded leaders?
    stranded_leader = None
    # or even ships?
    stranded_ship = None
    # stable wormhole
    stable_wormhole = None
    # unstable wormhole
    unstable_wormhole = None
    # planets
    planets = list()

    def __determine_unstable_wormhole(self):
        """
        Decide if the star system will be ok or just ugly
        traffic blocking wormhole.
        """

        if determine_probability(5):
            # Bad luck buddy
            return True
        return False

    def __determine_planets(self):
        """
        Decide how many and what planets we will have.
        """
        planet_count = 0
        planet = None

        # We can have 0 - 5 planets
        if determine_probability(4.6):
            planet_count = get_50_50(0, 5)
        elif determine_probability(27.2):
            planet_count = get_50_50(1, 4)
        else:
            planet_count = get_50_50(2, 3)

        for i in range(0, planet_count):
            planet = Planet()
            planet.randomize(self.color)
            self.planets.append(planet)

    def __determine_specialities(self):
        """
        Decide all various special factors for the star system.
        """

        if determine_probability(5):
            # FIXME: Set this to leader object
            self.stranded_leader = True
            return
        if determine_probability(5):
            # FIXME: Set this to some ship object
            self.stranded_ship = True
            return
        if determine_probability(5):
            # FIXME: Set this to some beast object
            self.beast = True

    def __init__(self):
        """
        Generate new star system.
        """
        return

    def randomize(self):
        """
        Radomize content of the star system for space creation.
        """
        # Here we do not create stable wormhole and position as
        # those values must came from the whole universe layout
        self.unstable_wormhole = self.__determine_unstable_wormhole()
        # And anything worth setting values is only in non-wormhole setup
        if not self.unstable_wormhole:
            self.__determine_planets()
            self.__determine_specialities()
