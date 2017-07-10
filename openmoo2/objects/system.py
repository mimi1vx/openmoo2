# vim: set ts=4 sw=4 et: coding=UTF-8


class StarSystem(object):
    """ Object containing all information and getters for Star systems."""

    _systems = set()
    max_planets = 5

    def __init__(self, name, color, **kwargs):
        """Initialize star system."""
        self.color = color
        self.__name = None
        self.name = name
        self.__planets = None
        self.administrator = None


    @property
    def planets(self):
        """Property handling dict of planets."""
        if self.color == 'black':
            return {}
        if len(self.__planets) > StarSystem.max_planets:
            raise Exception
        return self.__planets

    @planets.setter
    def planets(self, planet):
        if self.color == 'black':
            raise Exception
        counter = len(self.__planets)
        if counter >= StarSystem.max_planets:
            raise Exception
        self.__planets[counter+1] = planet

    @planets.deleter
    def planets(self):
        pass

    @property
    def administrator(self):
        if self.color == 'black':
            raise Exception
        return self.__administrator

    @administrator.setter
    def administrator(self, admin):
        self.__administrator = admin

    @administrator.deleter
    def administrator(self):
        self.administrator = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name in StarSystem._systems:
            raise Exception
        if self.__name:
            StarSystem._systems.discard(self.name)
        StarSystem._systems.add(name)
        self.__name = name

    @name.deleter
    def name(self):
        pass
