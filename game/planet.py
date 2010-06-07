import universe
import lbx

__author__="peterman"
__date__ ="$May 16, 2010 11:00:06 AM$"

class Planet(universe.GameObject):

    def __init__(self, planet_id):
        self.set_id(planet_id)

    def set_colony_id(self, colony_id):
        self.__colony_id = colony_id

    def get_colony_id(self):
        return self.__colony_id

    def set_star(self, star_id):
        self.__star_id = star_id

    def get_star(self):
        return self.__star_id

    def set_position(self, position):
        self.__position = position

    def get_position(self):
        return self.__position

    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type

    def set_size(self, size):
        self.__size = size

    def get_size(self):
        return self.__size

    def set_gravity(self, gravity):
        self.__gravity = gravity

    def get_gravity(self):
        return self.__gravity

    def set_terrain(self, terrain):
        self.__terrain = terrain

    def get_terrain(self):
        return self.__terrain

    def set_picture(self, picture):
        self.__picture = picture

    def get_picture(self):
        return self.__picture

    def set_minerals(self, minerals):
        self.__minerals = minerals

    def get_minerals(self):
        return self.__minerals

    def set_foodbase(self, foodbase):
        self.__foodbase = foodbase
        
    def get_foodbase(self):
        return self.__foodbase

    def set_terraformations(self, terraformations):
        self.__terraformations = terraformations

    def get_terraformations(self):
        return self.__terraformations

    def set_max_farms(self, max_farms):
        self.__max_farms = max_farms

    def get_max_farms(self):
        return self.__max_farms

    def set_max_population(self, max_population):
        self.__max_population = max_population

    def get_max_population(self):
        return self.__max_population

    def set_special(self, special):
        self.__special = special

    def get_special(self):
        return self.__special

    def set_flags(self, flags):
        self.__flags = flags

    def get_flags(self):
        return self.__flags

    def import_from_moo2(self, data):
        self.set_colony_id(lbx.read_short_int(data, 0x00))	# 0xffff = no colony here
        self.set_star(lbx.read_byte(data, 0x02))
        self.set_position(lbx.read_byte(data, 0x03))
        self.set_type(lbx.read_byte(data, 0x04))
        self.set_size(lbx.read_byte(data, 0x05))
        self.set_gravity(lbx.read_byte(data, 0x06))
#        self.set_group(lbx.read_byte(data, 0x07))   # not used ?
        self.set_terrain(lbx.read_byte(data, 0x08))
        self.set_picture(lbx.read_byte(data, 0x09))   # Background image on colony screen (0-5=image in planets.lbx)
        self.set_minerals(lbx.read_byte(data, 0x0a))
        self.set_foodbase(lbx.read_byte(data, 0x0b))
        self.set_terraformations(lbx.read_byte(data, 0x0c))
        self.set_max_farms(lbx.read_byte(data, 0x0d))   # unknown (Initial value is based on Planet Size but changes if colonized), 2=tiny, 4=small, 5=med, 7=large, A=huge
        self.set_max_population(lbx.read_byte(data, 0x0e))
        self.set_special(lbx.read_byte(data, 0x0f))
        self.set_flags(lbx.read_byte(data, 0x10))    # (bit 2 = Soil Enrichment)

    def is_asteroid_belt(self):
        return self.get_type() == 1

    def is_gas_giant(self):
        return self.get_type() == 2

    def is_planet(self):
        return self.get_type() == 3
