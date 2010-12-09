import pygame

import screen
import networking
import gui

class ResearchScreen(screen.Screen):

    def __init__(self):
        screen.Screen.__init__(self)

    def draw(self):
        hover = self.get_hover()
        DISPLAY = gui.GUI.get_display()

        DISPLAY.blit(self.get_image('research_screen', 'panel'), (80, 0))

        RULES = networking.Client.rules()
        ME = networking.Client.get_me()

        font4 = gui.GUI.get_font('font4')
        font5 = gui.GUI.get_font('font5')

        self.reset_triggers_list()

        research_areas = ME.list_research_areas()

        tech_color = 0x047800
        tech_hover_color = 0x28c800
        tech_active_color = 0x64d000

        for research in research_areas:
            research_index = RULES['research'][research]['index']
            first_tech_id = research_areas[research][0]
            first_tech = RULES['tech_table'][first_tech_id]
            area_id = first_tech['area']

            if ME.get_research_area() == area_id:
                color = tech_active_color
            else:
                color = tech_color

            x = 95 + (227 * (research_index % 2))
            y = 51 + (105 * (research_index // 2))

            font5.write_text(DISPLAY, x, y, RULES['research_areas'][area_id]['name'], [0x0, 0x181818, color, color], 2)

            i = 0
            y += 19
            x += 10
            for tech_id in research_areas[research]:
                if (hover is not None) and (hover['action'] == "set_research") and (hover['tech_id'] == tech_id):
                    write_color = tech_hover_color
                else:
                    write_color = color

                label = font4.render(RULES['tech_table'][tech_id]['name'], [0x0, 0x181818, write_color], 2)

                yy = i * 15
                DISPLAY.blit(label, (x, y + yy))
                self.add_trigger({'action': "set_research", 'tech_id': tech_id, 'rect': pygame.Rect((x, y + yy), label.get_size())})
                i += 1

    def process_trigger(self, trigger):
        print("@ research_screen::trigger()")
        print("    %s" % trigger)

        if trigger['action'] == "set_research":
            tech_id = trigger['tech_id']
            networking.Client.set_research(tech_id)
            return self.get_escape_trigger()


Screen = ResearchScreen()