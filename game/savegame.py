import os
import sys

sys.path.append("classes")

MAX_TECHNOLOGIES = 0xCB             # 203 technologies

def get_int(b0, b1, b2 = 0, b3 = 0):
    return b0 + (b1 << 8) + (b2 << 16) + (b3 << 24)

def read_short_int(data, offset):
    return ord(data[offset]) + (ord(data[offset+1]) << 8)

def read_long_int(data, offset):
    return ord(data[offset]) + (ord(data[offset+1]) << 8) + (ord(data[offset+2]) << 16) + (ord(data[offset+3]) << 24)

def read_byte(data, offset):
    return ord(data[offset])

def read_signed_byte(data, offset):
    v = ord(data[offset])
    if v > 0x7f:
        v -= 0x100
    return v

def read_string(data, offset, length):
    return data[offset:offset + length].rstrip(chr(0) + chr(1) + chr(2) + chr(3)).split(chr(0))[0]


def bitmask_to_player_id_list(bitmask):
    list = []
    if bitmask & 1:
        list.append(0)
    if bitmask & 2:
        list.append(1)
    if bitmask & 4:
        list.append(2)
    if bitmask & 8:
        list.append(3)
    if bitmask & 16:
        list.append(4)
    if bitmask & 32:
        list.append(5)
    if bitmask & 64:
        list.append(6)
    if bitmask & 128:
        list.append(7)
    return list

"""
"""
def list_savegames():
    from stat import ST_MTIME
    list = []
    for n in range(1,11):
        filename = "SAVE%i.GAM" % n
        savefile = open(filename, 'rb')
        data = savefile.read(64)
        savefile.close()
        info = read_game(data)
        sg_stat = os.stat(filename)
        info['ST_MTIME'] = sg_stat[ST_MTIME]
        list.append(info)
    return list

"""
    read_game
"""
def read_game(data):
    return {
        'name':					read_string(data, 0x04, 23).lstrip(chr(0) + chr(1) + chr(2) + chr(3)),
        'stardate':				read_short_int(data, 0x29),
        'end_of_turn_summary':			read_byte(data, 0x2E),
        'end_of_turn_wait':			read_byte(data, 0x2F),
        'random_events':			read_byte(data, 0x30),
        'enemy_moves':				read_byte(data, 0x31),
        'expanding_help':			read_byte(data, 0x32),
        'auto_select_ships':			read_byte(data, 0x33),
        'animations':				read_byte(data, 0x34),
        'auto_select_colony':			read_byte(data, 0x35),
        'show_relocation_lines':		read_byte(data, 0x36),
        'show_gnn_report':			read_byte(data, 0x37),
        'auto_delete_trade_good_housing':	read_byte(data, 0x38),
        'auto_save_game':			read_byte(data, 0x39),
        'show_only_serious_turn_summary':	read_byte(data, 0x3A),
        'ship_initiative':			read_byte(data, 0x3B)
    }

def read_galaxy(data):
    return {
        'size_factor':	read_byte(data, 0x31be4),
        'width':	get_int(ord(data[0x31be9]), ord(data[0x31bea])),
        'height':	get_int(ord(data[0x31beb]), ord(data[0x31bec]))
    }

def read_heroes(data, debug = False):
    HEROES_DATA_OFFSET	= 0x19a9b
    HERO_RECORD_SIZE	= 0x3b 		# = 59
    heroes = []
    for i in range(67):
        offset = HEROES_DATA_OFFSET + (HERO_RECORD_SIZE * i)

        if debug:
            print "hero @ %x" % offset

        heroes.append({
            'id':               i,
            'name':		data[offset:offset + 0x0f].rstrip(chr(0)).split(chr(0))[0],
    	    'title':		data[offset + 0x0f:offset + 0x23].rstrip(chr(0)).split(chr(0))[0],
            'type':		read_byte(data, offset + 0x23),
            'experience':	read_short_int(data, offset + 0x24),
            'common_skills':    read_long_int(data, offset + 0x26),
            'special_skills':   read_long_int(data, offset + 0x2a),
            'tech1':            read_byte(data, offset + 0x2e),
            'tech2':            read_byte(data, offset + 0x2f),
            'tech3':            read_byte(data, offset + 0x30),
            'picture':          read_byte(data, offset + 0x31),
            'skill_value':	read_short_int(data, offset + 0x32),
            'level':		read_byte(data, offset + 0x34),
            'location':		read_short_int(data, offset + 0x35),
            'eta':		read_byte(data, offset + 0x37),
            'level_up':		read_byte(data, offset + 0x38),
            'status':		read_byte(data, offset + 0x39),
            'player':		read_byte(data, offset + 0x3a)
        })

    if debug:
        i += 1 
        offset = 0x19a9b + (59 * i)
        print "STOP hero @ %x" % offset
    return heroes
# end func read_heroes

def read_colony_population(data, colony_offset):
    population	= ord(data[colony_offset + 0x0A])
#    colonists_raw = []
    colonists = {0x02: [], 0x03: [], 0x82: []}
    for i in range(population):
        offset = colony_offset + 0x0C + (4 * i)
        t = (read_byte(data, offset) & 0x80) + (read_byte(data, offset + 1) & 3)
        colonists[t].append({
            'a':	read_byte(data, offset),
            'b':	read_byte(data, offset + 1),
            'c':	read_byte(data, offset + 2),
            'd':	read_byte(data, offset + 3),
#	    'type':	(ord(data[offset]) & 0x80) + (ord(data[offset + 1]) & 3),
            'r1':	(read_byte(data, offset) & 0x70) >> 4,
            'race':	(read_byte(data, offset) & 0x07)
        })
    return colonists
# end func read_colony_population

def read_colonies(data, planets, debug = False):
    COLONIES_DATA_OFFSET	= 0x0025d
    COLONY_RECORD_SIZE		= 361
    c = get_int(ord(data[0x0000025b]), ord(data[0x0000025c]))

    if debug:
        print "Number of colonies to read: %i" % c

    colonies = []

    for i in range(c):
        offset	= COLONIES_DATA_OFFSET + (COLONY_RECORD_SIZE * i)
        colony = Colony()
        colony.import_from_moo2(i, data[offset:offset + COLONY_RECORD_SIZE])
#	owner	= ord(data[offset])
        colonies.append(colony)
    return colonies
# end func read_colonies
        
def read_players(data, debug = False):
    #
    # Players
    #

    players = []

    if debug:
        print
        print "=== Players ==="

    for i in range(8):
        offset		= 0x01aa0f + (3753 * i)
        if debug:
            print "player @ %x" % offset

        players.append({
            'emperor':		data[offset:offset + 0x0F].rstrip(chr(0)).split(chr(0))[0],
            'race':		data[offset + 0x14:offset + 0x24].rstrip(chr(0)).split(chr(0))[0],
#	    'race':		ord(data[offset + 0x24]),
            'picture':		read_byte(data, offset + 0x24),
            'color':		read_byte(data, offset + 0x25),
            'personality':	ord(data[offset + 0x26]),
            'objective':	ord(data[offset + 0x27]),			# 100 = Human Player
            # 0x28 ~ 0x2f	unknown
            'tax_rate':		ord(data[offset + 0x30]),
            'BC':		get_int(ord(data[offset + 0x31]), ord(data[offset + 0x32]), ord(data[offset + 0x33]), ord(data[offset + 0x34])),
            'total_frighters':	get_int(ord(data[offset + 0x35]), ord(data[offset + 0x36])),
            'used_frighters':	get_int(ord(data[offset + 0x37]), ord(data[offset + 0x38])),
            'command_points':	get_int(ord(data[offset + 0x39]), ord(data[offset + 0x3A])),
            # 0x3B ~ 0xA8	unknown
            # 0xA0		?
            # 0xA1		?
            # 0xA2		?
            # 0xA3		?
            # 0xA4		?
            # 0xA5		?
            # 0xA6		?
            # 0xA7		?
            # 0xA8		?
            'total_production':	get_int(ord(data[offset + 0xA9]), ord(data[offset + 0xAA])),
            'RP':		get_int(ord(data[offset + 0xAB]), ord(data[offset + 0xAC])),
            # 0xAD		unknown	...
#		... pracant na vedce ... 0x10 -> 0x0f
            # 0xAE		unknown
            'food':		get_int(ord(data[offset + 0x0AF]), ord(data[offset + 0x0B0])),
            'yearly_bc':	get_int(ord(data[offset + 0x0B1]), ord(data[offset + 0x0B2])),
            'research_progress':get_int(ord(data[offset + 0x1EA]), ord(data[offset + 0x1EB])),
            'research_area':    ord(data[offset + 0x320]),
#               0x00 = None
#		0x04 = Construction
#		0x07 = Force Fields
#		0x0a = Sociology
#		0x12 = Biology
#		0x16 = Chemistry
#		0x1c = Computers
#		0x37 = Power
#		0x39 = Physics
            'research_item':    	ord(data[offset + 0x321]),
            'racepicks':	{
            			    'goverment':		ord(data[offset + 0x89E]),
                                    'population':		read_signed_byte(data, offset + 0x89F),
                                    'farming':			read_signed_byte(data, offset + 0x8A0),
                                    'industry':			read_signed_byte(data, offset + 0x8A1),
                                    'science':			read_signed_byte(data, offset + 0x8A2),
                                    'money':			read_signed_byte(data, offset + 0x8A3),
                                    'ship_defense':		read_signed_byte(data, offset + 0x8A4),
                                    'ship_attack':		read_signed_byte(data, offset + 0x8A5),
                                    'ground_combat':		read_signed_byte(data, offset + 0x8A6),
                                    'spying':			read_signed_byte(data, offset + 0x8A7),
                                    'low_g':			ord(data[offset + 0x8A8]),
                                    'high_g':			ord(data[offset + 0x8A9]),
                                    'aquatic':			ord(data[offset + 0x8AA]),
                                    'subterranean':		ord(data[offset + 0x8AB]),
                                    'large_home_world':		ord(data[offset + 0x8AC]),
                                    'rich_home_world':		ord(data[offset + 0x8AD]),
                                    # where is poor_home_worlds?
                                    'artifacts_home_world':	ord(data[offset + 0x8AE]),
                                    'cybernetic':		ord(data[offset + 0x8AF]),
                                    'lithovore':		ord(data[offset + 0x8B0]),
                                    'repulsive':		ord(data[offset + 0x8B1]),
                                    'charismatic':		ord(data[offset + 0x8B2]),
                                    'uncreative':		ord(data[offset + 0x8B3]),
                                    'creative':			ord(data[offset + 0x8B4]),
                                    'tolerant':			ord(data[offset + 0x8B5]),
                                    'fantastic_traders':	ord(data[offset + 0x8B6]),
                                    'telepathic':		ord(data[offset + 0x8B7]),
                                    'lucky':			ord(data[offset + 0x8B8]),
                                    'omniscience':		ord(data[offset + 0x8B9]),
                                    'stealthy_ships':		ord(data[offset + 0x8BA]),
                                    'trans_dimensional':	ord(data[offset + 0x8BB]),
                                    'warlord':			ord(data[offset + 0x8BC])
                                },
#	    'technologies':	[],
            'known_techs':	[],
            'prototypes':	[],
            'tributes':		[]
        })

        for ii in range(MAX_TECHNOLOGIES):
            offset2 = offset + 0x117 + ii
#            players[-1]['technologies'].append(ord(data[offset2]))
            if ord(data[offset2]) == 3:
                players[-1]['known_techs'].append(ii + 1)

#	0x1e2
#
        for ii in range(6):
            offset2 = offset + 0x325 + (ii * 0x63)
#            proto_name = data[offset2:offset2 + 0x0F].rstrip(chr(0)).split(chr(0))[0]
#            players[-1]['prototypes'].append({
#		'name':	data[offset2:offset2 + 0x0F].rstrip(chr(0)).split(chr(0))[0]
#	    })

            proto = read_ship_design(data, offset2)
#            if proto['name']:
#                print("")
#                print("=== Prototype @%i: ===" % offset2)
#                print(proto)
#                print("=== /Prototype ===")
#                print("")

            players[-1]['prototypes'].append(proto)

        for ii in range(7):
            offset2 = offset + 0x649 + (ii)
            players[-1]['tributes'].append(ord(data[offset2]))

    if debug:
        i += 1 
        offset = 0x01aa0f + (3753 * i)
        print "STOP player @ %x" % offset

    players.append({
        'race':		"Antareans",
        'emperor':	"?"
    })
    players.append({
        'race':		"Guardian",
        'emperor':	"?"
    })
    players.append({
        'race':		"Amoeba",
        'emperor':	"?"
    })
    players.append({
        'race':		"Crystal",
        'emperor':	"?"
    })
    players.append({
        'race':		"Dragon",
        'emperor':	"?"
    })
    players.append({
        'race':		"Eel",
        'emperor':	"?"
    })
    players.append({
        'race':		"Hydra",
        'emperor':	"?"
    })

    return players
#end func read_players

def read_stars(data, debug = False):
    #       http://www.spheriumnorth.com/orion-forum/nfphpbb/viewtopic.php?p=149
    SOLAR_SYSTEMS_COUNT_OFFSET	= 0x17ad1
    SOLAR_SYSTEMS_DATA_OFFSET	= 0x17ad3
    SOLAR_SYSTEM_RECORD_SIZE	= 0x71
    systems = []
    c = ord(data[SOLAR_SYSTEMS_COUNT_OFFSET])
    for i in range(c):
#    for i in range(72):
        offset = SOLAR_SYSTEMS_DATA_OFFSET + (SOLAR_SYSTEM_RECORD_SIZE * i)
        if debug:
            print "system @ %x" % offset
        systems.append({
            'id':			i,
            'name':     		read_string(data, offset, 15),
            'x':        		read_short_int(data, offset + 0x0f),
            'y':        		read_short_int(data, offset + 0x11),
            'size':     		read_byte(data, offset + 0x13),
            'owner':			read_byte(data, offset + 0x14),		# primary owner
            'pict_type':		read_byte(data, offset + 0x15),
            'class':    		read_byte(data, offset + 0x16),
            'last_planet_selected':	[
                                            read_byte(data, offset + 0x17),
                                            read_byte(data, offset + 0x18),
            				    read_byte(data, offset + 0x19),
                                            read_byte(data, offset + 0x1A),
            				    read_byte(data, offset + 0x1B),
                                            read_byte(data, offset + 0x1C),
                                            read_byte(data, offset + 0x1D),
                                            read_byte(data, offset + 0x1E)
                                        ],
            'black_hole_blocks':	[
                                        ],
            '0x1f':		ord(data[offset + 0x1f]),
            '0x20':		ord(data[offset + 0x20]),
            '0x21':		ord(data[offset + 0x21]),
            '0x22':		ord(data[offset + 0x22]),
            '0x23':		ord(data[offset + 0x23]),
            '0x24':		ord(data[offset + 0x24]),
            '0x25':		ord(data[offset + 0x25]),
            '0x26':		ord(data[offset + 0x26]),
            '0x27':		ord(data[offset + 0x27]),
            'special':  	ord(data[offset + 0x28]),
            'wormhole': 	ord(data[offset + 0x29]),
            '0x2a':		ord(data[offset + 0x2a]),	# blockaded? ( 0 | 1 )
            '0x2b':		ord(data[offset + 0x2b]),
            '0x2c':		ord(data[offset + 0x2c]),
            '0x2d':		ord(data[offset + 0x2d]),
            '0x2e':		ord(data[offset + 0x2e]),
            '0x2f':		ord(data[offset + 0x2f]),
            '0x30':		ord(data[offset + 0x30]),
            '0x31':		ord(data[offset + 0x31]),
            '0x32':		ord(data[offset + 0x32]),
            'visited':		ord(data[offset + 0x33]),	# bitmask as boleans for each player
            '0x34':		ord(data[offset + 0x34]),
            '0x35':		ord(data[offset + 0x35]),
            '0x36':		ord(data[offset + 0x36]),
            '0x37':		ord(data[offset + 0x37]),
            '0x38':		ord(data[offset + 0x38]),
            'indictor': 	ord(data[offset + 0x39]),	# 0 = none, 1-8 = owner player 0-7  ( http://code.google.com/p/moo2x/wiki/star )
            '0x3a':		ord(data[offset + 0x3a]),
            '0x3b':		ord(data[offset + 0x3b]),
            '0x3c':		ord(data[offset + 0x3c]),
            '0x3d':		ord(data[offset + 0x3d]),
            '0x3e':		ord(data[offset + 0x3e]),
            'artemis':  	ord(data[offset + 0x3f]),	# 0 = none, 1-8=owner player 0-7 ( http://code.google.com/p/moo2x/wiki/star )
            '0x40':		ord(data[offset + 0x40]),	# Star has dimensional portal ?
            '0x41':		ord(data[offset + 0x41]),
            '0x42':		ord(data[offset + 0x42]),
            '0x43':		ord(data[offset + 0x43]),
            '0x44':		ord(data[offset + 0x44]),
            '0x45':		ord(data[offset + 0x45]),
            '0x46':		ord(data[offset + 0x46]),
            '0x47':		ord(data[offset + 0x47]),
            '0x48':		ord(data[offset + 0x48]),
            '0x49':		ord(data[offset + 0x49]),
            'objects':   	[
                                    get_int(ord(data[offset + 0x4a]), ord(data[offset + 0x4b])),
        			    get_int(ord(data[offset + 0x4c]), ord(data[offset + 0x4d])),
        			    get_int(ord(data[offset + 0x4e]), ord(data[offset + 0x4f])),
        			    get_int(ord(data[offset + 0x50]), ord(data[offset + 0x51])),
        			    get_int(ord(data[offset + 0x52]), ord(data[offset + 0x53]))
                                ],
#		??? Relocation star id (0-7 player #, not sure about size of array. ) 
            '0x54':		ord(data[offset + 0x54]),
            '0x55':		ord(data[offset + 0x55]),
            '0x56':		ord(data[offset + 0x56]),
            '0x57':		ord(data[offset + 0x57]),
            '0x58':		ord(data[offset + 0x58]),
            '0x59':		ord(data[offset + 0x59]),
            '0x5a':		ord(data[offset + 0x5a]),
            '0x5b':		ord(data[offset + 0x5b]),
            '0x5c':		ord(data[offset + 0x5c]),
            '0x5d':		ord(data[offset + 0x5d]),
            '0x5e':		ord(data[offset + 0x5e]),
            '0x5f':		ord(data[offset + 0x5f]),
            '0x60':		ord(data[offset + 0x60]),
            '0x61':		ord(data[offset + 0x61]),
            '0x62':		ord(data[offset + 0x62]),
            '0x63':		ord(data[offset + 0x63]),
#		unknown:
            '0x64':		ord(data[offset + 0x64]),
            '0x65':		ord(data[offset + 0x65]),
            '0x66':		ord(data[offset + 0x66]),
            '0x67':		ord(data[offset + 0x67]),
            '0x68':		ord(data[offset + 0x68]),
            '0x69':		ord(data[offset + 0x69]),
            '0x6a':		ord(data[offset + 0x6a]),
            '0x6b':		ord(data[offset + 0x6b]),
            '0x6c':		ord(data[offset + 0x6c]),
            '0x6d':		ord(data[offset + 0x6d]),
            '0x6e':		ord(data[offset + 0x6e]),
            '0x6f':		ord(data[offset + 0x6f]),
            '0x70':		ord(data[offset + 0x70])
            })
    if debug:
        i += 1
        offset = 0x17ad3 + (SOLAR_SYSTEM_RECORD_SIZE * i)
        print "STOP system @ %x" % offset
#    blah
    return systems
# end func read_stars

def read_planets(data, systems, debug = False):
#    PLANETS_COUNT_OFFSET	= 0x162e7
    PLANETS_DATA_OFFSET		= 0x162e9
    PLANET_RECORD_SIZE		= 0x11
    planets = []

    c = 0
    for system in systems:
        for o in system['objects']:
            if o != 0xffff:
                c += 1

#    c = get_int(ord(data[PLANETS_COUNT_OFFSET]), ord(data[PLANETS_COUNT_OFFSET + 1]))
    c = 250

    if debug:
        print "Reading planetary objects ..."
        print "    count: %i" % c

    for i in range(c):
        offset = PLANETS_DATA_OFFSET + (PLANET_RECORD_SIZE * i)
#        system_number = ord(data[offset + 0x02])
#        position = ord(data[offset + 0x03])
        planets.append({
            'colony':           read_short_int(data, offset),	# 0xffff = no colony here
            'parent_star':	read_byte(data, offset + 0x02),
            'position':		read_byte(data, offset + 0x03),
            'type':             read_byte(data, offset + 0x04),
            'size':             read_byte(data, offset + 0x05),
            'gravity':          read_byte(data, offset + 0x06),
            'group':            read_byte(data, offset + 0x07),   # not used
            'terrain':          read_byte(data, offset + 0x08),
            'picture':          read_byte(data, offset + 0x09),   # Background image on colony screen (0-5=image in planets.lbx)
            'minerals':         read_byte(data, offset + 0x0a),
            'foodbase':         read_byte(data, offset + 0x0b),
            'terraformations':  read_byte(data, offset + 0x0c),
            'max_farms':        read_byte(data, offset + 0x0d),   # unknown (Initial value is based on Planet Size but changes if colonized), 2=tiny, 4=small, 5=med, 7=large, A=huge
            'max_population':   read_byte(data, offset + 0x0e),
            'special':          read_byte(data, offset + 0x0f),
            'flags':            read_byte(data, offset + 0x10)    # (bit 2 = Soil Enrichment)
        })
    return planets
# end func read_planets

def read_ship_design(data, offset):
    MAX_WEAPONS = 8
    weapons = []
    for i in range(MAX_WEAPONS):
        offset2 = offset + 0x1C + (8 * i)
        weapon = read_byte(data, offset2)
        if (weapon > 0):
            weapons.append({
                'weapon':		weapon,
                'count':		read_byte(data, offset2 + 0x02),
                'current_count':	read_byte(data, offset2 + 0x03),
                'arc':			read_byte(data, offset2 + 0x04),
                'beam_mods':		read_byte(data, offset2 + 0x05),
                'missile_mods':		read_byte(data, offset2 + 0x06),
                'ammo':			read_byte(data, offset2 + 0x07)
            })
    return {
            'name':		read_string(data, offset, 16),
            'size':		read_byte(data, offset + 0x10),
    	    'type':		read_byte(data, offset + 0x11),
            'shield':		read_byte(data, offset + 0x12),
            'drive':		read_byte(data, offset + 0x13),
            'speed':		read_byte(data, offset + 0x14),
            'computer':		read_byte(data, offset + 0x15),
            'armor':		read_byte(data, offset + 0x16),
            'special_devices':	data[offset + 0x17:offset + 0x1C],	# char  special_device_flags[(MAX_SPECIALS+7)/8];
            'weapons':		weapons,
            'picture':		read_byte(data, offset + 0x5C),
            'builder':		read_byte(data, offset + 0x5D),		# or previous owner?
            'cost':		read_short_int(data, offset + 0x5E),
            'combat_speed':	read_byte(data, offset + 0x60),
            'build_date':	read_short_int(data, offset + 0x61)
    }
# end func read_ship_design

def read_ships(data, debug = False):
    SAVE_SHIP_COUNT_OFFSET    = 0x21f56
    SAVE_SHIPS_OFFSET         = 0x21f58
    SAVE_SHIP_RECORD_SIZE     = 0x81        # = 129
#    SAVE_SHIP_WEAPONS_OFFSET  = 0x1c
#    SAVE_SHIP_SPECIALS_OFFSET = 0x17

    c = get_int(ord(data[SAVE_SHIP_COUNT_OFFSET]), ord(data[SAVE_SHIP_COUNT_OFFSET + 1]))
    ships = []
    
    for i in range(c):
        offset          = SAVE_SHIPS_OFFSET + (SAVE_SHIP_RECORD_SIZE * i)
        if debug:
    	    print "ship @ %x" % offset
            
        ships.append({
            'design':			read_ship_design(data, offset),
            'owner':			read_byte(data, offset + 0x63),
            'status':			read_byte(data, offset + 0x64),           # 0 = orbitting, 2 = traveling, 5 = destroyed?
            'location':			read_byte(data, offset + 0x65),
            'location_x':		read_byte(data, offset + 0x66),
            'x':			read_short_int(data, offset + 0x67),
            'y':			read_short_int(data, offset + 0x69),
            'group_has_navigator':	read_byte(data, offset + 0x6B),		# does the moving group have navigator?
            'travelling_speed':		read_byte(data, offset + 0x6C),		# possibly less than ftl_type
            'turns_left':		read_byte(data, offset + 0x6D),		# until arrival
            'shield_damage_percent':	read_byte(data, offset + 0x6E),
            'drive_damage_percent':	read_byte(data, offset + 0x6F),
            'computer_damage':		read_byte(data, offset + 0x70),
            'crew_quality':		read_byte(data, offset + 0x71),
            'crew_experience':		read_short_int(data, offset + 0x72),
            'officer_id':		read_short_int(data, offset + 0x74),
            'special_device_damage':	data[offset + 0x76:offset + 0x7B],	# bit flag array
            'armor_damage':		read_short_int(data, offset + 0x7B),
            'structural_damage':	read_short_int(data, offset + 0x7D),
            'mission':			read_byte(data, offset + 0x7F),		# AI field
            'just_built':		read_byte(data, offset + 0x80),
        })

    if debug:
        i += 1		
        offset          = SAVE_SHIPS_OFFSET + (SAVE_SHIP_RECORD_SIZE * i)
        print "STOP ship @ %x" % offset
    return ships
# end func read_ships

def read_savegame(filename):
    pass
    print "Loading savegame '%s'" % filename
    
    filesize = os.path.getsize(filename)
    savefile = open(filename, 'rb')
    data = savefile.read(filesize)
    savefile.close()

    game	= read_game(data)
    galaxy	= read_galaxy(data)
    heroes	= read_heroes(data)			# complete
    players	= read_players(data)
    stars	= read_stars(data)
    planets	= read_planets(data, stars)		# complete
    colonies	= read_colonies(data, planets)
    ships	= read_ships(data)			# complete

#    for i in range(len(stars)):
    stars_by_coordinates = {}
#    for star in stars:

    for i in range(len(stars)):
        star = stars[i]
        k = "%i:%i" % (star['x'], star['y'])
        stars_by_coordinates[k] = star
        num = 0
        for object in star['objects']:
#	    print "object: %i" % object
            if object != 0xffff:
                num += 1
                planets[object]['num'] = num

#    print "Attaching planets to colonies..."
    for i in range(len(colonies)):
        colony		= colonies[i]
        planet_id	= colony.planet_id
        if colony.owner() < 0xff:
#	    print "	... planet #%i to colony #%i" % (planet_id, i)
            colony.assign_planet(planets[planet_id])
    	    colony.name = "%s %i" % (stars[planets[planet_id]['parent_star']]['name'], planets[planet_id]['num'])
#	else:
#	    print "	... colony #%i has owner 0xff" % (i)
#    print "	Finished"

    return {
        'game':			game,
        'galaxy':		galaxy,
        'heroes':		heroes,
        'players':		players,
        'stars':		stars,
        'stars_by_coordinates':	stars_by_coordinates,
        'planets':		planets,
        'colonies':		colonies,
        'ships':		ships
    }
