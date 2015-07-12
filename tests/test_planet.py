# vim: set ts=4 sw=4 et: coding=UTF-8
"""
Test planet generator from objects/planet.py
"""

from nose.tools import ok_
from openmoo2.objects import planet


class Test_Planet(object):
    @classmethod
    def setup_class(cls):
        cls.random_planet = planet.Planet()
        cls.home_planet = planet.Planet(user_planet=True)

    def test_planet_setup(self):
        ok_(self.random_planet.setup is not None, "random planet has setup 'None'")
        ok_(self.home_planet.setup == "Normal", "home planet has another setup than 'Normal'")

    def test_planet_size(self):
        ok_(self.random_planet.size is not None, "random planet has size 'None'")
        ok_(self.home_planet.size == "Medium", "home planet has another size than 'Medium'")

    def test_planet_biology(self):
        ok_(self.random_planet.biology is not None, "random planet has biology 'None'")
        ok_(self.home_planet.biology == "Terran", "home planet has another biology than 'Terran'")

    def test_planet_minerals(self):
        ok_(self.random_planet.minerals is not None, "random planet has minerals 'None'")
        ok_(self.home_planet.minerals == "Abundant", "home planet has another minerals than 'Abundant'")

    def test_planet_gravity(self):
        """TODO : add with random generator for gravity"""
        pass
