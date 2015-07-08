import screen
import pygame

import networking
import gui

class LeadersScreen(screen.Screen):

    def __init__(self):
        screen.Screen.__init__(self)
        self.__type = 1

    def reset_triggers_list(self):
        screen.Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE",        	'rect': pygame.Rect((544, 445), (70, 18))})
        self.add_trigger({'action': "hire",         	'rect': pygame.Rect((319, 445), (60, 18))})
        self.add_trigger({'action': "showColonyLeaders", 'rect': pygame.Rect((15, 14), (135, 15))})
        self.add_trigger({'action': "showShipOfficers",	'rect': pygame.Rect((160, 14), (135, 15))})

    def draw(self):

        DISPLAY	= gui.GUI.get_display()
        STARS = networking.Client.list_stars()

        if self.__type == 1:
            HEROES = networking.Client.list_colony_leaders()
        else:
            HEROES = networking.Client.list_officers()

        self.reset_triggers_list()

        font3 = gui.GUI.get_font('font3')
        font4 = gui.GUI.get_font('font4')

        DISPLAY.blit(self.get_image('leaders_screen', 'panel'), (0, 0))

        if self.__type == 1:
            DISPLAY.blit(self.get_image('leaders_screen', 'colony_leaders_button'), (7, 10))
        else:
            DISPLAY.blit(self.get_image('leaders_screen', 'ship_officers_button'), (7, 10))

        common_palette = [0x0, 0x20284c, 0x789cc0]

        i = -1
        for hero_id, hero in HEROES.items():
            i += 1
#            DISPLAY.blit(self.__leader_faces[hero['picture']], (13, 38 + (109 * i)))
            DISPLAY.blit(self.get_image('leader', 'face', hero['picture']), (13, 38 + (109 * i)))


            font4.write_text(DISPLAY, 125, 38 + (109 * i), hero['name'], common_palette, 1)

            if hero['location'] == 0xffff:
                location_text = "Officer Pool"
            else:
                if self.__type == 1:
                    location_text = STARS[hero['location']].get_name()
                elif self.__type == 0:
                    location_text = "ship..."

            location_surface = font3.render(location_text, common_palette, 2)
#            text_width, text_height = FONTS['font_11'].size(location)
            text_width, text_height = location_surface.get_size()


#            DISPLAY.blit(FONTS['font_11'].render(location, 1, (0x78, 0x9c, 0xc0)), (49 - (text_width / 2), 130 + (109 * i)))
#            font3.write_text(DISPLAY, x, y, text, palette, letter_spacing)
            DISPLAY.blit(location_surface, (49 - (text_width / 2), 131 + (109 * i)))

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

            skill_row = 0
            for skill in skills:
                y = 50 + (109 * i) + (17 * skill_row)
                DISPLAY.blit(self.get_image('leader', 'skill_icon', skill[0]), (94, y))
                font4.write_text(DISPLAY, 116, y + 4, skill[1], common_palette, 1)
                skill_row += 1

    def process_trigger(self, trigger):
        if trigger['action'] == "showColonyLeaders" and self.__type == 0:
            self.__type = 1
            self.redraw_flip()

        elif trigger['action'] == "showShipOfficers" and self.__type == 1:
            self.__type = 0
            self.redraw_flip()


Screen = LeadersScreen()