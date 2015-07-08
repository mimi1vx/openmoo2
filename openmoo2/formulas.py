
#from math import floor

from _game_constants import *

from _buildings import *

GOVERMENT_FEUDAL	= 0
GOVERMENT_DICTATORSHIP	= 2
GOVERMENT_DEMOCRACY	= 4
GOVERMENT_UNIFICATION	= 6

TERRAIN_TOXIC		= 0
TERRAIN_RADIATED	= 1
TERRAIN_BARED		= 2
TERRAIN_DESERT		= 3
TERRAIN_TUNDRA		= 4
TERRAIN_OCEAN		= 5
TERRAIN_SWAMP		= 6  
TERRAIN_ARID		= 7
TERRAIN_TERRAN		= 8
TERRAIN_GAIA		= 9

MINERAL_ULTRAPOOR	= 0
MINERAL_POOR		= 1
MINERAL_ABUNDANT	= 2
MINERAL_RICH		= 3
MINERAL_ULTRARICH	= 4

SPECIAL_ARTIFACTS	= 10

R_MICROLITE_CONSTRUCTION	= 108

def get_colony_farming(planet, colony, players):
    if colony.is_outpost():
        return 0

    planet_terrain = planet['terrain']
    planet_bases = [0, 0, 0, 2, 2, 2, 2, 4, 4, 6]
    farming = 0

#    print "	planet_terrain: %s" % planet['terrain']

    colony_owner = colony.owner
    player_goverment = players[colony_owner]['racepicks']['goverment']
#    print "	player_goverment: %i" % player_goverment

    for colonist in colony.colonists[FARMER]:
        racepick_farming = players[colonist['race']]['racepicks']['farming']
        racepick_aquatic = players[colonist['race']]['racepicks']['aquatic']
#	print "	colonist: %s ... %i (aquatic = %i)" % (colonist, racepick_farming, racepick_aquatic)

        if racepick_aquatic and (planet_terrain in (TERRAIN_OCEAN, TERRAIN_TERRAN)):
            base = planet_bases[TERRAIN_GAIA]
        elif racepick_aquatic and (planet_terrain in (TERRAIN_TUNDRA, TERRAIN_SWAMP)):
            base = planet_bases[TERRAIN_TERRAN]
        else:
            base = planet_bases[planet_terrain]
        
        
        farming += base + racepick_farming

    if player_goverment == GOVERMENT_UNIFICATION:
        farming = (farming * 150) / 100
    
    return farming / 2
# end func get_colony_farming
