
#import formulas

#from game import *
#import techtable

def bin(i):
    if i > 1:
        return bin(i >> 1) + str(i & 1)
    return str(i & 1)
# end func bin

def debug_stars(GAME):
    STARS	= GAME['DATA']['stars']
    for star in STARS:
        print "Star % 3i ... % 15s ... size = %i ... coordinates: [%i, %i]" % (star['id'], star['name'], star['size'], star['x'], star['y'])
#	print "		size: %i" % star['size']
#	print
    print
# end func debug_stars

def debug_colonies_population(GAME):
    DATA	= GAME['DATA']
    STARS	= DATA['stars']
    PLANETS	= DATA['planets']
    COLONIES	= DATA['colonies']
    PLAYERS	= DATA['players']
    
    print "planets: %i" % len(PLANETS)
    for i in range(len(COLONIES)):
        colony		= COLONIES[i]
        planet_id	= colony.planet_id
        if planet_id < len(PLANETS):
#	    print "planet_id: %i" % planet_id
            planet	= PLANETS[planet_id]
            if colony.is_outpost():
                print "Outpost %i ... %s %i" % (i, STARS[planet['parent_star']]['name'], PLANETS[planet_id]['num'])
            else:
                max_populations = colony.get_max_populations(PLAYERS)
                max_population = max(max_populations)
                research = colony.research
                print "Colony %i ... %s %i" % (i, STARS[planet['parent_star']]['name'], PLANETS[planet_id]['num'])
                print "			population: %i / %i (loaded max population: %i)" % (colony['population'], max_population, colony['max_population'])
                print "			research: %i (loaded is: %i)" % (research, colony['total_research'])
                for k in research_data.keys():
                    print "				%s: %s" % (k, research_data[k])
#    		print "colony #%.3i : % 15s % 10i / % 2i" % (i, name, colony['population'], max_population)
#		print "	planet_id: %i" % colony['planet_id']
#		print "		terraformations: %i" % planet['terraformations']
#		farming		= formulas.get_colony_farming(planet, colony, PLAYERS)
#		print "	max_population: %i (counted = %i)" % (colony['max_population'], max(max_populations))
#		print "	population: %i" % colony['population']
#		print "	owner: %s" % PLAYERS[colony['owner']]['race']
#		print "	total_food: %i (counted = %i)" % (colony['total_food'], farming)
#		print "	total_production: %i (counted = %i, poluttion = %i) ... RESULT = %i" % (colony['total_production'], production, pollution, (production - pollution))
                print
# end func debug_colonies_population


def debug_players(GAME):

    DATA = GAME['DATA']
#    DISPLAY = GAME['DISPLAY']
#    IMAGES = GAME['IMAGES']
#    FONTS = GAME['FONTS']

#    tchst = ["non-reserchable", "unknown", "???", "KNOWN"]
    technames = techtable.get_technames()

    player = DATA['players'][0]

    print "%s emperor of %s" % (player['emperor'], player['race'])
    print "	objective: %i" % player['objective']
    print "	color: %i" % player['color']
    print "     known technologies:"
    for i in range(203):
#        techname = "?"
        status = player['technologies'][i]
        if status == 3:
    	    print "         #%.3i %s" % (i, technames[i])
        elif player['research_item'] and (i == player['research_item']-1):
    	    print "         #%.3i %s ... RESEARCHING" % (i, technames[i])
    print

#end func debug_clonies_popilation

def debug_heroes(GAME):
    HEROES = GAME['DATA']['heroes']
    for i in range(len(HEROES)):
        hero = HEROES[i]
#	if hero['player'] < 0xff:
        if hero['player'] == 0:
    	    print "hero %i" % i
            for k in hero.keys():
                print "	%s: %s" % (k, hero[k])
            print
# end func debug_heroes

def debug_ships(GAME):
    SHIPS = GAME['DATA']


    return
    DICTIONARY	= GAME['DICTIONARY']
    PLAYERS	= GAME['DATA']['players']
#    STARS	= GAME['DATA']['stars']
    SHIPS	= GAME['DATA']['ships']
    i = 0
    statuses	= ["orbiting", "traveling", "launching", "status3", "status4", "status5", "building", "status7"]
    for ship in SHIPS:
        if ship['status'] != 5:			# 5 = destroyed?
            design = ship['design']
            print "Ship % 3i ... % 15s ... coordinates: [%i, %i]" % (i, design['name'], ship['x'], ship['y'])
#		print "	design:"
            print "		        name: %s" % design['name']
            print "		        size: %i ... %s" % (design['size'], DICTIONARY['SHIP_SIZES'][design['size']])
#	    print "		        type: %i ... %s" % (design['type'], DICTIONARY['SHIP_TYPES'][design['type']])
#	    print "		      shield: %i ... %s" % (design['shield'], DICTIONARY['SHIELDS'][design['shield']])
#	    print "		       drive: %i ... %s" % (design['drive'], DICTIONARY['DRIVES'][design['drive']])
#	    print "		       speed: %i" % design['speed']
#	    print "		    computer: %i ... %s" % (design['computer'], DICTIONARY['COMPUTERS'][design['computer']])
#	    print "		       armor: %i ... %s" % (design['armor'], DICTIONARY['ARMORS'][design['armor']])
#	    print "		    specials: ..."
#	    print "		     weapons: ..."
#	    print "		     picture: %i" % design['picture']
#	    print "		     builder: %i" % design['builder']
#	    print "		combat_speed: %i" % design['combat_speed']
#	    print "		  build_date: %s" % stardate(design['build_date'])
#	    print "	data:"
            print "		       owner: %i ... %s" % (ship['owner'], PLAYERS[ship['owner']]['race'])
            if ship['owner'] < 8:
                print "		player color: %i" % PLAYERS[ship['owner']]['color']
            print "		      status: %i ... %s" % (ship['status'], statuses[ship['status']])
#	    print "		 coordinates: %i, %i" % (ship['x'], ship['y'])
            print "		    location: %i" % ship['location']
            print "		  location_x: %i" % ship['location_x']
#	    print "		    location: %i ... %s" % (ship['location'], STARS[ship['location']]['name'])
#	    print "		  turns_left: %i" % ship['turns_left']
            if ship['status'] == 2:
                location = ship['location']
                location_x = ship['location_x']
                result = (location_x << 8) + location
                print "			location: %i ... %s" % (location, bin(location))
                print "		      location_x: %i ... %s" % (location_x, bin(location_x))
                print "			  result: %i ... %s" % (result, bin(result))
            print
            i += 1
# end func debug_ships
