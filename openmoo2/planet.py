# vim: set ts=4 sw=4 et: coding=UTF-8

class Planet(object):
    """
    Object containing all information and
    getters for Planets
    """

    # Default planet identifiers
    # type of planet: normal, asteroids, gas giant, ...
    setup = None
    # size of the planet Tiny -> Huge
    size = None
    # radiated/Toxic -> Gaia
    biology = None
    # have native inhabitants?
    natives = False
    # have ancient artefacts?
    artefacts = False
    # have gold deposits?
    gold_deposits = False
