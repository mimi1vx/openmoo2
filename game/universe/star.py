import lbx
from savegame import bitmask_to_player_id_list
from space_object import SpaceObject

__author__ = "peterman"
__date__ = "$May 15, 2010 9:12:05 AM$"

class Star(SpaceObject):

    def __init__(self, star_id):
        self.set_id(star_id)
    # /__init__

    def set_size(self, size):
        self.__size = size

    def get_size(self):
        return self.__size

    def set_pict_type(self, pict_type):
        self.__pict_type = pict_type

    def get_pict_type(self):
        return self.__pict_type

    def set_class(self, cl):
        self.__class = cl

    def get_class(self):
        return self.__class

    def set_objects(self, objects):
        self.__objects = objects

    def get_objects(self):
        return self.__objects

    def visited(self):
        return self.__visited

    def wormhole(self):
        return self.__wormhole

    def visited_by_player(self, player_id):
        return self.__visited & (1 << player_id)

    def get_data(self):
        return self.__moo2data

    def is_in_nebula(self):
        return self.__is_in_nebula

    def import_from_moo2(self, data):

        self.__moo2data = data

        self.set_name(lbx.read_string(data, 0, 15))
        self.set_x(lbx.read_short_int(data, 0x0f))
        self.set_y(lbx.read_short_int(data, 0x11))
        self.set_size(lbx.read_byte(data, 0x13))
        self.__owner = lbx.read_byte(data, 0x14)		# primary owner
        self.set_pict_type(lbx.read_byte(data, 0x15))
        self.set_class(lbx.read_byte(data, 0x16))
        self.__last_planet_selected = [
            lbx.read_byte(data, 0x17),
            lbx.read_byte(data, 0x18),
            lbx.read_byte(data, 0x19),
            lbx.read_byte(data, 0x1A),
            lbx.read_byte(data, 0x1B),
            lbx.read_byte(data, 0x1C),
            lbx.read_byte(data, 0x1D),
            lbx.read_byte(data, 0x1E)
        ]

        self.__special = lbx.read_byte(data, 0x28)
        self.__wormhole = lbx.read_byte(data, 0x29)
        self.__blockaded_players = bitmask_to_player_id_list(ord(data[0x2a]))
        self.__blockaded_by_bitmask = [ord(data[0x2b]), ord(data[0x2c]), ord(data[0x2d]), ord(data[0x2e]), ord(data[0x2f]), ord(data[0x30]), ord(data[0x31]), ord(data[0x32])]
        self.__visited = ord(data[0x33])                # bitmask as boleans for each player
        self.__just_visited_bitmask = ord(data[0x34])           # players bitmask to track first visit of this star -> user should get report
        self.__ignore_colony_ship_bitmask = ord(data[0x35])     # players bitmask to track if player chose to not use a colony ship, cleared on every new colony ship here?
        self.__ignore_combat_bitmask = ord(data[0x36])  # players bitmask to track if player chose to ignore combat ships = perform blockade only do not fight here?
        self.__colonize_player = ord(data[0x37])        # 0..7 or -1
        self.__colonies_bitmask = ord(data[0x38])       # has colony / players bitmask / redundant info?
        self.__interdictors_bitmask = ord(data[0x39])   # has warp interdictor / players bitmask
        self.__next_wfi_in_list = ord(data[0x3a])       # bookeeping ???
        self.__tachyon_com_bitmask = ord(data[0x3b])    # has tachyon communicator / players bitmask
        self.__subspace_com_bitmask = ord(data[0x3c])   # has subspace communicator / players bitmask
        self.__stargates_bitmask = ord(data[0x3d])      # has stargate / players bitmask
        self.__jumpgates_bitmask = ord(data[0x3e])      # has jumpgate / players bitmask
        self.__artemis_bitmask = ord(data[0x3f])        # has artemis net players bitmask
        self.__portals_bitmask = ord(data[0x40])	# has dimension portal / players bitmask
        self.__stagepoint_bitmask = ord(data[0x41])	# bitvector tells whether star is stagepoint for each AI
        self.__players_officers = [ord(data[0x42]), ord(data[0x43]), ord(data[0x44]), ord(data[0x45]), ord(data[0x46]), ord(data[0x47]), ord(data[0x48]), ord(data[0x49])]
        self.set_objects([
                         lbx.read_short_int(data, 0x4a),
                         lbx.read_short_int(data, 0x4c),
                         lbx.read_short_int(data, 0x4e),
                         lbx.read_short_int(data, 0x50),
                         lbx.read_short_int(data, 0x52)
                         ])
        self.__surrender_to = [ord(data[0x67]), ord(data[0x68]), ord(data[0x69]), ord(data[0x6a]), ord(data[0x6b]), ord(data[0x6c]), ord(data[0x6d]), ord(data[0x6e])]
        self.__is_in_nebula = (ord(data[0x6f]) == 1)

"""
                'black_hole_blocks':	[
                                            ],
                '0x1f':		ord(self.__data[0x1f]),
                '0x20':		ord(self.__data[0x20]),
                '0x21':		ord(self.__data[0x21]),
                '0x22':		ord(self.__data[0x22]),
                '0x23':		ord(self.__data[0x23]),
                '0x24':		ord(self.__data[0x24]),
                '0x25':		ord(self.__data[0x25]),
                '0x26':		ord(self.__data[0x26]),
                '0x27':		ord(self.__data[0x27]),
                '0x2a':		ord(self.__data[0x2a]),	# blockaded? ( 0 | 1 )
                '0x2b':		ord(self.__data[0x2b]),
                '0x2c':		ord(self.__data[0x2c]),
                '0x2d':		ord(self.__data[0x2d]),
                '0x2e':		ord(self.__data[0x2e]),
                '0x2f':		ord(self.__data[0x2f]),
                '0x30':		ord(self.__data[0x30]),
                '0x31':		ord(self.__data[0x31]),
                '0x32':		ord(self.__data[0x32]),
                '0x34':		ord(self.__data[0x34]),
                '0x35':		ord(self.__data[0x35]),
                '0x36':		ord(self.__data[0x36]),
                '0x37':		ord(self.__data[0x37]),
                '0x38':		ord(self.__data[0x38]),
                '0x3a':		ord(self.__data[0x3a]),
                '0x3b':		ord(self.__data[0x3b]),
                '0x3c':		ord(self.__data[0x3c]),
                '0x3d':		ord(self.__data[0x3d]),
                '0x3e':		ord(self.__data[0x3e]), # jumpgate players bitmask
                '0x3f':		ord(self.__data[0x3f]), # artemist_net players bitmask
                '0x40':		ord(self.__data[0x40]),	# dimensional portal players bitmask
                '0x41':		ord(self.__data[0x41]), # is_stagepoint bitvector tells whether star is stagepoint for each AI
                '0x42':		ord(self.__data[0x42]), # officer_id foir player #0
                '0x43':		ord(self.__data[0x43]), # officer_id foir player #1
                '0x44':		ord(self.__data[0x44]), # officer_id foir player #2
                '0x45':		ord(self.__data[0x45]), # officer_id foir player #3
                '0x46':		ord(self.__data[0x46]), # officer_id foir player #4
                '0x47':		ord(self.__data[0x47]), # officer_id foir player #5
                '0x48':		ord(self.__data[0x48]), # officer_id foir player #6
                '0x49':		ord(self.__data[0x49]), # officer_id foir player #7
    #		??? Relocation star id (0-7 player #, not sure about size of array. )
                '0x54':		ord(self.__data[0x54]),
                '0x55':		ord(self.__data[0x55]),
                '0x56':		ord(self.__data[0x56]),
                '0x57':		ord(self.__data[0x57]),
                '0x58':		ord(self.__data[0x58]),
                '0x59':		ord(self.__data[0x59]),
                '0x5a':		ord(self.__data[0x5a]),
                '0x5b':		ord(self.__data[0x5b]),
                '0x5c':		ord(self.__data[0x5c]),
                '0x5d':		ord(self.__data[0x5d]),
                '0x5e':		ord(self.__data[0x5e]),
                '0x5f':		ord(self.__data[0x5f]),
                '0x60':		ord(self.__data[0x60]),
                '0x61':		ord(self.__data[0x61]),
                '0x62':		ord(self.__data[0x62]),
                '0x63':		ord(self.__data[0x63]),
    #		unknown:
                '0x64':		ord(self.__data[0x64]),     # not used? always = 255 ?
                '0x65':		ord(self.__data[0x65]),     # not used? always = 255 ?
                '0x66':		ord(self.__data[0x66]),     # not used? always = 0 ?
                '0x67':		ord(self.__data[0x67]),     # surrender to #0 normally -1, else player to give colonies to
                '0x68':		ord(self.__data[0x68]),     # surrender to #1 normally -1, else player to give colonies to
                '0x69':		ord(self.__data[0x69]),     # surrender to #2 normally -1, else player to give colonies to
                '0x6a':		ord(self.__data[0x6a]),     # surrender to #3 normally -1, else player to give colonies to
                '0x6b':		ord(self.__data[0x6b]),     # surrender to #4 normally -1, else player to give colonies to
                '0x6c':		ord(self.__data[0x6c]),     # surrender to #5 normally -1, else player to give colonies to
                '0x6d':		ord(self.__data[0x6d]),     # surrender to #6 normally -1, else player to give colonies to
                '0x6e':		ord(self.__data[0x6e]),     # surrender to #7 normally -1, else player to give colonies to
                '0x6f':		ord(self.__data[0x6f]),     # in nebula
                '0x70':		ord(self.__data[0x70])      # artifacts_gave_app
    # /import_from_moo2
"""

class UnexploredStar(Star):
    """
                stars[star_id] = {
                    'id':               star.get_id(),
                    'name':             "Unexplored",
                    'x':                star.get_x(),
                    'y':                star.get_y(),
                    'size':             star.size(),
                    'pict_type':        star.pict_type(),
                    'class':            star.get_class(),
                    'visited':          star.visited
                }
    """
    def __init__(self, star_id, x, y, size, pict_type, cl):
        self.set_id(star_id)
        self.set_name("Unexplored")
        self.set_x(x)
        self.set_y(y)
        self.set_size(size)
        self.set_class(cl)
        self.set_pict_type(pict_type)

    def visited(self):
        return False

    def visited_by_player(self, player_id):
        return False
    