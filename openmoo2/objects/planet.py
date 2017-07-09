# vim: set ts=4 sw=4 et: coding=UTF-8

# import specific exceptions

planetgravity = {"tiny": {"ultrapoor": "low", "poor": "low", "average": "low", "rich": "medium", "ultrarich": "medium"},
                 "small": {"ultrapoor": "low", "poor": "low", "average": "medium", "rich": "medium", "ultrarich": "medium"},
                 "medium": {"ultrapoor": "low", "poor": "medium", "average": "medium", "rich": "medium", "ultrarich": "heavy"},
                 "large": {"ultrapoor": "medium", "poor": "medium", "average": "medium", "rich": "heavy", "ultrarich": "heavy"},
                 "huge": {"ultrapoor": "medium", "poor": "medium", "average": "heavy", "rich": "heavy", "ultrarich": "heavy"}}


class Planet(object):

    """object holding information about planet."""

    def __init__(self, kind, **kwarg):
        if kind not in ("asteroids", "giant", "planet"):
            raise Exception  # TODO: specific extension for unknow planet type

        # holds planet gravity
        self._gravity = None
        # holds colony -- can be colony or outpost
        self._colony = None

        self.kind = kind

        if kind == "asteroids":
            return
        if kind == "giant":
            self.colony = kwarg['colony'] if 'colony' in kwarg else None
            return

        for i in ("size", "organic", "mineral", "environment"):
            if i not in kwarg:
                raise Exception  # TODO specific exception for missing

        self.size = kwarg['size']
        self.organic = kwarg['organic']
        self.mineral = kwarg['mineral']
        self.environment = kwarg['environment']
        self.colony = kwarg['colony'] if 'colony' in kwarg else None

        if 'gravity' in kwarg:
            self.gravity = kwarg['gravity']
        else:
            self.gravity

        self.special = kwarg['special'] if 'special' in kwarg else None
        self.homeworld = True if self.special == 'homeworld' else False

    @property
    def gravity(self):
        """Set gravity of planet."""
        if self.kind in ('asteroids', 'giant'):
            del self.gravity
        elif self.kind == 'planet':
            if not self._gravity:
                self._gravity = planetgravity[self.size][self.mineral]
        return self._gravity

    @gravity.setter
    def gravity(self, value):
        if self.kind == 'asteroids' and value is not None:
            raise Exception  # TODO: specific exception
        if value not in ('low', 'medium', 'heavy', None):
            raise Exception  # TODO: specific exception
        if self.kind not in ('planet', 'asteroids'):
            raise Exception  # TODO: specific exception
        self._gravity = value

    @gravity.deleter
    def gravity(self):
        self._gravity = None

    @property
    def colony(self):
        """Colony setter for planet/giant"""
        if self.kind == 'asteroids':
            del self.colony
        return self._colony

    @colony.setter
    def colony(self, value):
        if self.kind == 'asteroids' and value is not None:
            raise Exception  # TODO: specific exception
        if self.kind == 'giant' and value is not None:
            if value.kind != 'outpost':
                raise Exception  # TODO: specific exception
        self._colony = value

    @colony.deleter
    def colony(self):
        self._colony = None

    # destroy planet --> stellar converter --> reinit as asteroids
    def destroy_planet(self):
        """Set planet as asteroid field and sets all planet attributes to None/False."""
        self.gravity = None
        self.kind = 'asteroids'
        self.size = None
        self.organic = None
        self.mineral = None
        self.colony = None
        self.outpost = None
        self.special = None
        self.homeworld = False
        self.environment = None

    def create_planet(self, **kwarg):
        """Oposite of destroy_planet"""
        if self.kind not in ('giant', 'asteroids'):
            raise Exception  # TODO: specific exception

        for i in ("size", "organic", "mineral", "environment"):
            if i not in kwarg:
                raise Exception  # TODO specific exception for missing

        if self.kind == 'giant':
            self.outpost = None

        self.kind = 'planet'
        self.size = kwarg['size']
        self.organic = kwarg['organic']
        self.mineral = kwarg['mineral']
        self.environment = kwarg['environment']

        if 'gravity' in kwarg:
            self.gravity = kwarg['gravity']
        else:
            self.gravity

    def __str__(self):
        if self.kind == 'asteroids':
            tmpstr = "This is asteroids field"
        elif self.kind == 'giant':
            if self.colony:
                tmpstr = "This is gas giant planet with outpost: {!s}".format(self.colony)
            else:
                tmpstr = "This is gas giant planet"
        elif self.kind == 'planet':
            tmpstr = "Planet size: {!s} gravity: {!s} with {!s} environment\n".format(
                self.size, self.gravity, self.environment)
            tmpstr += "Has {!s} minerals and {!s} biology\n".format(self.mineral, self.organic)
            if self.special:
                tmpstr += "Has {!s} special\n".format(self.special)
            if self.colony:
                if self.colony.kind == 'outpost':
                    tmpstr += "Has {!s} outpost".format(self.colony)
                elif self.colony.kind == 'colony':
                    tmpstr += "Is colonized:\n {!s}".format(self.colony)
        return tmpstr
