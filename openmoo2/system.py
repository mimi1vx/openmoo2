# vim: set ts=4 sw=4 et: coding=UTF-8

class StarSystem(object):
    """
    Object containing all information and
    getters for Star systems
    """

    # Default system identifiers
    # size of the system (number of planets)
    size = 0
    # position on map
    position_x = 0
    position_y = 0
    # have some space beast
    beast = None
    # have some stranded leaders?
    stranded_leader = None
    # or even ships?
    stranded_ship = None
