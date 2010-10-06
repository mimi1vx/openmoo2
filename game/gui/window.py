import time
import pygame

import input

class Window():

    def __init__(self, ui):
        self.set_ui(ui)
        self.reset_triggers_list()
        self.__input = input.Input()

    def log_info(self, message):
        ts = int(time.time())
        print("# INFO %i ... %s" % (ts, message))

    def log_error(self, message):
        ts = int(time.time())
        print("! ERROR %i ... %s" % (ts, message))

    def set_display(self, display):
#        print("@ @ @ gui_window::Window::set_display()")
        self.__display = display

    def get_display(self):
        return self.get_ui().get_display()

    def set_ui(self, ui):
#        print("@ @ @ gui_window::Window::__set_ui()")
        self.__ui = ui

    def get_ui(self):
        return self.__ui

    def get_all_fonts(self):
        return self.__ui.get_all_fonts()

    def get_font(self, font_id):
        return self.__ui.get_font(font_id)

    def reset_triggers_list(self):
        self.__triggers = []

    def add_trigger(self, trigger):
        if not trigger.has_key('hover_id'):
            trigger['hover_id'] = None
        self.__triggers.append(trigger)

    def get_triggers_list(self):
        return self.__triggers

    def get_trigger(self, trigger_id):
        return self.__triggers[trigger_id]

    def redraw_event_id(self):
        return self.__redraw_event

    def get_timestamp(self, zoom = 1):
        return int(time.time() * zoom)

    def set_redraw_mouse_timer(self, timing):
        pygame.time.set_timer(self.__input.redraw_mouse_event(), timing)

    def set_redraw_screen_timer(self, timing):
        pygame.time.set_timer(self.__input.redraw_screen_event(), timing)

    def set_mouse_cursor(self, surface):
        self.__input.set_mouse_cursor(surface)

    def redraw_mouse_cursor(self):
        self.__input.draw_mouse_cursor()

    def force_draw_mouse_cursor(self):
        self.__input.force_draw_mouse_cursor()

    def get_event(self):
        return self.__input.get_event(self.get_triggers_list())

    
    def draw_textbox(self, lines, x, y, title="", color = (0,255,0)):

        """draws a MOO2 textbox of varying size,at position x,y,  big enough to output all strings in lines[] """
        buttons = []
        schemes_font_palette = [0x0, 0x141420, 0x6c688c]
        light_text_palette = [0x0, 0x802810, 0xe48820, 0xe46824]
        dark_text_palette = [0x0, 0x440c00, 0xac542c]


        self.add_trigger({'action': "ESCAPE",    	'rect': pygame.Rect((1, 1), ( 640, 480))})


        DISPLAY         = self.get_display()

        font2 = self.get_font('font2')
        font3 = self.get_font('font3')
        font5 = self.get_font('font5')

        screen_width, screen_height = 640, 480;

        mid_part_width=self.get_image('text_box','top').get_width();
        mid_part_height=10 + 15*len(lines);

        off_y1 = self.get_image('text_box','top').get_height();
        off_y2 = mid_part_height + off_y1;

        y3 = self.get_image('text_box','bottom').get_height();

        
        
        # kludge? Correction for outsized boxes, where the bottom would have ended up outside of screen area
        bottom_box_boundary = y + mid_part_height + off_y1 +y3;
        if( bottom_box_boundary) > screen_height :
            y = y - (bottom_box_boundary - screen_height)

        y1 = y + off_y1;
        y2 = y + off_y2;


        DISPLAY.blit(self.get_image('text_box','top'), (x, y))
        temp_r = pygame.Rect((1,1),(1+mid_part_width,1+mid_part_height))

        DISPLAY.blit(self.get_image('text_box','middle'), (x, y1),temp_r);

        DISPLAY.blit(self.get_image('text_box','bottom'), (x, y2))

        font5.write_text(DISPLAY, x + 120, y + 20, title, light_text_palette, 1)

        lheight=40;

        for i in range(len(lines)):
        #   TODO: some intelligent way of justifying the lines, so the output resembles the original game
            font3.write_text(DISPLAY, x + 40, y + lheight, lines[i], dark_text_palette, 1)
            lheight=lheight+15

        self.flip()

        while True:
            event = self.get_event()
            if event:
                action = event['action']

                print "Textbox method, event: "+action;
                if action == "ESCAPE":
                    return

            #return buttons


