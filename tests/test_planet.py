# vim: set ts=4 sw=4 et: coding=UTF-8
"""
Test planet generator from objects/planet.py
"""

from nose.tools import ok_
from openmoo2.objects import planet


class TestPlanet(object):
    @classmethod
    def setup_class(cls):
        cls.random_planet = planet.Planet()
        cls.random_planet.randomize_planet()

    def test_planet_setup(self):
        ok_(self.random_planet.setup is not None, "random planet has setup 'None'")

    def test_planet_size(self):
        ok_(self.random_planet.size is not None, "random planet has size 'None'")

    def test_planet_biology(self):
        ok_(self.random_planet.biology is not None, "random planet has biology 'None'")

    def test_planet_minerals(self):
        ok_(self.random_planet.minerals is not None, "random planet has minerals 'None'")

    def test_planet_gravity(self):
        ok_(self.random_planet.gravity is not None, "random planet has gravity 'None'")
