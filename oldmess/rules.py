import math

from _buildings import *

from _game_constants import *
import _research
import _tech_table
import _governments

__author__="peterman"
__date__ ="$Jan 2, 2010 12:42:33 PM$"

PLANETS_MINERALS = {
    0: { 'worker_base':	1 },
    1: { 'worker_base':	2 },
    2: { 'worker_base':	3 },
    3: { 'worker_base':	5 },
    4: { 'worker_base':	8 },
}

PLANETS_SPECIALS = {
    SPECIAL_ARTIFACTS: {
        'research_bonus':		+2,
    }
}

DEFAULT_RULES = {

    'hero_levels':                      (0, 60, 150, 300, 1000, 2000),
    'planets_minerals':			PLANETS_MINERALS,
    'planets_specials':			PLANETS_SPECIALS,
    'research':				_research.RESEARCH,
    'research_areas':			_research.RESEARCH_AREAS,
    'tech_table':			_tech_table.TECH_TABLE,
    'buildings':			BUILDINGS,
    'governments':                      _governments.GOVERNMENTS,
}

"""
    'planet_worker_base':                           [1, 2, 3, 5, 8],
    'microlite_construction_per_worker':            1,
    'microlite_construction_industry_bonus':        1,

#    'automated_factory':                            5,
#    'automated_factory_per_worker':                 1,
#    'automated_factory_industry_bonus':             1,

#    'robo_miner_plant':                             10,
#    'robo_miner_plant_per_worker':                  2,
#    'robo_miner_plant_industry_bonus':              2,

#    'deep_core_mine':                               15,
#    'deep_core_mine_per_worker':                    3,
#    'deep_core_mine_industry_bonus':                3,

    'robotic_factory_mineral_bonuses':              [5, 8, 10, 15, 20],

    'weather_controller_farmer_bonus':              2,

    'astro_university_farmer_bonus':                1,
    'astro_university_worker_bonus':                1,
    'astro_university_scientist_bonus':             1,

    'research_lab':                                 5,
    'research_lab_scientist_bonus':                 1,
    'supercomputer':                                10,
    'supercomputer_scientist_bonus':                2,

    'autolab':                                      30,


    'heightened_intelligence_research_bonus':       1,
    'artifacts_reseach_bonus':                      2,
"""

"""
    returns the Food production summary table
"""
def compose_food_summary(RULES, colony, PLAYERS):
    planet = colony.planet()

#    if planet is None:
#        print("ERROR: colony has no planet!")
#        print("colony.owner() = %i" % colony.get_owner())

#    print("rules::compose_food_summary() colony.get_id() = %i" % colony.get_id())
#    print("rules::compose_food_summary() planet.get_id() = %i" % planet.get_id())

    summary = {
        'farmers':			0,
#        'astro_university':		0,
        'aquatic_bonus':		0,
#        'weather_controller':	0,
#        'morale_bonus':		0,
#        'hydroponic_farm':		0,
#        'blockaded':		0,
#        'government_bonus':		0
    }

    RULES_BUILDINGS	= RULES['buildings']

    farmers_num = len(colony.colonists[FARMER])

    goverment = PLAYERS[colony.get_owner()].get_racepick_item('goverment')

    for colonist in colony.colonists[FARMER]:
        summary['farmers'] += planet.get_foodbase()
        if PLAYERS[colonist['race']].get_racepick_item('aquatic'):
#		print "	aquatic farmer!"
            if planet.get_terrain() in [TERRAIN_OCEAN, TERRAIN_TERRAN]:
                summary['aquatic_bonus'] += 1

    # apply buildings farmer_bonus
    for b_id in colony.list_buildings():
        if BUILDINGS[b_id].has_key("farmer_bonus"):
#	    b_sum_key = "building_%i" % b_id
            b_sum_key = "%s_bonus" % BUILDINGS[b_id]['name']
            summary[b_sum_key] = farmers_num * RULES_BUILDINGS[b_id]['farmer_bonus']

    # count in morale
    summary['morale_bonus'] = float(sum(summary.values())) * colony.morale() / 100

    # apply buildings food_production
    for b_id in colony.list_buildings():
        if RULES_BUILDINGS[b_id].has_key("food_production"):
#	    b_sum_key = "building_%i" % b_id
            b_sum_key = "%s" % BUILDINGS[b_id]['name']
            summary[b_sum_key] = RULES_BUILDINGS[b_id]['food_production']

    # TODO: apply blockade
    # TODO: apply food replicators

    if goverment == GOVERMENT_UNIFICATION:
        summary['government_bonus'] = sum(summary.values()) // 2

    return summary
# /compose_food_summary

"""
    returns the hashmap of production items
"""
def compose_industry_summary(RULES, colony, colony_leader, PLAYERS):
    BUILDINGS = RULES['buildings']

    TECH_TABLE = RULES['tech_table']

    ME = PLAYERS[colony.get_owner()]

    planet = colony.planet()
    summary = {
        'workers':			0,
#        'microlite_constructions':	0,
#        'automated_factory_people':	0,
#        'deep_core_mine_people':	0,
#        'robominer_plant_people':	0,
#        'morale_bonus':                 0,
        'gravity_penalty':		0,
#        'blockaded':                    0,
#        'government_bonus':		0,
#        'recyclotron':                  0,
#        'automated_factory_bonus':	0,
#        'robominer_plant_bonus':	0,
#        'deep_core_mine_bonus':         0,
#        'robotic_factory':		0,
        'pollution':                    0,
    }

    planet_minerals = planet.get_minerals()

    worker_base = RULES['planets_minerals'][planet_minerals]['worker_base']
    player_goverment = PLAYERS[colony.get_owner()].get_racepick_item('goverment')
    industry_per_worker = worker_base

    workers_num = len(colony.colonists[WORKER])

    for colonist in colony.colonists[WORKER]:
        summary['workers'] += worker_base + PLAYERS[colonist['race']].get_racepick_item('industry')


    # TODO: appply technologies worker_bonus
    for tech_id in ME.get_known_techs():
        if TECH_TABLE[tech_id].has_key("worker_bonus"):
            b_sum_key = "%s ... bonus" % TECH_TABLE[tech_id]['name']
            summary[b_sum_key] = workers_num * TECH_TABLE[tech_id]['worker_bonus']
            industry_per_worker += TECH_TABLE[tech_id]['worker_bonus']

    # appply buildings worker_bonus
    for b_id in colony.list_buildings():
        if BUILDINGS[b_id].has_key("worker_bonus"):
            b_sum_key = "%s ... bonus" % BUILDINGS[b_id]['name']
            summary[b_sum_key] = workers_num * BUILDINGS[b_id]['worker_bonus']
            industry_per_worker += BUILDINGS[b_id]['worker_bonus']

    tmp_sum = float(sum(summary.values()))
#    print "rules::compose_industry_summary() ... tmp_sum = %f" % tmp_sum


    # TODO: apply morale!
    morale_bonus = tmp_sum * colony.morale() / 100

    if colony_leader and colony_leader['skills'].has_key('industry_bonus'):
#        print colony_leader
        leader_bonus = colony_leader['skills']['industry_bonus'] + (colony_leader['level'] * colony_leader['skills']['industry_bonus'])
#        print "rules::compose_industry_summary() ... leader_bonus = %f" % leader_bonus
        leader_bonus = tmp_sum * leader_bonus / 100
#        print "rules::compose_industry_summary() ... leader_bonus = %f" % leader_bonus
#                   print "leader_bonus = %i" % leader_bonus
#        summary['Leader Bonus'] = round((colony_leader['skills']['morale_bonus'] + (colony_leader['level'] * colony_leader['skills']['morale_bonus'])) / 10) * 10
    else:
        leader_bonus = 0



    # TODO: apply government
    if player_goverment == 6:			# GOVERMENT_UNIFICATION
        summary['government_bonus'] = tmp_sum * 0.5

    if morale_bonus:
        summary['Moral Bonus'] = morale_bonus
    if leader_bonus:
        summary['Leader Bonus'] = leader_bonus


#	print "industry_per_worker: %i" % industry_per_worker
#	print "planet gravity: %i" % planet['gravity']
    if not colony.has_building(B_GRAVITY_GENERATOR):
        for colonist in colony.colonists[WORKER]:
            if PLAYERS[colonist['race']].get_racepick_item('low_g'):
                # log-G race
                if planet.get_gravity() == 1:				# normal-G planet
                    summary['gravity_penalty'] -= float((industry_per_worker + PLAYERS[colonist['race']].get_racepick_item('industry'))) / 4
            elif PLAYERS[colonist['race']].get_racepick_item('high_g'):
                pass
            else:
                # normal-G race
                if planet.get_gravity() == 2:				# high-G planet
                    summary['gravity_penalty'] -= float((industry_per_worker + PLAYERS[colonist['race']].get_racepick_item('industry'))) / 2


    total = round(sum(summary.values()))
#	print "@@@ colony::get_industry_summary ... total = %s" % str(total)

#    summary['pollution'] -= colony.get_colony_pollution(total, PLAYERS)
    summary['pollution'] -= count_colony_pollution(colony, total, PLAYERS)

    if colony.has_building(B_RECYCLOTRON):
        summary['recyclotron'] = len(colony.colonists[FARMER]) + workers_num + len(colony.colonists[SCIENTIST])

    # apply buildings industry
    for b_id in colony.list_buildings():
        if BUILDINGS[b_id].has_key("industry"):
            b_sum_key = "%s ... industry" % BUILDINGS[b_id]['name']
            summary[b_sum_key] = BUILDINGS[b_id]['industry']

    # apply buildings industry_by_minerals
    for b_id in colony.list_buildings():
        if BUILDINGS[b_id].has_key("industry_by_minerals"):
            b_sum_key = "building_%s_minerals" % BUILDINGS[b_id]['name']
            summary[b_sum_key] = BUILDINGS[b_id]['industry_by_minerals'][planet_minerals]


    # TODO: apply food replicator: original ratio is 2 production units -> 1 food

    return summary
# /compose_industry_summary

"""
    returns the hasmap of research items
"""
def compose_research_summary(RULES, colony, PLAYERS):
    planet = colony.planet()
    summary = {
        'scientists':		0,
#        'artifacts':		0,
#        'intelligence':		0,
#        'supercomputer_people':	0,
#        'supercomputer_bonus':	0,
#        'research_lab_people':	0,
#        'research_lab_bonus':	0,
        'gravity_penalty':		0.0,
#        'astro_university':		0,
        'race_bonus':		0,
#        'morale_bonus':		0,
#        'government_bonus':		0,
#        'autolab':			0
    }

    if colony.is_outpost():
        return summary
    base = 3

    player_goverment = PLAYERS[colony.get_owner()].get_racepick_item('goverment')

    scientist_num = len(colony.colonists[SCIENTIST])

    morale = float(colony.morale())

    for colonist in colony.colonists[SCIENTIST]:
        race = colonist['race']
        summary['scientists'] += base
        summary['race_bonus'] += PLAYERS[race].get_racepick_item('science')

#        if PLAYERS[race]['technologies'][TECH_HEIGHTENED_INTELLIGENCE] == 3:
        if TECH_HEIGHTENED_INTELLIGENCE in PLAYERS[race].get_known_techs():
            summary['intelligence'] += RULES['heightened_intelligence_research_bonus']

        if RULES['planets_specials'].has_key(planet.get_special()):
            if RULES['planets_specials'][planet.get_special()].has_key("research_bonus"):
                summary['special'] = RULES['planets_specials'][planet.get_special()]['research_bonus']

#        if planet['special'] == SPECIAL_ARTIFACTS:
#            research['artifacts'] += RULES['artifacts_reseach_bonus']

        if not colony.has_building(B_GRAVITY_GENERATOR):
            if PLAYERS[race].get_racepick_item('low_g'):
                # low-G colonist
                if planet.get_gravity() == PLANET_NORMAL_G:	# normal-G planet
                    summary['gravity_penalty'] -= 1.75
            elif PLAYERS[race].get_racepick_item('high_g'):
                # high-G colonist
                pass
            else:
                # normal-G colonist
                if planet.get_gravity() == PLANET_HEAVY_G:
                    summary['gravity_penalty'] -= float(base) / 2

    # appply buildings scientist_bonus
    if scientist_num:
        for b_id in colony.list_buildings():
            if BUILDINGS[b_id].has_key("scientist_bonus"):
                b_sum_key = "%s ... bonus" % BUILDINGS[b_id]['name']
                summary[b_sum_key] = scientist_num * BUILDINGS[b_id]['scientist_bonus']

    # Government bonus
    morale_bonus = (morale * (float(sum(summary.values())))) / 100

    if player_goverment == GOVERMENT_DEMOCRACY:
        summary['government_bonus'] = float(sum(summary.values()) - summary['gravity_penalty']) * 0.5
    elif player_goverment == GOVERMENT_FEUDAL:
        summary['government_bonus'] = round(round(sum(summary.values()) - summary['gravity_penalty']) * -0.5)

    if morale_bonus:
        summary['morale_bonus'] = morale_bonus

    # appply buildings research
    for b_id in colony.list_buildings():
        if BUILDINGS[b_id].has_key("research"):
            b_sum_key = "%s ... research" % BUILDINGS[b_id]['name']
            summary[b_sum_key] = BUILDINGS[b_id]['research']

    return summary
# /compose_research_summary

def compose_morale_summary(RULES, colony, colony_leader, PLAYERS):
    ME = PLAYERS[colony.get_owner()]
    BUILDINGS = RULES['buildings']
    TECH_TABLE = RULES['tech_table']

    summary = {
#        'government_morale':	0,
#        'marine_barracks':		0,
#        'psionics':			0,
#        'holo_simulator':		0,
#        'virtual_reality_network':	0
    }

#	print(colony.get_owner())
#	print(PLAYERS[colony.get_owner()])
#	print(PLAYERS[colony.get_owner()]['racepicks'])
    player_goverment = PLAYERS[colony.get_owner()].get_racepick_item('goverment')
    summary['Government Morale'] = RULES['governments'][player_goverment]['morale']
#	print "@@@ colony::get_morale_summary ... goverment = %i" % player_goverment

    # Marine Barracks ... Eliminates morale penalties for dictatorship and feudal governments
#    if (colony.buildings[B_MARINE_BARRACKS]) and (player_goverment in [GOVERMENT_FEUDAL, GOVERMENT_FEUDAL2, GOVERMENT_DICTATORSHIP, GOVERMENT_IMPERIUM]):
#    if colony.has_building(B_MARINE_BARRACKS) and (player_goverment in [GOVERMENT_FEUDAL, GOVERMENT_FEUDAL2, GOVERMENT_DICTATORSHIP, GOVERMENT_IMPERIUM]):
#        summary['marine_barracks'] = 20

    # Holo Simulator ... Increases a planet's morale by +20%
#    if colony.has_building(B_HOLO_SIMULATOR):
 #       summary['holo_simulator'] = 20

    
    for b_id in colony.list_buildings():

        # appply buildings government_morale_bonus
        if BUILDINGS[b_id].has_key("government_morale_bonus"):
            b_sum_key = "%s_gov" % BUILDINGS[b_id]['name']
            summary[b_sum_key] = BUILDINGS[b_id]['government_morale_bonus'][player_goverment]

        # appply buildings morale_bonus
        if BUILDINGS[b_id].has_key("morale_bonus"):
            b_sum_key = BUILDINGS[b_id]['name']
            summary[b_sum_key] = BUILDINGS[b_id]['morale_bonus']

    # Psionics ... Morale on all planets is increased by 10% for dictatorship and imperium government

#	print "@@@ colony::get_morale_summary ... TECH_PSIONICS = %i" % PLAYERS[colony.get_owner()]['technologies'][TECH_PSIONICS]
#    if (PLAYERS[colony.get_owner()]['technologies'][TECH_PSIONICS] == 3) and (player_goverment in [GOVERMENT_DICTATORSHIP, GOVERMENT_IMPERIUM]):
#    if (TECH_PSIONICS in PLAYERS[colony.get_owner()].get_known_techs()) and (player_goverment in [GOVERMENT_DICTATORSHIP, GOVERMENT_IMPERIUM]):
#        summary['psionics'] = 10
    
    for tech_id in ME.get_known_techs():

        # appply technologies government_morale_bonus
        if TECH_TABLE[tech_id].has_key("government_morale_bonus"):
            b_sum_key = "%s_gov" % TECH_TABLE[tech_id]['name']
            summary[b_sum_key] = TECH_TABLE[tech_id]['government_morale_bonus'][player_goverment]

        # appply technologies morale_bonus
        if TECH_TABLE[tech_id].has_key("morale_bonus"):
            b_sum_key = "%s_bonus" % TECH_TABLE[tech_id]['name']
            summary[b_sum_key] = TECH_TABLE[tech_id]['morale_bonus']

    if colony_leader and colony_leader['skills'].has_key('morale_bonus'):
#        print colony_leader
#        print "leader morale_bonus = %i" % leader_morale_bonus
        summary['Leader Bonus'] = round((colony_leader['skills']['morale_bonus'] + (colony_leader['level'] * colony_leader['skills']['morale_bonus'])) / 10) * 10

    return summary
# /compose_morale_summary

"""
    Returns BC Summary
"""
def compose_bc_summary(RULES, colony, PLAYERS):
    planet = colony.planet()

    summary = {
        'taxes_collected':		0,
        'special_income':		0,
        'morale_bonus':		0,
        'government_bonus':		0,
        'stock_exchange':		0,
        'spaceport':		0,
        'trade_goods':		0
    }

    # Taxes Collected
    # TODO: do natives and androids produce taxes too?
    summary['taxes_collected'] = len(colony.colonists[FARMER] + colony.colonists[WORKER] + colony.colonists[SCIENTIST])

    # Special Income - Gold Deposits
    if planet.get_special() == 4:
        summary['special_income'] = 5

    # Morale Bonus
    morale = float(colony.morale())
    summary['morale_bonus'] = round(morale * (float(sum(summary.values()))) / 100)

    # Government Bonus
    player_goverment = PLAYERS[colony.get_owner()].get_racepick_item('goverment')
    if player_goverment == GOVERMENT_DEMOCRACY:
        summary['government_bonus'] = int(sum(summary.values()) / 2)

    # Planetary Stock Exchange
    if colony.has_building(B_STOCK_EXCHANGE):
        summary['stock_exchange'] = summary['taxes_collected']

    # Spaceport
    if colony.has_building(B_SPACEPORT):
        summary['spaceport'] = int(summary['taxes_collected'] / 2)

    # TODO: Trade Goods ... round the 50% of industry
    build_queue = colony.get_build_queue()
#	print build_queue[0]
#	print build_queue[1]
#	print build_queue[2]
#	print build_queue[3]
#	print build_queue[4]
#	print build_queue[5]
#	print build_queue[6]
    if (len(build_queue) > 0) and (build_queue[0]['production_id'] == BUILD_TRADE_GOODS):
        summary['trade_goods'] = int(colony.get_industry() / 2)


    return summary
# /compose_bc_summary

def get_empty_max_populations():
    return [0, 0, 0, 0, 0, 0, 0, 0]
# /get_empty_max_populations

"""
http://masteroforion2.blogspot.com/2005/10/maximum-population.html
"""
def compose_max_populations(colony, PLAYERS):
    planet = colony.planet()

    max_populations = get_empty_max_populations()
    if colony.is_outpost():
        return max_populations

    size = planet.get_size()
    terrain = planet.get_terrain()

    size_multiplier = [5, 10, 15, 20, 25][size]

    for i in range(8):
        player = PLAYERS[i]
#		print player['racepicks']

        if player.get_racepick_item('aquatic'):
            terrain_multiplier = [25, 25, 25, 25, 80, 100, 80, 60, 100, 100][terrain]	# Aquatic
        else:
            terrain_multiplier = [25, 25, 25, 25, 25, 25, 40, 60, 80, 100][terrain]	# default

        if player.get_racepick_item('tolerant'):
            terrain_multiplier += 25

        terrain_multiplier = min(terrain_multiplier, 100)

        if player.get_racepick_item('subterranean'):
            bonus = [2, 4, 6, 8, 10][size]		# Subterranean = 2 pop per each size class
        else:
            bonus = 0

    # TODO: Advanced City Planning ... bonus + 5

        max_populations[i] = round((float(size_multiplier * terrain_multiplier) / 100) + bonus)

        if colony.has_building(B_BIOSPHERES):
            max_populations[i] += 2

    present = [0, 0, 0, 0, 0, 0, 0, 0]
    for t in [FARMER, WORKER, SCIENTIST]:
        for colonist in colony.colonists[t]:
#	    	print "race: %i" % colonist['race']
            present[colonist['race']] = 1

#    	print "$$$ max_populations: %s $$$ before present filter" % max_populations
    for i in range(8):
        max_populations[i] = int(max_populations[i] * present[i])

    return max_populations
# /get_max_populations

def count_colony_pollution(colony, production, players):
#    print "$$$ count_colony_pollution $$$"
    planet = colony.planet()
    if colony.is_outpost():
        return 0


    if colony.has_building(B_CORE_WASTE_DUMP):
        return 0

    production = float(production)

    tolerant = 0
    pop = 0

    for t in (FARMER, SCIENTIST, WORKER):
        for colonist in colony.colonists[t]:
            pop += 1
            if players[colonist['race']].get_racepick_item('tolerant'):
                tolerant += 1

#	print "    population: %i" % pop
#	print "    tolerant: %i" % tolerant
#	print "    non-tolerant: %i" % (pop - tolerant)
#	print "    planet size: %i" % planet['size']

#	print "	production before atm. renewer: %s" % str(production)
    if colony.has_building(B_ATMOSPHERE_RENEWER):
        production = math.ceil(production / 4)
#	print "	production after atm. renewer: %s" % str(production)

    tolerance = [2, 4, 6, 8, 10][planet.get_size()]

#	if PLAYERS[self.get_owner()]['technologies'][TECH_NANO_DISASSEMBLERS] == 3:
    if TECH_NANO_DISASSEMBLERS in players[colony.get_owner()].get_known_techs():
        tolerance += tolerance

#	print "    planet tolerance: %i" % tolerance
    pollution = float(max(0, production - tolerance)) / 2
#	print "    pollution: %s" % str(pollution)

    pollution = float(pop - tolerant) * pollution / float(pop)
#	print "    pollution: %s" % str(pollution)

    return round(pollution)
# /get_colony_pollution


def count_summary_result(summary):
    sum = 0.0
    for k in summary:
        sum += float(summary[k])
    return round(sum)

def research_costs(research_areas, area, rp):
    if not area:
        return -1
    else:
        return research_areas[area]['cost']
# /research_costs

def research_turns(cost, progress, rp):
    if not rp:
        return -1
    else:
        cost = float(cost)
        progress = float(progress)
        rp = float(rp)
#        print("rules::research_turns() ... cost = %s" % str(cost))
#        print("rules::research_turns() ... rp = %s" % str(rp))
        return int(math.ceil((cost - progress) / rp))
#        return int(math.ceil((cost/rp)+math.sqrt(2*(cost/rp)-1)))
# /research_turns