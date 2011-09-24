import math

import moo2
import universe
import rules

import dictionary


def stardate(i):
    s = str(i)
    return s[:-1] + "." + s[-1]
# /stardate


PARSEC_LENGTH = 30


class Game(object):

    def __init__(self, rules, game_file = None):
        self.set_recount_flag(False)
        self.set_rules(rules)
        if game_file:
            self.load_moo2_savegame(game_file)
    # /__init__

    def set_recount_flag(self, value):
        self.__recount = value

    def set_rules(self, rules):
        self.__rules = rules
    # /set_rules

    def init_stars(self):
        self.__stars_by_coords = {}

        for star_id in self.__stars:
            star = self.__stars[star_id]
            k = "%i:%i" % (star.get_x(), star.get_y())
            self.__stars_by_coords[k] = star
            num = 0
            for object in star.get_objects():
#               print "object: %i" % object
                if object != 0xffff:
                    num += 1
                    self.__planets[object].set_position(num)
    # /init_stars
        
    def init_colonies(self):
        for colony_id in self.__colonies:
            colony	= self.__colonies[colony_id]
            planet_id	= colony.get_planet_id()
            if colony.get_owner() < 0xff:
                planet      = self.__planets[planet_id]
                colony.assign_planet(self.__planets[planet_id])
                colony.set_name("%s %i" % (self.__stars[planet.get_star()].get_name(), planet.get_position()))
    # /init_colonies

    def init_heroes(self):
        self.__players_heroes = {}
        for hero_id in self.__heroes:
            hero = self.__heroes[hero_id]
            if hero['player'] != 0xFF:
                if not self.__players_heroes.has_key(hero['player']):
                    self.__players_heroes[hero['player']] = {}
                self.__players_heroes[hero['player']][hero['id']] = hero
#        print self.__players_heroes
    # /init_heroes

    def init_players(self):
        for player_id, player in self.__players.items():
            for star_id, star in self.__stars.items():
                if star.visited_by_player(player_id):
                    player.add_explored_star_id(star_id)

    def load_moo2_savegame(self, filename):
        """
        Loads the original MOO2 savegame
        """

        savegame = moo2.Moo2Savegame(filename)

#        filesize = os.path.getsize(filename)
#        savefile = open(filename, 'rb')
#        data = savefile.read(filesize)
#        savefile.close()

        self.__game     = savegame.parse_game()
        self.__galaxy   = savegame.parse_galaxy()

        self.__heroes   = savegame.parse_heroes()          # 100%
        self.__players  = savegame.parse_players()
        self.__stars    = savegame.parse_stars()
        self.__planets	= savegame.parse_planets(self.__stars)		# 100%
        self.__colonies	= savegame.parse_colonies()
        self.__ships	= savegame.parse_ships()		# 100%

        self.init_stars()
        self.init_colonies()
        self.init_heroes()
        self.init_players()

        self.recount()
    # /load_moo2_savegame
 

    def get_colony_leader(self, colony_id):
#        print self.__colonies[colony_id].is_outpost()
        colony_owner = self.__colonies[colony_id].get_owner()
#        print
#        print("colony_id ... %i" % colony_id)
#        print("colony_data ... %s" % self.__colonies[colony_id])
#        print(self.__colonies[colony_id].planet())
#        print
        parent_star = self.__colonies[colony_id].planet().get_star()
 #       print "Game::get_colony_leader() ... colony_id = %i, owner = %i, parent_star = %i" % (colony_id, colony_owner, parent_star)
        for hero_id in self.list_player_colony_leaders(colony_owner):
            if self.__heroes[hero_id]['location'] == parent_star:
                return self.__heroes[hero_id]
        return None
    # /get_colony_leader

    def list_area_tech_ids(self, research_area):
        techs = []
        for tech_id in self.__rules['tech_table']:
            if self.__rules['tech_table'][tech_id]['area'] == research_area:
                techs.append(tech_id)
        return sorted(techs)
    # /list_techs_by_area

    def colony_owned_by(self, colony_id, player_id):
        """ Returns true if the given colony_id belongs to an actual colony"""
        return self.__colonies.has_key(colony_id) and self.__colonies[colony_id].is_owned_by(player_id)

    def recount_heroes(self):
        for hero_id, hero in self.__heroes.iteritems():
            hero['level'] = 0
            for level in self.__rules['hero_levels']:
                if hero['experience'] >= level:
                    hero['level'] += 1
#            print self.__heroes[hero_id]

    def recount_colonies(self):
        for colony_id in self.__colonies:
            print("Game::recount_colonies() ... colony_id = %i" % colony_id)
            if self.__colonies[colony_id].exists():
#                print("Game::recount_colonies() ... self.__colonies[%i].owner() = %i" % (colony_id, self.__colonies[colony_id].owner()))
                colony_leader = self.get_colony_leader(colony_id)
#                print "Game::recount_colonies() ... colony_id %i, leader = %s" % (colony_id, str(colony_leader))
#                for hero_id in self.__heroes:
 #               print
                self.__colonies[colony_id].recount(self.__rules, colony_leader, self.__players)
    # /recount_colonies

    def list_player_colony_leaders(self, player_id):
        list = {}
        if not self.__players_heroes.has_key(player_id):
            return list
        for hero_id in self.__players_heroes[player_id]:
            hero = self.__heroes[hero_id]
#            print hero
            if hero['type'] == 1:
                list[hero_id] = hero
        return list
    # /list_player_colony_leaders

    def list_player_officers(self, player_id):
        list = {}
        if not self.__players_heroes.has_key(player_id):
            return list
        for hero_id in self.__players_heroes[player_id]:
            hero = self.__heroes[hero_id]
#            print hero
            if hero['type'] == 0:
                list[hero_id] = hero
        return list
    # /list_player_colony_leaders

    def update_research(self, player_id, research_item):
        print("Game::update_research() ... player_id = %i, research_item = %i" % (player_id, research_item))
        player = self.__players[player_id]
        player.set_research_item(research_item)
        player.set_research_area(self.__rules['tech_table'][research_item]['area'])
        player.set_research_costs(rules.research_costs(self.__rules['research_areas'], player.get_research_area(), player.get_research()))
        player.set_research_turns_left(rules.research_turns(player.get_research_costs(), player.get_research_progress(), player.get_research()))
        return True
    # /update_research

    def set_colony_build_queue(self, player_id, colony_id, build_queue):
        """ Sets a new build queue for a given colony_id owned by player_id

        """
        print("@ Game::set_colony_build_queue()")
        print("    colony_id: %i" % colony_id)
        print("    build_queue: %s" % str(build_queue))
        if self.colony_owned_by(colony_id, player_id):
            # TODO: validate the build queue:
            #           all items must be available based on known technologies?
            #           buildings can't be already present - remove duplicates or just fail?
            #           check terraforming
            #           check gravity generator
            #           check artifical planet
            #           check star system unique items (star gate, artemis ...)
            #           what else?
            #           IF ANY ERROR OCCURS DURING ABOVE CHECKS, METHOD SHOULD NOT SET THE NEW QUEUE BUT RETURN FALSE TO PREVENT CONFUSION
            self.__colonies[colony_id].set_build_queue(build_queue)
            return True

        return False

    def recount_players(self):
        for player_id in self.__players:
            self.__players[player_id].set_research(0)
            self.__players[player_id].set_food(0)

        for colony_id in self.__colonies:
            if self.__colonies[colony_id].exists():
                owner = self.__colonies[colony_id].get_owner()
                self.__players[owner].add_research(self.__colonies[colony_id].get_research())
                self.__players[owner].add_food(self.__colonies[colony_id].get_food() - self.__colonies[colony_id].total_population())

        # hardcoded 8 players
        for player_id in range(8):
            player = self.__players[player_id]

            if player.alive():
                self.update_research(player_id, player.get_research_item())
#                player.print_debug()

            # refresh player's research_areas:
            research_areas = {}
            for res_id in self.__rules['research']:
#                print "                         AREA: %s" % res_id
                area_id = self.__rules['research'][res_id]['start_area']
#                print "                         start_area = %i" % area_id
                while 1:
#                    print "      checking area_id = %i" % area_id

                    if not self.__rules['research_areas'][area_id]['next']:
                        break

                    area_techs = self.list_area_tech_ids(area_id)
#                    print "          area_techs = %s" % str(area_techs)
                    new_area_id = 0
                    for tech_id in area_techs:
                        if player.knows_technology(tech_id):
#                            print "known tech! ... %i .. moving to next area" % tech_id
                            new_area_id = self.__rules['research_areas'][area_id]['next']
                            break
                            
                    if new_area_id:
                        area_id = new_area_id
#                        player['research_levels'][res_id] = area_id
                    else:
                        break

                research_areas[res_id] = self.list_area_tech_ids(area_id)
            player.update_research_areas(research_areas)
#            print "                    research_areas = %s" % str(player['research_areas'])

#            for tech_id in player['known_techs']:
#                tech = self.__rules['tech_table'][tech_id]
#                print "                         known = %s (area: %i)" % (tech['name'], tech['area'])
            # / refresh player's research_areas
    # /recount_players

    def recount(self):
        print "=== Recount Heroes ==="
        self.recount_heroes()

        print "=== Recount Colonies ==="
        self.recount_colonies()

        print "=== Recount Players ==="
        self.recount_players()
    # /recount


    def raise_population(self):
        for colony_id in self.__colonies:
            self.__colonies[colony_id].raise_population()
    # /raise_population

    def get_stars_for_player(self, player_id):
        """ Returns a dictionary of all stars in galaxy.
        Stars that player doesn't know yet are listed as an UnexploredStar class

        """
        stars = {}
        for star_id, star in self.__stars.items():
            if self.__players[player_id].knows_star_id(star_id):
                stars[star_id] = star
            else:
                stars[star_id] = universe.UnexploredStar(star_id, star.get_x(), star.get_y(), star.get_size(), star.get_pict_type(), star.get_class())
        return stars

    def get_colonies_for_player(self, player_id):
        colonies = {}
        for colony_id in self.__colonies:
            col = self.__colonies[colony_id]
            if col.get_owner() == player_id:
                colonies[colony_id] = col
            else:
                colonies[colony_id] = universe.EnemyColony(colony_id, col.get_owner())
        return colonies

    def get_data_for_player(self, player_id):
        """
        this method returns data for one particular player and leave data for other players
        security reasons to prevent hacked clients to display data that player should not know
        """

         # TODO: implement status checking, to prevent asynchronous requests problems (client receives bad data)

#        player_number = player_id + 1

        colony_leaders = self.list_player_colony_leaders(player_id)
#        print "=== Colony Leaders: ==="
#        print colony_leaders
#        print "=== /Colony Leaders: ==="

        officers = self.list_player_officers(player_id)
#        print "=== Officers: ==="
#        print officers
#        print "=== Officers: ==="


        return {
            'rules':            self.__rules,
            'me':               self.__players[player_id],

            'galaxy':           self.__galaxy,
            'players':          self.__players,                             # insecure
            'stars':            self.get_stars_for_player(player_id),       # 100% secure?
            'stars_by_coords':  self.__stars_by_coords,                     # insecure

            'colony_leaders':   colony_leaders,                             # 50% secure?
            'officers':         officers,                                   # 50% secure?

            'planets':          self.__planets,                             # insecure
            'colonies':         self.get_colonies_for_player(player_id),      # 100% secured ?
            'ships':            self.__ships,                               # insecure
            'prototypes':       self.__players[player_id].get_prototypes(),    # 100% secured?
        }
    # /get_data_for_player

    def __move_ships(self):
        """ Count new position af all moving or launching ships

            TODO: new start system exploration
            TODO: slowdown in nebulae
            TODO: usage of wormholes, jump gate and star gate

        """
        print("=== Move ships ===")
        for ship_id, ship in self.__ships.items():
            # if ship exists and is launching or already travelling
            if ship.exists() and ship.get_status() in (1, 2):
                ship_x, ship_y = ship.get_coords()
                ship_speed = ship.get_travelling_speed()
                dest = ship.get_destination()
                dest_x, dest_y = self.__stars[dest].get_coords()

                xx = dest_x - ship_x
                yy = dest_y - ship_y

                distance = math.sqrt(xx**2 + yy**2)

                parsecs = float(distance) / float(PARSEC_LENGTH)

                if parsecs > ship_speed:
                    # move towards ship's destination at known speed
                    parsec_x = float(xx) / parsecs
                    parsec_y = float(yy) / parsecs
                    ship_xx = int(ship_x + math.ceil(float(ship_speed) * parsec_x))
                    ship_yy = int(ship_y + math.ceil(float(ship_speed) * parsec_y))
                    ship.set_coords(ship_xx, ship_yy)
                    ship.set_travelling()
                else:
                    # ship has reached its destination
                    ship.set_coords(dest_x, dest_y)
                    ship.set_orbiting()
                    if not self.__players[ship.get_owner()].knows_star_id(dest):
                        self.__players[ship.get_owner()].add_explored_star_id(dest)

    def __colonies_production(self):
        """ Simple colony production
            Every turn, the first item from build queue is pulled and produced

            TODO: implement colony and outpost ships production
            TODO: implement regular ships production
            TODO: implement housing
            TODO: implement trade goods
            TODO: implement terraforming
            TODO: implement spies production
            TODO: implement real production cost

        """
        print("@ game::__colonies_production()")
        for colony_id, colony in self.__colonies.items():
            colony.debug_production(self.__rules)
#            for build_item in self.get_build_queue()[:
            print(colony.list_buildings())
            build_item = colony.get_build_item()
            if build_item is not None:
                production_id = build_item['production_id']
                print build_item
                if not self.__rules['buildings'][production_id].has_key('type') or self.__rules['buildings'][production_id]['type'] == "building":
                    colony.add_building(production_id)
                    colony.remove_build_item(production_id)
                colony.debug_production(self.__rules)
                print(colony.list_buildings())

    def next_turn(self):
#        raise research_progress
#        raise population

        print
        print "##"
        print "#    NEW TURN!"
        print "##"
        print

        self.recount()

        self.__move_ships()

        self.__colonies_production()

        for player_id in self.__players:
            player = self.__players[player_id]
            if player.alive():

                # research:
                if player.get_research_costs() > 0:
                    player.raise_research()
                    if player.reseatch_completed():
                        print "research completed"
                        print player.get_known_techs()
                        print player.get_research_item()
                        player.add_known_technology(player.get_research_item())
#
                        research_area_id = player.get_research_area()
#
                        if research_area_id:
                            research_area = self.__rules['research_areas'][research_area_id]
                            if research_area['next']:
                                player.set_research_area(research_area['next'])

                        player.set_research_progress(-1)
                # /research

                # BC:
                self.__players[player_id].raise_bc()
                # /BC

        self.raise_population()

        self.recount()

        self.__galaxy['stardate'] += 1
    # /next_turn

    def count_players(self):
        c = 0
        for player_id in range(8):
            if self.__players[player_id].alive():
                c += 1
        return c
    # /count_players

    def show_stars(self):
        s = ['small', 'medium', 'large']
        c = ['blue', 'white', 'yellow', 'orange', 'red', 'gray', 'black hole']
        print
        print("+---------+-----------------+------------+------------+--------+-------+-------+-------+-------+-------+")
        print("| star_id | name            | coords     | class      | size   | obj 1 | obj 2 | obj 3 | obj 4 | obj 5 |")
        print("+---------+-----------------+------------+------------+--------+-------+-------+-------+-------+-------+")
        for star_id, star in self.__stars.items():
            objects = star.get_objects()
            print("| %7i | %15s | %4i, %4i | %10s | %6s | %5i | %5i | %5i | %5i | %5i |" % (star_id, star.get_name(), star.get_x(), star.get_y(), c[star.get_class()], s[star.get_size()], objects[0], objects[1], objects[2], objects[3], objects[4]))
        print("+---------+-----------------+------------+------------+--------+-------+-------+-------+-------+-------+")
    # /show_stars

    def show_planets(self):
        si = ['tiny', 'small', 'medium', 'large', 'huge']
        ty = ["???", "asteroid belt", "gas giant", "planet"]
        mi = ['ultra poor', 'poor', 'abundant', 'rich', 'ultra rich']
        te = ['toxic', 'radiated', 'baren', 'desert', 'tundra', 'ocean', 'swamp', 'arid', 'terran', 'gaia', '?? K ??', '?? L ??']
        print
        print("+-----------+-----------------+----------+--------+---------------+------------+----------+------+---------+")
        print("| planet_id | star            | position | size   | type          | minerals   | terrain  | food | max pop |")
        print("+-----------+-----------------+----------+--------+---------------+------------+----------+------+---------+")
        for planet_id, planet in self.__planets.items():
            print("| %9i | %15s | %8i | %6s | %13s | %10s | %8s | %4i | %7i |" % (planet_id, self.__stars[planet.get_star()].get_name(), planet.get_position(), si[planet.get_size()], ty[planet.get_type()], mi[planet.get_minerals()], te[planet.get_terrain()], planet.get_foodbase(), planet.get_max_population()))
        print("+-----------+-----------------+----------+--------+---------------+------------+----------+------+---------+")
        print
    # /show_planets

    def show_players(self):
        print("NUMBER OF PLAYERS: %i" % self.count_players())
        print("+-----------+----------------------+----------------------+--------+--------+--------+----------------------+----------------------+---------+-----------+")
        print("| player_id | name                 | emperor              | food   | BC     | income | research:area        | :item                | :costs  | :progress |")
        print("+-----------+----------------------+----------------------+--------+--------+--------+----------------------+----------------------+---------+-----------+")
        for player_id, player in self.__players.items():
            print("| %9i | %20s | %20s | %6i | %6i | %6i | %20s | %20s | %7i | %9i |" % (player_id, player.get_race_name(), player.get_emperor_name(), player.get_food(), player.get_bc(), player.get_bc_income(), str(player.get_research_area()), str(player.get_research_item()), player.get_research_costs(), player.get_research_progress()))
        print("+-----------+----------------------+----------------------+--------+--------+--------+----------------------+----------------------+---------+-----------+")
        print
    # /show_players

    def show_colonies(self):
        print
        print("+-----------+-----------+-----------------+------------+------+----------+----------+-------+")
        print("| colony_id | planet_id | owner           | population | food | research | industry | BC    |")
        print("+-----------+-----------+-----------------+------------+------+----------+----------+-------+")
        for colony_id, colony in self.__colonies.items():
            planet_id = colony.get_planet_id()
            owner_id = colony.get_owner()
            if (planet_id < 0xFF) and (owner_id < 0xFF):
                owner = self.__players[owner_id]
                print("| %9i | %9i | %15s | %10s | %4i | %8i | %8i | %5i |" % (colony_id, planet_id, owner.get_race_name(), colony.get_population(), colony.get_food(), colony.get_research(), colony.get_industry(), colony.bc()))
            else:
                print("| %9i | %9s | %15s | %10s | %4i | %8i | %8i | ----- |" % (colony_id, "0xFF", "0xFF", colony.get_population(), colony.get_food(), colony.get_research(), colony.get_industry()))
#	    colony = self.colonies
        print("+-----------+-----------+-----------------+------------+------+----------+----------+-------+")
        print
    # /show_colonies
        

    def show_ships(self):
        print("@ game::show_ships()")
        print
        print("+---------+------------------+-----------------+----------+------------+----------------------------+-------+-------+")
        print("| ship_id | name             | owner           | status   | coords     | destination                | speed | turns |")
        print("+---------+------------------+-----------------+----------+------------+----------------------------+-------+-------+")
        for ship_id, ship in self.__ships.items():
            if ship.exists():
                dest = ship.get_destination()
                dest_name = self.__stars[dest].get_name()
                dest_x, dest_y = self.__stars[dest].get_coords()

                print("| %7i | %16s | %15s | %8s | %4i, %4i | [%3i, %3i] %15s | %5i | %5i |" % (ship_id, ship.get_name(), self.__players[ship.get_owner()].get_race_name(), ship.get_status_text(), ship.get_x(), ship.get_y(), dest_x, dest_y, dest_name, ship.get_travelling_speed(), ship.get_turns_left()))
        print("+---------+------------------+-----------------+----------+------------+----------------------------+-------+-------+")
        print

        DICT = dictionary.get_dictionary()

        for ship_id, ship in self.__ships.items():
            design = ship.get_design()
            print("    === ship_id # %i ===" % ship_id)
#            print(design)
            for dev_id in design['special_devices']:
                print("        special device: %2i ... %s" % (dev_id, DICT['SHIP_SPECIALS'][dev_id]))
            print

#        i = 0
#        print("<?xml version=\"1.0\"?>")
#        for name in DICT['SHIP_SPECIALS']:
#            print("<device id=\"%i\">\n\t<name>%s</name>\n</device>\n" % (i, name))
#            i += 1