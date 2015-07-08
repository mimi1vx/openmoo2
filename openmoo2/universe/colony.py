import math

import lbx

from _buildings import *
from _game_constants import *

import rules
#import universe

from game_object import GameObject

class Colony(GameObject):

    def __init__(self, colony_id):
        self.__planet = None
        self.set_id(colony_id)

    def set_planet_id(self, planet_id):
        self.__planet_id = planet_id

    def get_planet_id(self):
        return self.__planet_id

    def print_info(self):
        print "	owner: %i" % self.get_owner()

    def import_from_moo2(self, data):

        def read_population(data, population):
            colonists = {0x02: [], 0x03: [], 0x82: []}
            for i in range(population):
                offset = 0x0C + (4 * i)
                t = (lbx.read_char(data, offset) & 0x80) + (lbx.read_char(data, offset + 1) & 3)
    		colonists[t].append({
                    'a':	lbx.read_char(data, offset),
                    'b':	lbx.read_char(data, offset + 1),
                    'c':	lbx.read_char(data, offset + 2),
                    'd':	lbx.read_char(data, offset + 3),
                    'r1':	(lbx.read_char(data, offset) & 0x70) >> 4,
                    'race':	(lbx.read_char(data, offset) & 0x07)
                })
            return colonists
        # end func read_population

#	print "Colony::load_from_moo2()"
#	print "	data length: %i" % len(data)
#	self.colony_id			= colony_id
        self.set_owner(lbx.read_char(data,  0x000))
#        print("     Colony::import_from_moo2() ... self.__owner = %i" % self.__owner)
        self.allocated_to	= lbx.read_char(data,  0x001)
        self.set_planet_id(lbx.read_char(data,  0x002))
#        print("     Colony::import_from_moo2() ... self.planet_id = %i" % self.planet_id)
        self.__officer		= lbx.read_short_int(data, 0x004),   # not used ?
        self.__is_outpost	= lbx.read_char(data,  0x006)
#        print("     Colony::import_from_moo2() ... self.__is_outpost = %i" % self.__is_outpost)
        self.__morale		= lbx.read_char(data,  0x007) * 5 # Morale value is stored as divided by 5
        self.__pollution	= lbx.read_short_int(data, 0x008)
        self.set_population(lbx.read_char(data,  0x00a))
        print("     Colony::import_from_moo2() ... self.__population = %i" % self.get_population())
        self.assignment		= lbx.read_char(data,  0x00b)
#			0x00 = Agricultural Colony
#			0x01 = Industrial Colony
#			0x02 = Research Colony
#			0xff = (balanced?) Colony
#		0x00c ~ 0x0b3		colonists
        self.colonists		= read_population(data, self.get_population())
        self.__pop_raised		= [
                                    lbx.read_short_int(data, 0x0B4),	# race 0
                                    lbx.read_short_int(data, 0x0B6),	# race 1
                                    lbx.read_short_int(data, 0x0B8),	# race 2
                                    lbx.read_short_int(data, 0x0BA),	# race 3
                                    lbx.read_short_int(data, 0x0BC),	# race 4
                                    lbx.read_short_int(data, 0x0BE),	# race 5
                                    lbx.read_short_int(data, 0x0C0),	# race 6
                                    lbx.read_short_int(data, 0x0C2),	# race 7
                                    lbx.read_short_int(data, 0x0C4),	# androids
                                    lbx.read_short_int(data, 0x0C6)	# natives
                                ]
        self.__pop_grow		= [
                                    lbx.read_short_int(data, 0x0C8),	# race 0
                                    lbx.read_short_int(data, 0x0CA),	# race 1
                                    lbx.read_short_int(data, 0x0CC),	# race 2
                                    lbx.read_short_int(data, 0x0CE),	# race 3
                                    lbx.read_short_int(data, 0x0D0),	# race 4
                                    lbx.read_short_int(data, 0x0D2),	# race 5
                                    lbx.read_short_int(data, 0x0D4),	# race 6
                                    lbx.read_short_int(data, 0x0D6),	# race 7
                                    lbx.read_short_int(data, 0x0D8),	# androids
                                    lbx.read_short_int(data, 0x0DA)	# natives
                                ]
        self.n_turns_existed		= ord(data[0x0DC])	# bookeeping
        self.food2_per_farmer		= ord(data[0x0DD])	# Food per farmer in half-units of food
        self.industry_per_worker	= ord(data[0x0DE])
        self.research_per_scientist	= ord(data[0x0DF])
        self.max_farms			= ord(data[0x0E0])
        self.__max_population		= ord(data[0x0E1])
        self.climate			= ord(data[0x0E2])
        self.ground_strength		= lbx.read_short_int(data, 0x0E3)	# calculated for ai
        self.space_strength		= lbx.read_short_int(data, 0x0E5)	# calculated for ai
        self.set_food(lbx.read_short_int(data, 0x0E7))	# total food = food - population
        self.set_industry(lbx.read_short_int(data, 0x0E9))
        self.set_research(lbx.read_short_int(data, 0x0EB))
#		0x0ed		?

        self.__build_queue = []
        for i in range(0, 14, 2):
            production_id = ord(data[0x115 + i])
            if production_id < 0xFF:
                self.__build_queue.append({'production_id': production_id, 'flags': ord(data[0x115 + i + 1])})
        
#		0x115		building item #0				# 0x0b = colony base??? 0xf9 = spy? 0xfd = housing 0xfe = trade goods
#			0x0b = colony base
#			0xf9 = spy
#			0xfd = housing
#			0xfe = trade goods
#			0xff = nothing
#		0x116		?
#		0x117		building item #1				# 0x0b = colony base??? 0xf9 = spy?
#		0x118		?
#		0x119		building item #2				# 0x0b = colony base??? 0xf9 = spy?
#		0x11a		?
#		0x11b		building item #3				# 0x0b = colony base??? 0xf9 = spy?
#		0x11c		?
#		0x11d		building item #4				# 0x0b = colony base??? 0xf9 = spy?
#		0x11e		?
#		0x11f		building item #5				# 0x0b = colony base??? 0xf9 = spy?
#		0x120		?
#		0x121		building item #6				# 0x0b = colony base??? 0xf9 = spy?
#		0x122		?
        self.marines			= lbx.read_char(data, 0x130)
        self.armors			= lbx.read_char(data, 0x132)
        self.__buildings			= []
        for b_id in range(1, 49):
    	    offset = 0x136 + b_id
#            self.buildings.append(ord(data[offset]))
            if ord(data[offset]):
                self.__buildings.append(b_id)

#	self.print_info()

    def set_population(self, population):
        self.__population = population

    def get_population(self):
        return self.__population

    def list_buildings(self):
        return self.__buildings

    def has_building(self, b_id):
        return b_id in self.__buildings

    def add_building(self, building_id):
        if not self.has_building(building_id):
            self.__buildings.append(building_id)

    def assign_planet(self, planet):
        self.__planet = planet

    def get_food_summary(self):
        return self.__food_summary

    def get_industry_summary(self):
        return self.__industry_summary

    def get_research_summary(self):
        return self.__research_summary

    def get_morale_summary(self):
        return self.__morale_summary

    def get_bc_summary(self):
        return self.__bc_summary

    def init_available_production(self, game_rules, players):
        """returns a dict of production id lists"""

        rules_buildings = game_rules['buildings']
        ME = players[self.get_owner()]
        known_techs = ME.get_known_techs()

        replaced = []
        for production_id in self.list_buildings():
            if rules_buildings[production_id].has_key("replaces"):
                print "@ colony::init_available_production() ... replaces" + str(rules_buildings[production_id]['replaces'])
                for replaces_id in rules_buildings[production_id]['replaces']:
                    replaced.append(replaces_id)

        available = {'building': [], 'xship': [], 'special': [], 'capitol': []}
        for production_id, production in rules_buildings.items():
            if production['tech']:
                # knows required technology and not built
                if (production['tech'] in known_techs) and (not self.has_building(production_id)) and (not production_id in replaced):
                    if production.has_key('type'):
                        group_id = production['type']
                    else:
                        group_id = "building"
                    available[group_id].append("%s:%i" % (production['name'], production_id))
        for group_id in available:
            available[group_id].sort()
            for i in range(len(available[group_id])):
                available[group_id][i] = int(available[group_id][i].split(":")[1])

# TODO: check for gravity and colonists, if the gravity generator is not needed here remove it from the list
# TODO: check for colonists if the alien management center is needed, otherwise remove it from the list

        self.__available_production = available

    def get_available_production(self):
        return self.__available_production
    
    """
    """
    def display_summary(self, title, foot, summary):
        r_summary=[]
        total = rules.count_summary_result(summary)
        print("+----------------------------------------------------+")
        print("+ %s +" % title.ljust(50))
        print("+ ================================================== +")
        for k in summary:
            if summary[k]:
                print("+ %s ... %s +" % (str(summary[k]).rjust(6), k.ljust(39)))
                r_summary.append("%s   %s" % (str(summary[k]).rjust(6), k.ljust(39)))
        print("+                                                    +")
        print("+ % 6i ... %s +" % (total, foot.ljust(39)))
        print("+----------------------------------------------------+")
        r_summary.append(' ')
        r_summary.append("% 6i ... %s" % (total, foot.ljust(39)))

        return r_summary

    """
        Returns Morale Summary
    """
    def print_morale_summary(self):
        return self.display_summary("Morale Summary", "Total", self.get_morale_summary())

    # end func print_morale_summary

    def print_bc_summary(self):
        return self.display_summary("BC Summary", "Total Income", self.get_bc_summary())

    # end func print_bc_summary

    def print_food_summary(self):
        return self.display_summary("Food Summary", "Total Food Produced", self.get_food_summary())

    # end func print_food_summary

    def print_industry_summary(self):
        return self.display_summary("Industry Summary", "Total Industry Produced", self.get_industry_summary())
    # end func print_industry_summary

    def print_research_summary(self):
        return self.display_summary("Research Summary", "Research Industry Produced", self.get_research_summary())

    # end func print_research_summary

    """
        counts pollution for given production
    """
    def xget_colony_pollution(self, production, PLAYERS):
        planet = self.__planet
        if self.is_outpost():
            return 0

#	print "$$$ get_colony_pollution $$$"

        if self.has_building(B_CORE_WASTE_DUMP):
            return 0

        production = float(production)

        tolerant = 0
        pop = 0

        for t in (FARMER, SCIENTIST, WORKER):
            for colonist in self.colonists[t]:
                pop += 1
                if PLAYERS[colonist['race']]['racepicks']['tolerant']:
                    tolerant += 1

#	print "    population: %i" % pop
#	print "    tolerant: %i" % tolerant
#	print "    non-tolerant: %i" % (pop - tolerant)
#	print "    planet size: %i" % planet['size']

#	print "	production before atm. renewer: %s" % str(production)
        if self.has_building(B_ATMOSPHERE_RENEWER):
            production = math.ceil(production / 4)
#	print "	production after atm. renewer: %s" % str(production)

        tolerance = [2, 4, 6, 8, 10][planet['size']]

#	if PLAYERS[self.get_owner()]['technologies'][TECH_NANO_DISASSEMBLERS] == 3:
        if TECH_NANO_DISASSEMBLERS in PLAYERS[self.get_owner()]['known_techs']:
            tolerance += tolerance

#	print "    planet tolerance: %i" % tolerance
        pollution = float(max(0, production - tolerance)) / 2
#	print "    pollution: %s" % str(pollution)

        pollution = float(pop - tolerant) * pollution / float(pop)
#	print "    pollution: %s" % str(pollution)

        return round(pollution)
    # end func get_colony_pollution

    def exists(self):
        return self.get_owner() < 0xff

    def set_owner(self, player_id):
        self.__owner = player_id

    def get_owner(self):
        return self.__owner

    def is_owned_by(self, player_id):
        return self.exists() and self.get_owner() == player_id

    def is_outpost(self):
        return self.exists() and self.__is_outpost
        
    def is_colony(self):
        return self.exists() and not self.is_outpost()

    def max_population(self):
        return self.__max_population

    def get_officer(self):
        return self.__officer

    def morale(self):
        return self.__morale

    def bc(self):
        return self.__bc

    def set_food(self, food):
        self.__food = food

    def get_food(self):
        return self.__food

    def set_industry(self, industry):
        self.__industry = industry

    def get_industry(self):
        return self.__industry

    def planet(self):
        return self.__planet

    def pollution(self):
        return self.__pollution

    def set_research(self, research):
        self.__research = research

    def get_research(self):
        return self.__research

    def pop_raised(self):
        return self.__pop_raised

    def pop_grow(self):
        return self.__pop_grow

    def set_build_queue(self, queue):
        self.__build_queue = queue

    def get_build_queue(self):
        return self.__build_queue

    def get_build_queue_ids(self):
        id_list = []
        for item in self.__build_queue:
            id_list.append(item['production_id'])
        return id_list

    def add_build_item(self, production_id, flags = 0):
        if len(self.__build_queue) < 7:
           self.__build_queue.append({'production_id': production_id, 'flags': flags})

    def remove_build_item(self, production_id):
        build_queue_ids = self.get_build_queue_ids()
        if production_id in build_queue_ids:
            self.__build_queue.pop(build_queue_ids.index(production_id))

    def get_build_item(self):
        if len(self.__build_queue) > 0:
            if self.__build_queue[0]['production_id'] == 0xFF:
                return None
            elif self.__build_queue[0]['production_id'] == 249:  # repeat
                return self.__build_queue[1]
            else:
                return self.__build_queue[0]

        else:
            return None

    def in_build_queue(self, production_id):
        """
            Returns True if given productiion_id is already in queue
        """
        return production_id in self.get_build_queue_ids()

    """
        get_agregated_populations
    """
    def get_agregated_populations(self):
        pops    = [0, 0, 0, 0, 0, 0, 0, 0]
        for t in [FARMER, WORKER, SCIENTIST]:
            for colonist in self.colonists[t]:
                pops[colonist['race']] += 1
        return pops
    # end func get_agregated_populations


    def get_max_populations(self):
        return self.__max_populations

    """
    http://masteroforion2.blogspot.com/2005/09/growth-formula.html
    """
    def get_population_growth(self, max_populations, PLAYERS):
        growth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if self.is_outpost():
            return growth

        pops   = self.get_agregated_populations()

#	print "$$$ get_population_growth $$$ ... %s" % self.name
#	print "		populations: %s" % pops
#	print "		max_populations: %s" % max_populations


        total_population = sum(pops)

#	microbiotics	= False
#    	universal_antidote	= False

#    	print PLAYERS[colony['owner']]['technologies']
#    	print "	universal_antidote: %i" % PLAYERS[colony['owner']]['technologies'][193]

        if 192 in PLAYERS[self.get_owner()].get_known_techs():
            universal_antidote_bonus	= 50
        else:
            universal_antidote_bonus	= 0

        for race in range(8):
            race_population = pops[race]
            if race_population:
#    		print "	race: %i" % race
                max_population = max_populations[race]
#    		print "		race_population: %i" % race_population
#		print "		max_population: %i" % max_population
#		print "		total_population: %i" % total_population
#		print "		universal_antidote_bonus: %i" % universal_antidote_bonus

                b = math.floor((2000 * race_population * max(0, max_population - total_population) / max_population) ** 0.5)

                g, t, r, l, h = 0, 0, 0, 0, 0

                race_bonus			= PLAYERS[race].get_racepick_item('population')	# most races have 0, Sakkra have 100 here
                microbiotics_bonus		= 0	# 25 when invented
                random_bonus		= 0	# 100 when Boom of 100%
                leader_bonus		= 0	# e.g. 30 on Medicine 30%

                a = 100 + race_bonus + (microbiotics_bonus + universal_antidote_bonus) + random_bonus + leader_bonus

    # TODO: apply Clonning center
                c = 0

                growth[race] = int(((a * b) / 100) + math.floor(c))
    
#		print "$$$ get_population_growth $$$"
#		print "	race_population: %i" % race_population
#		print "	max_population: %i" % max_population
#		print "	agregated_population: %i" % agregated_population
#		print "	=> b: %i" % b
#		print "	+"
#		print "	a ..."
#		print "	="
#		print "	%i" % growth

        return growth
    # end func get_population_growth

    """
        raise the population
    """
    def raise_population(self):
        if self.get_owner() == 0xff:
            print "	owner is 0xff"
            return

        max_populations = self.get_max_populations()
#	print "raise_population ... max_populations: %s" % str(max_populations)
#	print "raise_population ... pop_raised: %s" % str(self.__pop_raised)
#	print "raise_population ... pop_grow: %s" % str(self.__pop_grow)
        for race in range(8):
    	    self.__pop_raised[race] += self.__pop_grow[race]
    	    if self.__pop_raised[race] > 999:
                # the race that turns over 999 in pop_raised gets a new farmer
        	r1 = self.get_owner()
                self.colonists[FARMER].append({'a': r1 & race, 'b': FARMER, 'c': 0x00, 'd': 0x00, 'r1': r1, 'race': race})
                self.__pop_raised[race] -= 1000
                self.__population += 1
    # end func raise_population

    def total_population(self):
        return len(self.colonists[FARMER]) + len(self.colonists[WORKER]) + len(self.colonists[SCIENTIST])

    def sumary_result(self, summary):
        res = 0.0
        for k, v in summary.iterkeys():
                res += float(v)
        return res

    """
        recounts colony values, should be called after any change
    """
    def recount(self, game_rules, colony_leader, players):
#	print "$$$ colony::recount() ... colony_id = %i" % self.colony_id

        self.__bc			= 0
        if not self.exists():
            self.__population           = 0
            self.__max_populations      = rules.get_empty_max_populations()
#	    print "	owner is 0xff"
#	    print
            return

#	planet = self.__planet

        if self.is_outpost():
#	    print "	this is outpost"
#	    print
            self.__population           = 0
            self.__pollution		= 0
            self.__industry		= 0
            self.__research		= 0
#	    self.__food_summary		= {}
#	    self.__industry_summary	= {}
#	    self.__research_summary	= {}
            self.__max_populations      = rules.get_empty_max_populations()
            return
        else:
        
#            officer = self.get_officer()
#            print(" * officer: %i" % officer)


#	    print "	name: %s" % self.name
#	    print "	owner: %s (%i)" % (PLAYERS[self.get_owner()]['race'], self.get_owner())

            """
                morale
            """
            self.__morale_summary = rules.compose_morale_summary(game_rules, self, colony_leader, players)
            self.__morale = rules.count_summary_result(self.__morale_summary)

            """
                food
            """
#	    print "### Recount of colony %i ... %s" % (self.colony_id, self.name)
#	    print "	industry:"
#	    print "		before: %i" % self.__industry
            self.__food_summary = rules.compose_food_summary(game_rules, self, players)
            self.__food = rules.count_summary_result(self.__food_summary)
#	    print "		after: %i" % self.__industry

            """
                industry
            """
#	    print "### Recount of colony %i ... %s" % (self.colony_id, self.name)
#	    print "	industry:"
#	    print "		before: %i" % self.__industry
            self.__industry_summary = rules.compose_industry_summary(game_rules, self, colony_leader, players)
            self.__pollution = self.__industry_summary['pollution']
            self.__industry = rules.count_summary_result(self.__industry_summary)
#	    print "		after: %i" % self.__industry

            """
                BC
            """
            self.__bc_summary = rules.compose_bc_summary(game_rules, self, players)
            self.__bc = rules.count_summary_result(self.__bc_summary)

            """
                research
            """
#	    print "	research:"
#	    print "		before: %i" % self.__research
            self.__research_summary = rules.compose_research_summary(game_rules, self, players)
            self.__research = rules.count_summary_result(self.__research_summary)
#	    print "		after: %i" % self.__research

            """
                population
            """
            self.__max_populations = rules.compose_max_populations(self, players)
            self.__max_population = max(self.__max_populations)
            self.__pop_grow = self.get_population_growth(self.__max_populations, players)

#	    for t in [FARMER, WORKER, SCIENTIST]:
#		for i in range(len(self.colonists[t])):
#		    pass
#		    print "colonists type #%i ... race: %i" % (t, self.colonists[t][i]['race'])
#		for colonist in self.colonists[t]:
#            	pops[colonist['race']] += 1

#	    print
#	    print("")
            self.init_available_production(game_rules, players)
    # end func recount

    def debug_production(self, rules):
        print("    @ colony::debug_production()... colony_id = %i" % self.get_id())
        for build_item in self.get_build_queue():
            production_id = build_item['production_id']
            if rules['buildings'][production_id].has_key('type'):
                type = rules['buildings'][production_id]['type']
            else:
                type = "building"
            print("        production_id: %3i ... flags: %3i ... type: %10s ... %s" % (production_id, build_item['flags'], type, rules['buildings'][production_id]['name']))
        print("")
#            print("        production_id: %i" % production_id)
##            print("            flags: %i" % build_item['flags'])
#            print("            name: %s" % rules['buildings'][production_id]['name'])
#            print("            type: %s" % type)


class EnemyColony(Colony):

    def __init__(self, colony_id, player_id):
        self.set_id(colony_id)
        self.set_owner(player_id)

    def is_outpost(self):
        return False
