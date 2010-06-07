
__author__="peterman"
__date__ ="$Jan 7, 2009 8:44:49 PM$"

import pygame

import get_input
#import debug

#from rules import RULES

SHOW_TYPE = None

##
#       DRAW
##
def draw(GAME):
    global SHOW_TYPE

    DISPLAY	= GAME['DISPLAY']
    IMAGES	= GAME['IMAGES']
    FONTS	= GAME['FONTS']

    DATA        = GAME['DATA']
    STARS       = DATA['stars']

    DISPLAY.blit(IMAGES['LEADERS_SCREEN'], (0, 0))

    if SHOW_TYPE == 1:
        DISPLAY.blit(IMAGES['OFFICER.LBX']['buttons']['colony_leaders'], (7, 10))
    else:
        DISPLAY.blit(IMAGES['OFFICER.LBX']['buttons']['ship_officers'], (160, 10))


#    debug.debug_heroes(GAME)

#    HEROES = GAME['DATA']['heroes']
#    HEROES = DATA[["my_colony_leaders", "officers"][SHOW_TYPE]]
    HEROES = DATA[["colony_leaders", "officers"][SHOW_TYPE]]
    
    i = -1
    for hero_id in HEROES.keys():
        hero = HEROES[hero_id]
#        print(hero)
#	if (hero['player'] == 0) and (hero['type'] == SHOW_TYPE):
        i += 1
#	    print(hero['name'])
        DISPLAY.blit(IMAGES['OFFICER.LBX']['leaders'][hero['picture']], (13, 38 + (109 * i)))

        DISPLAY.blit(FONTS['font_12_bold'].render(hero['name'], 1, (0x78, 0x9c, 0xc0)), (125, 36 + (109 * i)))

        if hero['location'] == 0xffff:
            location = "Officer Pool"
        else:
            if SHOW_TYPE == 1:
                location = STARS[hero['location']].get_name()
            elif SHOW_TYPE == 0:
                location = "ship..."

        text_width, text_height = FONTS['font_11'].size(location)
        DISPLAY.blit(FONTS['font_11'].render(location, 1, (0x78, 0x9c, 0xc0)), (49 - (text_width / 2), 130 + (109 * i)))

        skills = []

        if hero['type'] == 0:		# ship leader skills
            if hero['special_skills'] & 4:
                skills.append(['fighter_pilot', "Fighter Pilot"])
            if hero['special_skills'] & 8:
                skills.append(['fighter_pilot', "Fighter Pilot*"])
            if hero['special_skills'] & 16:
                skills.append(['galactic_role', "Galactic Role"])
            if hero['special_skills'] & 32:
                skills.append(['galactic_role', "Galactic Role*"])
            if hero['special_skills'] & 64:
                skills.append(['helmsman', "Helmsman"])
            if hero['special_skills'] & 128:
                skills.append(['helmsman', "Helmsman*"])
            if hero['special_skills'] & 256:
                skills.append(['navigator', "Navigator"])
            if hero['special_skills'] & 512:
                skills.append(['navigator', "Navigator*"])
            if hero['special_skills'] & 1024:
                skills.append(['ordnance', "Ordnance"])
            if hero['special_skills'] & 2048:
                skills.append(['ordnance', "Ordnance*"])
            if hero['special_skills'] & 16384:
                skills.append(['weaponry', "Weaponry"])
            if hero['special_skills'] & 32768:
                skills.append(['weaponry', "Weaponry*"])

        elif hero['type'] == 1:		# colony leader skills
            if hero['special_skills'] & 16:
                skills.append(['financial_leader', "Financial Leader"])
            if hero['special_skills'] & 32:
                skills.append(['financial_leader', "Financial Leader*"])
            if hero['special_skills'] & 64:
                skills.append(['instructor', "Instructor"])
            if hero['special_skills'] & 128:
                skills.append(['instructor', "Instructor*"])
            if hero['special_skills'] & 256:
                skills.append(['labor_leader', "Labor Leader"])
            if hero['special_skills'] & 512:
                skills.append(['labor_leader', "Labor Leader*"])
            if hero['special_skills'] & 1024:
                skills.append(['medicine', "Medicine"])
            if hero['special_skills'] & 2048:
                skills.append(['medicine', "Medicine*"])
            if hero['special_skills'] & 4096:
                skills.append(['science_leader', "Science Leader"])
            if hero['special_skills'] & 8196:
                skills.append(['science_leader', "Science Leader*"])
            if hero['special_skills'] & 16384:
                skills.append(['spiritual_leader', "Spiritual Leader"])
            if hero['special_skills'] & 32768:
                skills.append(['spiritual_leader', "Spiritual Leader*"])
            if hero['special_skills'] & 65536:
                skills.append(['tactics', "Tactics"])
            if hero['special_skills'] & 131072:
                skills.append(['tactics', "Tactics*"])
            
        if hero['common_skills'] & 1:	# commond skills
            skills.append(['assassin', "Assassin"])
        if hero['common_skills'] & 2:
            skills.append(['assassin', "Assassin*"])
        if hero['common_skills'] & 4:
            skills.append(['commando', "Commando"])
        if hero['common_skills'] & 8:
            skills.append(['commando', "Commando*"])
        if hero['common_skills'] & 16:
            skills.append(['diplomat', "Diplomat"])
        if hero['common_skills'] & 32:
            skills.append(['diplomat', "Diplomat*"])
        if hero['common_skills'] & 64:
            skills.append(['famous', "Famous"])
        if hero['common_skills'] & 128:
            skills.append(['famous', "Famous*"])
        if hero['common_skills'] & 256:
            skills.append(['megawealth', "Megawealth"])
        if hero['common_skills'] & 512:
            skills.append(['megawealth', "Megawealth*"])
        if hero['common_skills'] & 1024:
            skills.append(['operations', "Operations"])
        if hero['common_skills'] & 2048:
            skills.append(['operations', "Operations*"])
        if hero['common_skills'] & 4096:
            skills.append(['researcher', "Researcher"])
        if hero['common_skills'] & 8192:
            skills.append(['researcher', "Researcher*"])
        if hero['common_skills'] & 16384:
            skills.append(['spy_master', "Spy Master"])
        if hero['common_skills'] & 32768:
            skills.append(['spy_master', "Spy Master*"])
        if hero['common_skills'] & 65536:
            skills.append(['telepath', "Telepath"])
        if hero['common_skills'] & 131072:
            skills.append(['telepath', "Telepath*"])
        if hero['common_skills'] & 262144:
            skills.append(['trader', "Trader"])
        if hero['common_skills'] & 524288:
            skills.append(['trader', "Trader*"])

#	    skills = []
#	    skills.append(['91', "91"])
#	    skills.append(['92', "92"])
#	    skills.append(['108', "108"])

        skill_row = 0
        for skill in skills:
            y = 50 + (109 * i) + (17 * skill_row)
            DISPLAY.blit(IMAGES['OFFICER.LBX']['skill_icons'][skill[0]], (94, y))
            DISPLAY.blit(FONTS['font_13_bold'].render(skill[1], 1, (0x78, 0x9c, 0xc0)), (114, y))
            skill_row += 1
                
            

    pygame.display.flip()
# end func draw

##
#       RUN
##
def run(GAME):
    global SHOW_TYPE

    draw(GAME)

    triggers = [
        {'action': "ESCAPE",        	'rect': pygame.Rect((544, 445), (70, 18))},
        {'action': "hire",         	'rect': pygame.Rect((319, 445), (70, 18))},
        {'action': "showColonyLeaders", 'rect': pygame.Rect((15, 14), (135, 15))},
        {'action': "showShipOfficers",	'rect': pygame.Rect((160, 14), (135, 15))}

    ]

    while True:
        event = get_input.get_input(triggers)
        action = event['action']

        if (action == "ESCAPE"):
            return

        if (action == "showColonyLeaders"):
            if SHOW_TYPE == 0:
        	SHOW_TYPE = 1
                draw(GAME)

        if (action == "showShipOfficers"):
            if SHOW_TYPE == 1:
        	SHOW_TYPE = 0
                draw(GAME)

        else:
            print "UNKNONW ACTION: " + action
    

if SHOW_TYPE is None:
    SHOW_TYPE = 1
