import os

import lbx

import universe

def compose_int(b0, b1, b2 = 0, b3 = 0):
    return b0 + (b1 << 8) + (b2 << 16) + (b3 << 24)
# end func get_int

def bitarray(bytes_array):
    """
        returns a list of booleans from bit-values of given bytearray
    """
    ba = []
    index = 1
    for byte in bytes_array:
        for bit in range(7):
            if byte & 1 << bit:
                ba.append(index)
            index += 1
    return ba

class Moo2Savegame(object):
    """
    
    """

    def __init__(self, filename):
        """
        Loads the original MOO2 savegame
        """
        filesize = os.path.getsize(filename)
        savefile = open(filename, 'rb')
        self.__data = savefile.read(filesize)
        savefile.close()

    def parse_game(self):
        return {
            'name':				lbx.read_string(self.__data, 0x04, 23).lstrip(chr(0) + chr(1) + chr(2) + chr(3)),
            'end_of_turn_summary':		lbx.read_byte(self.__data, 0x2E),
            'end_of_turn_wait':			lbx.read_byte(self.__data, 0x2F),
            'random_events':			lbx.read_byte(self.__data, 0x30),
            'enemy_moves':			lbx.read_byte(self.__data, 0x31),
            'expanding_help':			lbx.read_byte(self.__data, 0x32),
            'auto_select_ships':		lbx.read_byte(self.__data, 0x33),
            'animations':			lbx.read_byte(self.__data, 0x34),
            'auto_select_colony':		lbx.read_byte(self.__data, 0x35),
            'show_relocation_lines':		lbx.read_byte(self.__data, 0x36),
            'show_gnn_report':			lbx.read_byte(self.__data, 0x37),
            'auto_delete_trade_good_housing':	lbx.read_byte(self.__data, 0x38),
            'auto_save_game':			lbx.read_byte(self.__data, 0x39),
            'show_only_serious_turn_summary':	lbx.read_byte(self.__data, 0x3A),
            'ship_initiative':			lbx.read_byte(self.__data, 0x3B),
        }
    # end func read_game

    def parse_galaxy(self):
        return {
            'size_factor':	lbx.read_byte(self.__data, 0x31be4),
            'width':            compose_int(ord(self.__data[0x31be9]), ord(self.__data[0x31bea])),
            'height':           compose_int(ord(self.__data[0x31beb]), ord(self.__data[0x31bec])),
            'stardate':		lbx.read_short_int(self.__data, 0x29),
        }
    # end func parse_galaxy

    def parse_hero_common_skills(self, type, skills_flags):
#        print "Moo2Savegame::parse_hero_common_skills ... type = %i, skills_flags = %i" % (type, skills_flags)
        print " * common_skills = %i" % skills_flags
        if type == 1:
            # Colony Leader
            if skills_flags & 1:
                print ""
            if skills_flags & 2:
                print ""
            if skills_flags & 4:
                print ""
            if skills_flags & 8:
                print ""
            if skills_flags & 16:
                print ""
            if skills_flags & 32:
                print ""
            if skills_flags & 64:
                print ""
            if skills_flags & 128:
                print ""
            if skills_flags & 256:
                print ""
            if skills_flags & 512:
                print ""
    # end func parse_hero_common_skills

    def parse_hero_skills(self, type, common_skills, special_skills):
#        print "Moo2Savegame::parse_hero_common_skills ... type = %i, skills_flags = %i" % (type, skills_flags)
#        print " * special_skills = %i" % special_skills
        skills = {}
        
        if common_skills & 1:
            skills['assasin']       = 2             # bit  0 = Assasin
        if common_skills & 2:
            skills['assasin']       = 3             # bit  1 = Assasin*

        if common_skills & 4:
            skills['commando']      = 2             # bit  2 = Commando
        if common_skills & 8:
            skills['commando']      = 3             # bit  3 = Commando*

        if common_skills & 16:
            skills['diplomat']      = 10            # bit  4 = Diplomat
        if common_skills & 32:
            skills['diplomat']      = 15            # bit  5 = Diplomat*

        if common_skills & 64:
            skills['famous']        = 60            # bit  6 = Famous
        if common_skills & 128:
            skills['famous']        = 90            # bit  7 = Famous*

        if common_skills & 256:
            skills['megawealth']    = 10            # bit  8 = Megawealth
        if common_skills & 512:
            skills['megawealth']    = 15            # bit  9 = Megawealth*

        if common_skills & 1024:
            skills['operations']    = 2             # bit 10 = Operations
        if common_skills & 2048:
            skills['operations']    = 3             # bit 11 = Operations*

        if common_skills & 4096:
            skills['researcher']    = 5             # bit 12 = Researcher
        if common_skills & 8192:
            skills['researcher']    = 7.5           # bit 13 = Researcher*

        if common_skills & 16384:
            skills['spy_master']    = 2             # bit 14 = Spy Master
        if common_skills & 32768:
            skills['spy_master']    = 3             # bit 15 = Spy Master*

        if common_skills & 65536:
            skills['telepath']      = 2             # bit 16 = Telepath
        if common_skills & 131072:
            skills['telepath']      = 3             # bit 17 = Telepath*

        if common_skills & 262144:
            skills['trader']        = 10            # bit 18 = Trader
        if common_skills & 524288:
            skills['trader']        = 15            # bit 19 = Trader*


        if type == 0:
            pass
        elif type == 1:
            # Colony Leader
            if special_skills & 1:
                skills['pollution_bonus'] = 10      # bit  0 = Environmentalist
            if special_skills & 2:
                skills['pollution_bonus'] = 15      # bit  1 = Environmentalist*

            if special_skills & 4:
                skills['farming_bonus'] = 10        # bit  2 = Farming Leader
            if special_skills & 8:
                skills['farming_bonus'] = 15        # bit  3 = Farming Leader*

            if special_skills & 16:
                skills['income_bonus'] = 10         # bit  4 = Financial Leader
            if special_skills & 32:
                skills['income_bonus'] = 15         # bit  5 = Financial Leader*

            if special_skills & 64:
                skills['instructor'] = 0.7          # bit  6 = Instructor
            if special_skills & 128:
                skills['instructor'] = 1.1          # bit  7 = Instructor*

            if special_skills & 256:
                skills['industry_bonus'] = 10       # bit  8 = Labor Leader
            if special_skills & 512:
                skills['industry_bonus'] = 15       # bit  9 = Labor Leader*

            if special_skills & 1024:
                skills['medicine'] = 10             # bit 10 = Medicine
            if special_skills & 2048:
                skills['medicine'] = 15             # bit 11 = Medicine*

            if special_skills & 4096:
                skills['research_bonus'] = 10       # bit 12 = Science Leader
            if special_skills & 8192:
                skills['research_bonus'] = 15       # bit 13 = Science Leader*

            if special_skills & 16384:
                skills['morale_bonus'] =  0         # bit 14 = Spiritual Leader
            if special_skills & 32768:
                skills['morale_bonus'] = 7.5        # bit 15 = Spiritual Leader*

            if special_skills & 65536:
                skills['tactics'] = 6               # bit 16 = Tactics
            if special_skills & 131072:
                skills['tactics'] = 9               # bit 17 = Tactics*

            return skills
    # end func parse_hero_special_skills

    def parse_heroes(self):
        HEROES_DATA_OFFSET	= 0x19a9b
        HERO_RECORD_SIZE	= 0x3b 		# = 59
        heroes = {}
        for i in range(67):
            hero_id = i
            offset = HEROES_DATA_OFFSET + (HERO_RECORD_SIZE * i)

#            print "hero @ %x" % offset

            type            = lbx.read_byte(self.__data, offset + 0x23)
            common_skills   = lbx.read_long_int(self.__data, offset + 0x26)
            special_skills  = lbx.read_long_int(self.__data, offset + 0x2a)

            heroes[hero_id] = {
                'id':               i,
#                'name':             data[offset:offset + 0x0f].rstrip(chr(0)).split(chr(0))[0],
                'name':             lbx.read_string(self.__data, offset, 15),
#                'title':            data[offset + 0x0f:offset + 0x23].rstrip(chr(0)).split(chr(0))[0],
                'title':            lbx.read_string(self.__data, offset, 35),
                'type':             type,
                'experience':       lbx.read_short_int(self.__data, offset + 0x24),
                'tech1':            lbx.read_byte(self.__data, offset + 0x2e),
                'tech2':            lbx.read_byte(self.__data, offset + 0x2f),
                'tech3':            lbx.read_byte(self.__data, offset + 0x30),
                'picture':          lbx.read_byte(self.__data, offset + 0x31),
                'skill_value':      lbx.read_short_int(self.__data, offset + 0x32),
                'level':            lbx.read_byte(self.__data, offset + 0x34),
                'location':         lbx.read_short_int(self.__data, offset + 0x35),
                'eta':              lbx.read_byte(self.__data, offset + 0x37),
                'level_up':         lbx.read_byte(self.__data, offset + 0x38),
                'status':           lbx.read_byte(self.__data, offset + 0x39),
                'player':           lbx.read_byte(self.__data, offset + 0x3a),
                'skills':           self.parse_hero_skills(type, common_skills, special_skills),
                'common_skills':    common_skills,
                'special_skills':   special_skills,
            }
#            if heroes[hero_id]['player'] == 0:
#                print "Moo2Savegame::parse_heroes ... hero_id = %i, name = %s" % (hero_id, heroes[hero_id]['name'])
#                print " * level = %i" % heroes[hero_id]['level']
#                print " * skill_value = %i" % heroes[hero_id]['skill_value']
#                print " * experience = %i" % heroes[hero_id]['experience']
#                print " * status = %i" % heroes[hero_id]['status']
            
#        i += 1
#        offset = 0x19a9b + (59 * i)
#        print "STOP hero @ %x" % offset
        return heroes
    # end func parse_heroes

    def parse_known_techs(self, offset):
        known_techs = []
        for i in range(203):               # original moo2 mas 203 usable technologies
#            offset2 = offset + 0x117 + i
            tech_status = ord(self.__data[offset + i])
 #           if tech_status and tech_status != 1:
#               print "tech_status = %i" % tech_status
            if tech_status == 3:
                known_techs.append(i + 1)
        return known_techs
    # end func parse_known_techs

    def parse_players(self):
        #
        # Players
        #
        PLAYERS_DATA_OFFSET	= 0x01aa0f
        PLAYER_RECORD_SIZE	= 3753

        pl = {}
        players = {}

#        print
#        print "=== Players ==="

        for i in range(8):

            player_id = i
            offset		= PLAYERS_DATA_OFFSET + (PLAYER_RECORD_SIZE * i)
#            print "player @ %x" % offset

#            players.append({
            players[player_id] = universe.Player(player_id)
#            pl[player_id].import_from_moo2(self.__data[offset:offset + PLAYER_RECORD_SIZE])
            players[player_id].set_emperor_name(lbx.read_string(self.__data, offset, 15))
            players[player_id].set_race_name(lbx.read_string(self.__data, offset + 0x14, 36))
            players[player_id].set_picture(lbx.read_byte(self.__data, offset + 0x24))
            players[player_id].set_color(lbx.read_byte(self.__data, offset + 0x25))
            players[player_id].set_personality(ord(self.__data[offset + 0x26]))
            players[player_id].set_objective(ord(self.__data[offset + 0x27]))
            players[player_id].set_tax_rate(ord(self.__data[offset + 0x30]))
            players[player_id].set_bc(compose_int(ord(self.__data[offset + 0x31]), ord(self.__data[offset + 0x32]), ord(self.__data[offset + 0x33]), ord(self.__data[offset + 0x34])))
            players[player_id].set_total_frighters(compose_int(ord(self.__data[offset + 0x35]), ord(self.__data[offset + 0x36])))
            players[player_id].set_used_frighters(compose_int(ord(self.__data[offset + 0x37]), ord(self.__data[offset + 0x38])))
            players[player_id].set_command_points(compose_int(ord(self.__data[offset + 0x39]), ord(self.__data[offset + 0x3A])))
            players[player_id].set_industry(compose_int(ord(self.__data[offset + 0xA9]), ord(self.__data[offset + 0xAA])))
            players[player_id].set_research(compose_int(ord(self.__data[offset + 0xAB]), ord(self.__data[offset + 0xAC])))
            players[player_id].set_food(compose_int(ord(self.__data[offset + 0x0AF]), ord(self.__data[offset + 0x0B0])))
#            players[player_id].set_bc_income(compose_int(ord(self.__data[offset + 0x0B1]), ord(self.__data[offset + 0x0B2])))
            players[player_id].set_bc_income(lbx.read_signed_short_int(self.__data, offset + 0xB1))
            players[player_id].set_research_progress(compose_int(ord(self.__data[offset + 0x1EA]), ord(self.__data[offset + 0x1EB])))
            players[player_id].set_research_area(ord(self.__data[offset + 0x320]))
            players[player_id].set_research_item(ord(self.__data[offset + 0x321]))
            players[player_id].set_research_costs(0)
            players[player_id].set_racepicks({
                                        'goverment':		ord(self.__data[offset + 0x89E]),
                                        'population':		lbx.read_signed_byte(self.__data, offset + 0x89F),
                                        'farming':		lbx.read_signed_byte(self.__data, offset + 0x8A0),
                                        'industry':		lbx.read_signed_byte(self.__data, offset + 0x8A1),
                                        'science':		lbx.read_signed_byte(self.__data, offset + 0x8A2),
                                        'money':		lbx.read_signed_byte(self.__data, offset + 0x8A3),
                                        'ship_defense':		lbx.read_signed_byte(self.__data, offset + 0x8A4),
                                        'ship_attack':		lbx.read_signed_byte(self.__data, offset + 0x8A5),
                                        'ground_combat':	lbx.read_signed_byte(self.__data, offset + 0x8A6),
                                        'spying':		lbx.read_signed_byte(self.__data, offset + 0x8A7),
                                        'low_g':		ord(self.__data[offset + 0x8A8]),
                                        'high_g':		ord(self.__data[offset + 0x8A9]),
                                        'aquatic':		ord(self.__data[offset + 0x8AA]),
                                        'subterranean':		ord(self.__data[offset + 0x8AB]),
                                        'large_home_world':	ord(self.__data[offset + 0x8AC]),
                                        'rich_home_world':	ord(self.__data[offset + 0x8AD]),
                                        # where is poor_home_worlds?
                                        'artifacts_home_world':	ord(self.__data[offset + 0x8AE]),
                                        'cybernetic':		ord(self.__data[offset + 0x8AF]),
                                        'lithovore':		ord(self.__data[offset + 0x8B0]),
                                        'repulsive':		ord(self.__data[offset + 0x8B1]),
                                        'charismatic':		ord(self.__data[offset + 0x8B2]),
                                        'uncreative':		ord(self.__data[offset + 0x8B3]),
                                        'creative':		ord(self.__data[offset + 0x8B4]),
                                        'tolerant':		ord(self.__data[offset + 0x8B5]),
                                        'fantastic_traders':	ord(self.__data[offset + 0x8B6]),
                                        'telepathic':		ord(self.__data[offset + 0x8B7]),
                                        'lucky':		ord(self.__data[offset + 0x8B8]),
                                        'omniscience':		ord(self.__data[offset + 0x8B9]),
                                        'stealthy_ships':	ord(self.__data[offset + 0x8BA]),
                                        'trans_dimensional':	ord(self.__data[offset + 0x8BB]),
                                        'warlord':		ord(self.__data[offset + 0x8BC]),
                                    })
            players[player_id].set_known_techs(self.parse_known_techs(offset + 0x117))
            players[player_id].set_prototypes([])
            players[player_id].set_tributes([])
            for ii in range(6):
                offset2 = offset + 0x325 + (ii * 0x63)
                players[player_id].add_prototype(self.parse_ship_design(offset2))

            for ii in range(7):
                offset2 = offset + 0x649 + (ii)
                players[player_id].add_tribute(ord(self.__data[offset2]))
#            players[player_id].set_()
            players[8] = universe.Player(8)
            players[8].set_race_name("Antareans")
            players[8].set_emperor_name("Antarean")

            players[9] = universe.Player(8)
            players[9].set_race_name("Orion")
            players[9].set_emperor_name("Loknar")

            players[10] = universe.Player(10)
            players[10].set_race_name("Space Amoeba")
            players[10].set_emperor_name("Amoeba")

            players[11] = universe.Player(11)
            players[11].set_race_name("Space Crystal")
            players[11].set_emperor_name("Crystal")

            players[12] = universe.Player(12)
            players[12].set_race_name("Space Dragon")
            players[12].set_emperor_name("Dragon")

            players[13] = universe.Player(13)
            players[13].set_race_name("Space Eeel")
            players[13].set_emperor_name("Eel")

            players[14] = universe.Player(14)
            players[14].set_race_name("Space Hydra")
            players[14].set_emperor_name("Hydra")

            for player_id in range(8, 15):
                players[player_id].set_bc(0)
                players[player_id].set_bc_income(0)
                players[player_id].set_research_area(0)
                players[player_id].set_research_item(0)
                players[player_id].set_food(0)
                players[player_id].set_research_costs(0)
                players[player_id].set_research_progress(0)
        return players
        """
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
        """
    #end func parse_players

    def parse_stars(self):
        #       http://www.spheriumnorth.com/orion-forum/nfphpbb/viewtopic.php?p=149
        SOLAR_SYSTEMS_COUNT_OFFSET	= 0x17ad1
        SOLAR_SYSTEMS_DATA_OFFSET	= 0x17ad3
        SOLAR_SYSTEM_RECORD_SIZE	= 0x71

        stars = {}
        c = ord(self.__data[SOLAR_SYSTEMS_COUNT_OFFSET])
        for star_id in range(c):
            offset = SOLAR_SYSTEMS_DATA_OFFSET + (SOLAR_SYSTEM_RECORD_SIZE * star_id)

            stars[star_id] = universe.Star(star_id)
            stars[star_id].import_from_moo2(self.__data[offset:offset + SOLAR_SYSTEM_RECORD_SIZE])
        return stars

    def __old__parse_stars(self):

        for i in range(c):
            offset = SOLAR_SYSTEMS_DATA_OFFSET + (SOLAR_SYSTEM_RECORD_SIZE * i)
            systems = {}
#            print "system @ %x" % offset
            star_id = i
#            systems.append({
            systems[star_id] = {
                'id':			i,
                'name':     		lbx.read_string(self.__data, offset, 15),
                'x':        		lbx.read_short_int(self.__data, offset + 0x0f),
                'y':        		lbx.read_short_int(self.__data, offset + 0x11),
                'size':     		lbx.read_byte(self.__data, offset + 0x13),
                'owner':			lbx.read_byte(self.__data, offset + 0x14),		# primary owner
                'pict_type':		lbx.read_byte(self.__data, offset + 0x15),
                'class':    		lbx.read_byte(self.__data, offset + 0x16),
                'last_planet_selected':	[
                                                lbx.read_byte(self.__data, offset + 0x17),
                                                lbx.read_byte(self.__data, offset + 0x18),
                                                lbx.read_byte(self.__data, offset + 0x19),
                                                lbx.read_byte(self.__data, offset + 0x1A),
                                                lbx.read_byte(self.__data, offset + 0x1B),
                                                lbx.read_byte(self.__data, offset + 0x1C),
                                                lbx.read_byte(self.__data, offset + 0x1D),
                                                lbx.read_byte(self.__data, offset + 0x1E)
                                            ],
                'black_hole_blocks':	[
                                            ],
                '0x1f':		ord(self.__data[offset + 0x1f]),
                '0x20':		ord(self.__data[offset + 0x20]),
                '0x21':		ord(self.__data[offset + 0x21]),
                '0x22':		ord(self.__data[offset + 0x22]),
                '0x23':		ord(self.__data[offset + 0x23]),
                '0x24':		ord(self.__data[offset + 0x24]),
                '0x25':		ord(self.__data[offset + 0x25]),
                '0x26':		ord(self.__data[offset + 0x26]),
                '0x27':		ord(self.__data[offset + 0x27]),
                'special':  	ord(self.__data[offset + 0x28]),
                'wormhole': 	ord(self.__data[offset + 0x29]),
                '0x2a':		ord(self.__data[offset + 0x2a]),	# blockaded? ( 0 | 1 )
                '0x2b':		ord(self.__data[offset + 0x2b]),
                '0x2c':		ord(self.__data[offset + 0x2c]),
                '0x2d':		ord(self.__data[offset + 0x2d]),
                '0x2e':		ord(self.__data[offset + 0x2e]),
                '0x2f':		ord(self.__data[offset + 0x2f]),
                '0x30':		ord(self.__data[offset + 0x30]),
                '0x31':		ord(self.__data[offset + 0x31]),
                '0x32':		ord(self.__data[offset + 0x32]),
                'visited':		ord(self.__data[offset + 0x33]),	# bitmask as boleans for each player
                '0x34':		ord(self.__data[offset + 0x34]),
                '0x35':		ord(self.__data[offset + 0x35]),
                '0x36':		ord(self.__data[offset + 0x36]),
                '0x37':		ord(self.__data[offset + 0x37]),
                '0x38':		ord(self.__data[offset + 0x38]),
                'indictor': 	ord(self.__data[offset + 0x39]),	# 0 = none, 1-8 = owner player 0-7  ( http://code.google.com/p/moo2x/wiki/star )
                '0x3a':		ord(self.__data[offset + 0x3a]),
                '0x3b':		ord(self.__data[offset + 0x3b]),
                '0x3c':		ord(self.__data[offset + 0x3c]),
                '0x3d':		ord(self.__data[offset + 0x3d]),
                '0x3e':		ord(self.__data[offset + 0x3e]),
                'artemis':  	ord(self.__data[offset + 0x3f]),	# 0 = none, 1-8=owner player 0-7 ( http://code.google.com/p/moo2x/wiki/star )
                '0x40':		ord(self.__data[offset + 0x40]),	# Star has dimensional portal ?
                '0x41':		ord(self.__data[offset + 0x41]),
                '0x42':		ord(self.__data[offset + 0x42]),
                '0x43':		ord(self.__data[offset + 0x43]),
                '0x44':		ord(self.__data[offset + 0x44]),
                '0x45':		ord(self.__data[offset + 0x45]),
                '0x46':		ord(self.__data[offset + 0x46]),
                '0x47':		ord(self.__data[offset + 0x47]),
                '0x48':		ord(self.__data[offset + 0x48]),
                '0x49':		ord(self.__data[offset + 0x49]),
                'objects':   	[
                                        compose_int(ord(self.__data[offset + 0x4a]), ord(self.__data[offset + 0x4b])),
                                        compose_int(ord(self.__data[offset + 0x4c]), ord(self.__data[offset + 0x4d])),
                                        compose_int(ord(self.__data[offset + 0x4e]), ord(self.__data[offset + 0x4f])),
                                        compose_int(ord(self.__data[offset + 0x50]), ord(self.__data[offset + 0x51])),
                                        compose_int(ord(self.__data[offset + 0x52]), ord(self.__data[offset + 0x53]))
                                    ],
    #		??? Relocation star id (0-7 player #, not sure about size of array. )
                '0x54':		ord(self.__data[offset + 0x54]),
                '0x55':		ord(self.__data[offset + 0x55]),
                '0x56':		ord(self.__data[offset + 0x56]),
                '0x57':		ord(self.__data[offset + 0x57]),
                '0x58':		ord(self.__data[offset + 0x58]),
                '0x59':		ord(self.__data[offset + 0x59]),
                '0x5a':		ord(self.__data[offset + 0x5a]),
                '0x5b':		ord(self.__data[offset + 0x5b]),
                '0x5c':		ord(self.__data[offset + 0x5c]),
                '0x5d':		ord(self.__data[offset + 0x5d]),
                '0x5e':		ord(self.__data[offset + 0x5e]),
                '0x5f':		ord(self.__data[offset + 0x5f]),
                '0x60':		ord(self.__data[offset + 0x60]),
                '0x61':		ord(self.__data[offset + 0x61]),
                '0x62':		ord(self.__data[offset + 0x62]),
                '0x63':		ord(self.__data[offset + 0x63]),
    #		unknown:
                '0x64':		ord(self.__data[offset + 0x64]),
                '0x65':		ord(self.__data[offset + 0x65]),
                '0x66':		ord(self.__data[offset + 0x66]),
                '0x67':		ord(self.__data[offset + 0x67]),
                '0x68':		ord(self.__data[offset + 0x68]),
                '0x69':		ord(self.__data[offset + 0x69]),
                '0x6a':		ord(self.__data[offset + 0x6a]),
                '0x6b':		ord(self.__data[offset + 0x6b]),
                '0x6c':		ord(self.__data[offset + 0x6c]),
                '0x6d':		ord(self.__data[offset + 0x6d]),
                '0x6e':		ord(self.__data[offset + 0x6e]),
                '0x6f':		ord(self.__data[offset + 0x6f]),
                '0x70':		ord(self.__data[offset + 0x70])
                }
#        i += 1
#        offset = 0x17ad3 + (SOLAR_SYSTEM_RECORD_SIZE * i)
#        print "STOP system @ %x" % offset
    #    blah
        return systems
    # end func parse_stars

    def parse_planets(self, stars):
        PLANETS_COUNT_OFFSET	= 0x162e7
        PLANETS_DATA_OFFSET		= 0x162e9
        PLANET_RECORD_SIZE		= 0x11
        planets = {}
#        pl = {}

        c = 0
        for star_id in stars:
            star = stars[star_id]
            for o in star.get_objects():
                if o != 0xffff:
                    c += 1

        c = compose_int(ord(self.__data[PLANETS_COUNT_OFFSET]), ord(self.__data[PLANETS_COUNT_OFFSET + 1]))
#        c = 250

#        print "Reading planetary objects ..."
#        print "    count: %i" % c

        for i in range(c):
            planet_id = i
            offset = PLANETS_DATA_OFFSET + (PLANET_RECORD_SIZE * i)
    #        system_number = ord(self.__data[offset + 0x02])
    #        position = ord(self.__data[offset + 0x03])
#            planets.append({
            planets[planet_id] = universe.Planet(planet_id)
            planets[planet_id].import_from_moo2(self.__data[offset:offset + PLANET_RECORD_SIZE])
#            pl[planet_id] = {
#                'planet_id':        planet_id,
#                'colony':           lbx.read_short_int(self.__data, offset),	# 0xffff = no colony here
#                'parent_star':      lbx.read_byte(self.__data, offset + 0x02),
#                'position':         lbx.read_byte(self.__data, offset + 0x03),
#                'type':             lbx.read_byte(self.__data, offset + 0x04),
#                'size':             lbx.read_byte(self.__data, offset + 0x05),
#                'gravity':          lbx.read_byte(self.__data, offset + 0x06),
#                'group':            lbx.read_byte(self.__data, offset + 0x07),   # not used
#                'terrain':          lbx.read_byte(self.__data, offset + 0x08),
#                'picture':          lbx.read_byte(self.__data, offset + 0x09),   # Background image on colony screen (0-5=image in planets.lbx)
#                'minerals':         lbx.read_byte(self.__data, offset + 0x0a),
#                'foodbase':         lbx.read_byte(self.__data, offset + 0x0b),
#                'terraformations':  lbx.read_byte(self.__data, offset + 0x0c),
#                'max_farms':        lbx.read_byte(self.__data, offset + 0x0d),   # unknown (Initial value is based on Planet Size but changes if colonized), 2=tiny, 4=small, 5=med, 7=large, A=huge
#                'max_population':   lbx.read_byte(self.__data, offset + 0x0e),
#                'special':          lbx.read_byte(self.__data, offset + 0x0f),
#                'flags':            lbx.read_byte(self.__data, offset + 0x10)    # (bit 2 = Soil Enrichment)
#            }
        return planets
    # end func parse_planets

    def parse_colonies(self):
        COLONIES_DATA_OFFSET	= 0x0025d
        COLONY_RECORD_SIZE		= 361
        c = compose_int(ord(self.__data[0x0000025b]), ord(self.__data[0x0000025c]))

#        print "Number of colonies to read: %i" % c

        colonies = {}

        for colony_id in range(c):
#            print("Moo2Savegame::parse_colonies() ... colony_id = %i" % colony_id)
            offset	= COLONIES_DATA_OFFSET + (COLONY_RECORD_SIZE * colony_id)
            colonies[colony_id] = universe.Colony(colony_id)
            colonies[colony_id].import_from_moo2(self.__data[offset:offset + COLONY_RECORD_SIZE])
#            print
        return colonies
    # end func parse_colonies

    def parse_ship_design(self, offset):
        MAX_WEAPONS = 8
        weapons = []
        for i in range(MAX_WEAPONS):
            offset2 = offset + 0x1C + (8 * i)
            weapon = lbx.read_byte(self.__data, offset2)
            if (weapon > 0):
                weapons.append({
                    'weapon':		weapon,
                    'count':		lbx.read_byte(self.__data, offset2 + 0x02),
                    'current_count':	lbx.read_byte(self.__data, offset2 + 0x03),
                    'arc':		lbx.read_byte(self.__data, offset2 + 0x04),
                    'beam_mods':	lbx.read_byte(self.__data, offset2 + 0x05),
                    'missile_mods':	lbx.read_byte(self.__data, offset2 + 0x06),
                    'ammo':		lbx.read_byte(self.__data, offset2 + 0x07)
                })
        return {
                'name':                 lbx.read_string(self.__data, offset, 16),
                'size':         	lbx.read_byte(self.__data, offset + 0x10),
                'type':                 lbx.read_byte(self.__data, offset + 0x11),      # 0 = combat ship, 1 = colony ship, 2 = transport ship, 3 = guardian, 4 = outpost ship
                'shield':		lbx.read_byte(self.__data, offset + 0x12),
                'drive':		lbx.read_byte(self.__data, offset + 0x13),
                'speed':		lbx.read_byte(self.__data, offset + 0x14),
                'computer':		lbx.read_byte(self.__data, offset + 0x15),
                'armor':		lbx.read_byte(self.__data, offset + 0x16),
#                'special_devices':	self.__data[offset + 0x17:offset + 0x1C],	# char  special_device_flags[(MAX_SPECIALS+7)/8];
                'special_devices':	bitarray(bytearray(self.__data[offset + 0x17:offset + 0x1C])),	# char  special_device_flags[(MAX_SPECIALS+7)/8];
                'weapons':		weapons,
                'picture':		lbx.read_byte(self.__data, offset + 0x5C),
                'builder':		lbx.read_byte(self.__data, offset + 0x5D),		# or previous owner?
                'cost':                 lbx.read_short_int(self.__data, offset + 0x5E),
                'combat_speed':         lbx.read_byte(self.__data, offset + 0x60),
                'build_date':           lbx.read_short_int(self.__data, offset + 0x61)
        }
    # end func parse_ship_design

    def parse_one_ship(self, ship_id):
        SAVE_SHIPS_OFFSET         = 0x21f58
        SAVE_SHIP_RECORD_SIZE     = 0x81        # = 129
        offset          = SAVE_SHIPS_OFFSET + (SAVE_SHIP_RECORD_SIZE * ship_id)
        data = self.__data[offset:offset + SAVE_SHIP_RECORD_SIZE]

        ship = universe.Starship(ship_id)

        ship_design = self.parse_ship_design(offset)
        ship.set_name(ship_design['name'])
        ship.set_design(ship_design)
        ship.set_owner(lbx.read_byte(data, 0x63))
        ship.set_status(lbx.read_byte(data, 0x64))                               # 0 = orbitting, 2 = traveling, 5 = destroyed?
        ship.set_destination(lbx.read_short_int(data, 0x65) % 500)                             # destination star
        ship.set_x(lbx.read_short_int(data, 0x67))
        ship.set_y(lbx.read_short_int(data, 0x69))
        ship.set_group_has_navigator(lbx.read_byte(data, 0x6B))
        ship.set_travelling_speed(lbx.read_byte(data, 0x6C))     # possibly less than ftl_type
        ship.set_turns_left(lbx.read_byte(data, 0x6D))           # until arrival
        ship.set_shield_damage_percent(lbx.read_byte(data, 0x6E))
        ship.set_drive_damage_percent(lbx.read_byte(data, 0x6F))
        ship.set_computer_damage(lbx.read_byte(data, 0x70))
        ship.set_crew_quality(lbx.read_byte(data, 0x71))
        ship.set_crew_experience(lbx.read_short_int(data, 0x72))
        ship.set_officer_id(lbx.read_short_int(data, 0x74))
        ship.set_special_device_damage(data[0x76:0x7B]) # bit flag array
        ship.set_armor_damage(lbx.read_short_int(data, 0x7B))
        ship.set_structural_damage(lbx.read_short_int(data, 0x7D))
        ship.set_mission(lbx.read_byte(data, 0x7F))              # used for AI
        ship.set_just_built(lbx.read_byte(data, 0x80))

        return ship

    def parse_ships(self):
        SAVE_SHIP_COUNT_OFFSET    = 0x21f56

        c = compose_int(ord(self.__data[SAVE_SHIP_COUNT_OFFSET]), ord(self.__data[SAVE_SHIP_COUNT_OFFSET + 1]))
        ships = {}
        for ship_id in range(c):
            ships[ship_id] = self.parse_one_ship(ship_id)
        return ships
    # end func parse_ships

    def set_rules(self, rules):
        self.__rules = rules
    # end func set_rules

    def init_stars(self):
        self.__stars_by_coords = {}

        for star_id in self.__stars:
            star = self.__stars[star_id]
            k = "%i:%i" % (star['x'], star['y'])
            self.__stars_by_coords[k] = star
            num = 0
            for object in star['objects']:
#               print "object: %i" % object
                if object != 0xffff:
                    num += 1
                    self.__planets[object]['num'] = num
    # end func init_stars

    def init_heroes(self):
        self.__players_heroes = {}
        for hero in self.__heroes:
            if hero['player'] != 0xFF:
                if not self.__players_heroes.has_key(hero['player']):
                    self.__players_heroes[hero['player']] = {}
                self.__players_heroes[hero['player']][hero['id']] = hero
#        print self.__players_heroes
    # end func init_heroes
