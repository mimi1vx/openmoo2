# vim: set ts=4 sw=4 et: coding=UTF-8
"""
Test planet generator from objects/planet.py
"""

from nose.tools import raises, eq_
from openmoo2.objects.planet import Planet


class FakeColony(object):

    def __init__(self, owner):
        self.owner = owner

    def __str__(self):
        return self.owner


class TestPlanet(object):
    outpost = FakeColony('Boo')
    colony = FakeColony('Poo')

    @raises(Exception)  # TODO: specific exception
    def test_planet_wrong_type(self):
        Planet('foo')

    def test_planet_gravity_override(self):
        planetx = Planet('planet', size='huge', organic='rich', mineral='rich', environment='toxic', gravity='medium')
        eq_(planetx.gravity, 'medium')

    def test_gravity_heavy(self):
        planetx = Planet('planet', size='huge', organic='rich', mineral='rich', environment='toxic')
        eq_(planetx.gravity, 'heavy')

    def test_gravity_low(self):
        planetx = Planet('planet', size='tiny', organic='rich', mineral='poor', environment='toxic')
        eq_(planetx.gravity, 'low')

    def test_gravity_medium(self):
        planetx = Planet('planet', size='small', organic='rich', mineral='average', environment='toxic')
        eq_(planetx.gravity, 'medium')

    def test_gravity_del(self):
        planetx = Planet('planet', size='tiny', organic='rich', mineral='poor', environment='toxic')
        planetx.gravity = 'heavy'
        eq_(planetx.gravity, 'heavy')
        del planetx.gravity
        eq_(planetx.gravity, 'low')

    @raises(Exception)  # TODO: specific exceptions
    def test_read_gravity_giant(self):
        planetx = Planet('giant')
        planetx.gravity

    @raises(Exception)  # TODO: specific Exception
    def test_set_gravity_giant(self):
        planetx = Planet('giant')
        planetx.gravity = 'heavy'

    @raises(Exception)  # TODO: specific exceptions
    def test_set_gravity_asteroids(self):
        planetx = Planet('asteroids')
        planetx.gravity = 'heavy'

    def test_set_gravity_asteroids2(self):
        planetx = Planet('asteroids')
        planetx.gravity = None
        eq_(planetx.gravity, None)

    def test_set_gravity_correctly(self):
        planetx = Planet('planet', size='small', organic='rich', mineral='average', environment='toxic')
        gravity = ('low', 'medium', 'heavy')
        for i in gravity:
            planetx.gravity = i
            eq_(planetx.gravity, i)

    @raises(Exception)
    def test_set_gravity_wrongly(self):
        planetx = Planet('planet', size='small', organic='rich', mineral='average', environment='toxic')
        planetx.gravity = 'jupajda'

    @raises(Exception)
    def test_bad_init_planet1(self):
        Planet('planet')

    @raises(Exception)
    def test_bad_init_planet2(self):
        Planet('planet', size='small')

    @raises(Exception)
    def test_bad_init_planet3(self):
        Planet('planet', size='small', organic='poor',)

    @raises(Exception)
    def test_bad_init_planet4(self):
        Planet('planet', organic='poor', mineral='poor')

    @raises(Exception)
    def test_bad_init_planet5(self):
        Planet('planet', environment='toxic')

    @raises(Exception)
    def test_bad_init_planet6(self):
        Planet('planet', size='tiny', organic='poor', environment='toxic')

    @raises(Exception)
    def test_bad_init_planet7(self):
        Planet('planet', environment='toxic', mineral='rich', size='huge')

    def test_destroy_planet(self):
        planetx = Planet('planet', size='huge', organic='rich', mineral='rich', environment='toxic')
        eq_(planetx.kind, 'planet')
        planetx.destroy_planet()
        eq_(planetx.kind, 'asteroids')

    def test_planet_strings_asteroids(self):
        planetx = Planet('asteroids')
        eq_(str(planetx), 'This is asteroids field')

    def test_planet_strings_giant(self):
        planetx = Planet('giant')
        eq_(str(planetx), 'This is gas giant planet')

    def test_planet_strings_giant_outpost(self):
        planetx = Planet('giant', outpost=self.outpost)
        eq_(str(planetx), 'This is gas giant planet with outpost: Boo')

    def test_planet_strings_planet(self):
        planetx = Planet('planet', size='small', organic='rich', mineral='average', environment='gaia')
        eq_(str(planetx), 'Planet size: small gravity: medium with gaia environment\nHas average minerals and rich biology\n')

    def test_planet_strings_planet_outpost(self):
        planetx = Planet(
            'planet',
            size='small',
            organic='rich',
            mineral='average',
            environment='gaia',
            outpost=self.outpost)
        eq_(str(planetx), 'Planet size: small gravity: medium with gaia environment\nHas average minerals and rich biology\nHas Boo outpost')

    def test_planet_strings_planet_colony(self):
        planetx = Planet(
            'planet',
            size='small',
            organic='rich',
            mineral='average',
            environment='gaia',
            colony=self.colony)
        eq_(str(planetx), 'Planet size: small gravity: medium with gaia environment\nHas average minerals and rich biology\nIs colonized:\n Poo')

    def test_planet_strings_planet_colony_special(self):
        planetx = Planet(
            'planet',
            size='small',
            organic='rich',
            mineral='average',
            environment='gaia',
            colony=self.colony,
            special="Orion")
        eq_(str(planetx), 'Planet size: small gravity: medium with gaia environment\nHas average minerals and rich biology\nHas Orion special\nIs colonized:\n Poo')
