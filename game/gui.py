import copy
import lbx

class Gui():

    def __init__(self, pg, default_font):
        self.__pygame = pg
        self.__pygame.init()
        self.__pygame.display.set_mode((640, 480), 0, 24)
        self.__default_font = default_font
        self.__images = {}
    # /__init__

    def get_fonts(self):
        return {
            'font_10':		self.__pygame.font.SysFont(self.__default_font, 10),
            'font_10_bold':	self.__pygame.font.SysFont(self.__default_font, 10, True),
            'font_11':		self.__pygame.font.SysFont(self.__default_font, 11),
            'font_11_bold':	self.__pygame.font.SysFont(self.__default_font, 11, True),
            'font_12':		self.__pygame.font.SysFont(self.__default_font, 12),
            'font_12_bold':	self.__pygame.font.SysFont(self.__default_font, 12, True),
            'font_13':		self.__pygame.font.SysFont(self.__default_font, 13),
            'font_13_bold':	self.__pygame.font.SysFont(self.__default_font, 13, True),
            'font_14':		self.__pygame.font.SysFont(self.__default_font, 14),
            'font_14_bold':	self.__pygame.font.SysFont(self.__default_font, 14, True),
            'font_15':		self.__pygame.font.SysFont(self.__default_font, 15),
            'font_15_bold':	self.__pygame.font.SysFont(self.__default_font, 15, True),
            'font_16':		self.__pygame.font.SysFont(self.__default_font, 16),
            'font_16_bold':	self.__pygame.font.SysFont(self.__default_font, 16, True),
            'font_17':		self.__pygame.font.SysFont(self.__default_font, 17),
            'font_17_bold':	self.__pygame.font.SysFont(self.__default_font, 17, True),
            'font_18':		self.__pygame.font.SysFont(self.__default_font, 18),
            'font_18_bold':	self.__pygame.font.SysFont(self.__default_font, 18, True),
            'FONT3':		self.__pygame.font.SysFont(self.__default_font, 18)
        }
    # /get_fonts

    def load_lbx_archives(self, moo2_dir = "../moo2"):
#        print("Loading LBX archives located in %s directory" % moo2_dir)
        self.__lbx = {
            'APP_PICS.LBX':     lbx.Archive("%s/APP_PICS.LBX" % moo2_dir, "7b04085428c25c8d1ef26d18c45e10ff"),
            'BUFFER0.LBX':      lbx.Archive("%s/BUFFER0.LBX" % moo2_dir, "72061ddf5816d13287a720c0606ea845"),
            'COLBLDG.LBX':      lbx.Archive("%s/COLBLDG.LBX" % moo2_dir, "d4c75440f233eb3170f1d01719f4b915"),
            'COLONY2.LBX':      lbx.Archive("%s/COLONY2.LBX" % moo2_dir, "cc054705454ceae81c37ffd42a312412"),
            'COLPUPS.LBX':      lbx.Archive("%s/COLPUPS.LBX" % moo2_dir, "2ecad5faf06c64afb8124b162d21b253"),
            'COLSUM.LBX':       lbx.Archive("%s/COLSUM.LBX" % moo2_dir, "cb9be56155b2304abb92613ca5549980"),
            'COLSYSDI.LBX':     lbx.Archive("%s/COLSYSDI.LBX" % moo2_dir, "d2ad38fc93b6876246868b880acd7ec9"),
            'FONTS.LBX':        lbx.Archive("%s/FONTS.LBX" % moo2_dir, "51002fdf406bac511f649fff9c1f531c"),
            'GAME.LBX':         lbx.Archive("%s/GAME.LBX" % moo2_dir, "6ac9233d3c0221c2a01c24e7e995de63"),
            'IFONTS.LBX':       lbx.Archive("%s/IFONTS.LBX" % moo2_dir, "deb8a07d2446b725810904d1d73def87"),
            'INFO.LBX':         lbx.Archive("%s/INFO.LBX" % moo2_dir, "2b7d672d890d936072f9bd9c9e9e3d51"),
            'MAINMENU.LBX':	lbx.Archive("%s/MAINMENU.LBX" % moo2_dir, "d6d537ea650a324738ec5adf2dadc529"),
            'OFFICER.LBX':      lbx.Archive("%s/OFFICER.LBX" % moo2_dir, "65cc1180ca1246667bbdaf49cb47517f"),
            'PLANETS.LBX':      lbx.Archive("%s/PLANETS.LBX" % moo2_dir, "6996b43ea2e8329e14e1ad366a804129"),
            'PLNTSUM.LBX':      lbx.Archive("%s/PLNTSUM.LBX" % moo2_dir, "37465fb75f1864fa750f3163acfe6261"),
            'RACEICON.LBX':	lbx.Archive("%s/RACEICON.LBX" % moo2_dir, "db068efad10498daeb38c48b5425f681"),
            'SR_R9_SC.LBX':     lbx.Archive("%s/SR_R9_SC.LBX" % moo2_dir, "07e1d2361881c5373c71ee4a29a0a267"),
            'TECHSEL.LBX':      lbx.Archive("%s/TECHSEL.LBX" % moo2_dir, "db472e2a7f8185536a21db6e9c73a7a5")
        }
    # /load_lbx_archives

    def check_lbx_archives(self):
        check = True
        for arch_key, arch_obj in self.__lbx.items():
            if arch_obj.check_md5():
                print("%s ... MD5 checksum OK" % arch_obj.get_filename())
            else:
                print("ERROR: %s ... md5 checksum FAILED" % arch_obj.get_filename())
                print("    expected MD5: %s" % arch_obj.md5_hexdigest_expected())
                print("      actual MD5: %s" % arch_obj.md5_hexdigest())
#                print("    > possibly corrupted file or not original MOO2 version 1.31 file")
                print("")
                check = False
        return check
#        if self.__md5_hexdigest == md5sum:
#            print("%s md5 checksum OK" % filename)
#        else:
#            print("%s md5 checksum FAILED ... expected %s got %s" % (filename, self.__md5_hexdigest, md5sum))


    def get_lbx_archives(self):
        return self.__lbx
    # /get_lbx_archives

    def load_raw_palettes(self):
        self.__raw_palettes = {
            'FONTS_01': self.__lbx['FONTS.LBX'].read_palette(1),
            'FONTS_02': self.__lbx['FONTS.LBX'].read_palette(2),
            'FONTS_03': self.__lbx['FONTS.LBX'].read_palette(3),
            'FONTS_04': self.__lbx['FONTS.LBX'].read_palette(4),
            'FONTS_05': self.__lbx['FONTS.LBX'].read_palette(5),
            'FONTS_06': self.__lbx['FONTS.LBX'].read_palette(6),
            'FONTS_07': self.__lbx['FONTS.LBX'].read_palette(7),
            'FONTS_08': self.__lbx['FONTS.LBX'].read_palette(8),
            'FONTS_09': self.__lbx['FONTS.LBX'].read_palette(9),
            'FONTS_10': self.__lbx['FONTS.LBX'].read_palette(10),
            'FONTS_11': self.__lbx['FONTS.LBX'].read_palette(11),
            'FONTS_12': self.__lbx['FONTS.LBX'].read_palette(12),
            'FONTS_13': self.__lbx['FONTS.LBX'].read_palette(13),

            'IFONTS_1': self.__lbx['IFONTS.LBX'].read_palette(1),
            'IFONTS_2': self.__lbx['IFONTS.LBX'].read_palette(2),
            'IFONTS_3': self.__lbx['IFONTS.LBX'].read_palette(3),
            'IFONTS_4': self.__lbx['IFONTS.LBX'].read_palette(4)
        }
    # /load_raw_palettes

    def get_raw_palettes(self):
        return self.__raw_palettes
    # /get_raw_palettes
    
    def init_palettes(self):
        self.__palettes = {
            'APP_PICS.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'BUFFER0.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'COLBLDG.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'COLONY2.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'COLPUPS.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'COLSUM.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'COLSYSDI.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'GAME.LBX':         copy.deepcopy(self.__raw_palettes['FONTS_01']),
            'INFO.LBX':         copy.deepcopy(self.__raw_palettes['FONTS_01']),
            'MAINMENU.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_06']),
            'OFFICER.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'PLANETS.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'RACEICON.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'SR_R9_SC.LBX':	copy.deepcopy(self.__raw_palettes['FONTS_02'])
        }
    # /init_palettes
    
    def set_palette_color(self, palette_key, color_num, color_def):
        self.__palettes[palette_key][color_num] = color_def
    # /set_palette_color
    
    def get_palettes(self):
        return self.__palettes
    # /get_palettes

    def load_image(self, lbx_key, picture_id, picture_frame, palette_key, color_key):
        return self.__lbx[lbx_key].get_surface(picture_id, picture_frame, self.__palettes[palette_key], color_key)
    # /load_image

    def set_image(self, image_key, image_data):
        self.__images[image_key] = image_data
    # /set_image

    def get_image(self, image_key):
        return self.__images[image_key]
    # /get_image

    def draw_image(self, image_key, target, x, y):
        target.blit(self.get_image(image_key), (x, y))
    # /draw_image

    def draw_screen(self, image_key, target):
        target.blit(self.get_image(image_key), (0, 0))
    # /draw_screen

    def load_splashscreen(self):
        self.__images['MAIN_MENU_BG'] = self.load_image('MAINMENU.LBX', 0, 0, 'MAINMENU.LBX', None)
    # /load_splashscreen

    def draw_splashscreen(self, target):
        self.draw_image('MAIN_MENU_BG', target, 0, 0)
    # /draw_splashscreen

    def load_planet_background(self, picture_num):
        self.__images['PLANET_BACKGROUND'][picture_num] = self.load_image('PLANETS.LBX', picture_num, 0, 'PLANETS.LBX', None)

    def load_graphic(self):
        IMAGES = self.__images

        IMAGES['MAIN_SCREEN'] = {}
        IMAGES['MAIN_SCREEN']['background'] = self.load_image('COLONY2.LBX', 49, 0, 'COLONY2.LBX', None)
        IMAGES['MAIN_SCREEN']['screen'] = self.load_image('BUFFER0.LBX', 0, 0, 'BUFFER0.LBX', 0x00)
        IMAGES['LEADERS_SCREEN'] = self.load_image('OFFICER.LBX', 0, 0, 'BUFFER0.LBX', None)
        IMAGES['MAIN_LEFT_3_BUTTONS'] = self.load_image('BUFFER0.LBX', 3, 0, 'BUFFER0.LBX', None)
        IMAGES['MAIN_ZOOM_IN'] = self.load_image('BUFFER0.LBX', 6, 0, 'BUFFER0.LBX', None)
        IMAGES['MAIN_ZOOM_OUT'] = self.load_image('BUFFER0.LBX', 7, 0, 'BUFFER0.LBX', None)
        IMAGES['MAIN_TURN_ON'] = self.load_image('BUFFER0.LBX', 12, 0, 'BUFFER0.LBX', None)

        #	star map
        IMAGES['MAP_STARS'] = {}
        for star_class in range(7):
            IMAGES['MAP_STARS'][star_class] = {}
            for star_size in range(6):
                pic = 148 + (6 * star_class) + (5 - star_size)
                IMAGES['MAP_STARS'][star_class][star_size] = self.load_image('BUFFER0.LBX', pic, 0, 'BUFFER0.LBX', None)

        IMAGES['STARSYSTEM_DIALOG'] = self.load_image('BUFFER0.LBX', 73, 0, 'BUFFER0.LBX', 0x00)

        IMAGES['SYSTEM_ORBIT'] = {}
        for i in range(5):
            IMAGES['SYSTEM_ORBIT'][i] = self.load_image('BUFFER0.LBX', 77 + i, 0, 'BUFFER0.LBX', 0x00)

        IMAGES['SYSTEM_ASTEROIDS'] = {}
        for i in range(1):
            IMAGES['SYSTEM_ASTEROIDS'][i] = self.load_image('BUFFER0.LBX', 91 + i, 0, 'BUFFER0.LBX', lbx.COLORKEY)

        IMAGES['SYSTEM_STAR'] = {}
        for i in range(6):
            IMAGES['SYSTEM_STAR'][i] = self.load_image('BUFFER0.LBX', 83 + i, 0, 'BUFFER0.LBX', 0x00)
        IMAGES['SYSTEM_STAR'][6] = self.load_image('BUFFER0.LBX', 184 , 0, 'BUFFER0.LBX', 0x00)

        IMAGES['SYSTEM_PLANETS'] = {}
        for terrain in range(10):
            IMAGES['SYSTEM_PLANETS'][terrain] = {}
            for size in range(5):
                IMAGES['SYSTEM_PLANETS'][terrain][size] = self.load_image('BUFFER0.LBX', (92 + (5 * terrain) + size), 0, 'BUFFER0.LBX', None)

        IMAGES['SYSTEM_GAS_GIANTS'] = {}
        for size in range(5):
#	    IMAGES['SYSTEM_GAS_GIANTS'][size] = self.load_image('BUFFER0.LBX', 142 + size, 0, 'BUFFER0.LBX', None)
            IMAGES['SYSTEM_GAS_GIANTS'][size] = self.load_image('BUFFER0.LBX', 142, 0, 'BUFFER0.LBX', None)

        IMAGES['SYSTEM_COLONY_MARKS'] = {}
        IMAGES['SYSTEM_OUTPOST_MARKS'] = {}
        for color in range(8):
            IMAGES['SYSTEM_COLONY_MARKS'][color] = self.load_image('BUFFER0.LBX', 35 + color, 0, 'BUFFER0.LBX', 0x00)
            IMAGES['SYSTEM_OUTPOST_MARKS'][color] = self.load_image('BUFFER0.LBX', 43 + color, 0, 'BUFFER0.LBX', 0x00)

    #	COLONY VIEW

        # planets backgrounds are lazy loaded...
        IMAGES['PLANET_BACKGROUND'] = {}
        for i in range(30):
            IMAGES['PLANET_BACKGROUND'][i] = None

        IMAGES['COLONY_SCREEN'] = {}
        IMAGES['COLONY_SCREEN']['background'] = IMAGES['MAIN_SCREEN']['background']

        IMAGES['COLONY_SCREEN']['panel'] = self.load_image('COLPUPS.LBX', 5, 0, 'COLPUPS.LBX', None)
        IMAGES['COLONY_SCREEN']['planet_arrow'] = self.load_image('COLSYSDI.LBX', 64, 0, 'COLSYSDI.LBX', 0x00)

        IMAGES['COLONY_SCREEN']['planet_schemes'] = {}
        for terrain in range(10):
#	    IMAGES['COLONY_SCREEN']['planet_schemes'].append([])
            IMAGES['COLONY_SCREEN']['planet_schemes'][terrain] = {}
            for size in range(5):
#		IMAGES['COLONY_SCREEN']['planet_schemes'][terrain].append(LBX['COLSYSDI.LBX', 11 + (5 * terrain) + size, 0, 'COLSYSDI.LBX']))
                IMAGES['COLONY_SCREEN']['planet_schemes'][terrain][size] = self.load_image('COLSYSDI.LBX', 11 + (5 * terrain) + size, 0, 'COLSYSDI.LBX', None)

        IMAGES['COLONY_SCREEN']['gasgiant_scheme'] = self.load_image('COLSYSDI.LBX', 61, 0, 'COLSYSDI.LBX', 0x00)
        IMAGES['COLONY_SCREEN']['asteroids_scheme'] = self.load_image('COLSYSDI.LBX', 63, 0, 'COLSYSDI.LBX', 0x00)

        IMAGES['RACEICON.LBX'] = {}
        for i in range(13):
#	    IMAGES['RACEICON.LBX'].append([])
            IMAGES['RACEICON.LBX'][i] = {}
            for ii in range(13):
#		IMAGES['RACEICON.LBX'][i].append(LBX['RACEICON.LBX', (i * 13) + ii, 0, 'RACEICON.LBX'], 0x00))
                IMAGES['RACEICON.LBX'][i][ii] = self.load_image('RACEICON.LBX', (i * 13) + ii, 0, 'RACEICON.LBX', 0x00)

        IMAGES['COLONY2.LBX'] = {}

        IMAGES['COLONY2.LBX']['1food'] = self.load_image('COLONY2.LBX', 0, 0, 'COLONY2.LBX', 0x00)
        IMAGES['COLONY2.LBX']['1production'] = self.load_image('COLONY2.LBX', 1, 0, 'COLONY2.LBX', 0x00)
        IMAGES['COLONY2.LBX']['1research'] = self.load_image('COLONY2.LBX', 2, 0, 'COLONY2.LBX', 0x00)
        IMAGES['COLONY2.LBX']['1money'] = self.load_image('COLONY2.LBX', 3, 0, 'COLONY2.LBX', 0x00)

        IMAGES['COLONY2.LBX']['10food'] = self.load_image('COLONY2.LBX', 4, 0, 'COLONY2.LBX', 0x00)
        IMAGES['COLONY2.LBX']['10production'] = self.load_image('COLONY2.LBX', 5, 0, 'COLONY2.LBX', 0x00)
        IMAGES['COLONY2.LBX']['10research'] = self.load_image('COLONY2.LBX', 6, 0, 'COLONY2.LBX', 0x00)
        IMAGES['COLONY2.LBX']['10money'] = self.load_image('COLONY2.LBX', 3, 0, 'COLONY2.LBX', 0x00)

        IMAGES['OFFICER.LBX'] = {}
        IMAGES['OFFICER.LBX']['buttons'] = {}
        IMAGES['OFFICER.LBX']['buttons']['colony_leaders'] = self.load_image('OFFICER.LBX', 3, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['buttons']['ship_officers'] = self.load_image('OFFICER.LBX', 4, 0, 'BUFFER0.LBX', None)

        IMAGES['OFFICER.LBX']['leaders'] = {}
        for i in range(67):
            IMAGES['OFFICER.LBX']['leaders'][i] = self.load_image('OFFICER.LBX', 21 + i, 0, 'BUFFER0.LBX', None)

        IMAGES['OFFICER.LBX']['skill_icons'] = {}
        IMAGES['OFFICER.LBX']['skill_icons']['assassin'] = self.load_image('OFFICER.LBX', 88, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['commando'] = self.load_image('OFFICER.LBX', 89, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['diplomat'] = self.load_image('OFFICER.LBX', 90, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['91'] = self.load_image('OFFICER.LBX', 91, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['92'] = self.load_image('OFFICER.LBX', 92, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['famous'] = self.load_image('OFFICER.LBX', 93, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['farmer'] = self.load_image('OFFICER.LBX', 94, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['fighter_pilot'] = self.load_image('OFFICER.LBX', 95, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['financial_leader'] = self.load_image('OFFICER.LBX', 96, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['galactic_role'] = self.load_image('OFFICER.LBX', 97, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['helmsman'] = self.load_image('OFFICER.LBX', 98, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['instructor'] = self.load_image('OFFICER.LBX', 99, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['labor_leader'] = self.load_image('OFFICER.LBX', 100, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['medicine'] = self.load_image('OFFICER.LBX', 101, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['megawealth'] = self.load_image('OFFICER.LBX', 102, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['navigator'] = self.load_image('OFFICER.LBX', 103, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['operations'] = self.load_image('OFFICER.LBX', 104, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['ordnance'] = self.load_image('OFFICER.LBX', 105, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['researcher'] = self.load_image('OFFICER.LBX', 106, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['science_leader'] = self.load_image('OFFICER.LBX', 107, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['108'] = self.load_image('OFFICER.LBX', 108, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['spiritual_leader'] = self.load_image('OFFICER.LBX', 109, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['spy_master'] = self.load_image('OFFICER.LBX', 110, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['tactics'] = self.load_image('OFFICER.LBX', 111, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['telepath'] = self.load_image('OFFICER.LBX', 112, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['trader'] = self.load_image('OFFICER.LBX', 113, 0, 'BUFFER0.LBX', None)
        IMAGES['OFFICER.LBX']['skill_icons']['weaponry'] = self.load_image('OFFICER.LBX', 114, 0, 'BUFFER0.LBX', None)

        IMAGES['MAP_SHIPS'] = {}
        for c in range(9):
            IMAGES['MAP_SHIPS'][c] = {}
            for i in range(4):
                IMAGES['MAP_SHIPS'][c][i] = self.load_image('BUFFER0.LBX', 205 + (c * 4 + i), 0, 'BUFFER0.LBX', None)

        for c in range(9, 14):
            IMAGES['MAP_SHIPS'][c] = {}
            for i in range(4):
                IMAGES['MAP_SHIPS'][c][i] = self.load_image('BUFFER0.LBX', 205 + (c * 4 + (3 - i)), 0, 'BUFFER0.LBX', None)

        IMAGES['GOVERNMENT_ICONS'] = {}
        for i in range(8):
            IMAGES['GOVERNMENT_ICONS'][i] = self.load_image('COLONY2.LBX', 19 + i, 0, 'COLONY2.LBX', 0x00)

        IMAGES['MORALE_ICONS'] = {}
        IMAGES['MORALE_ICONS']['good'] = self.load_image('COLONY2.LBX', 16, 0, 'COLONY2.LBX', 0x00)
        IMAGES['MORALE_ICONS']['bad'] = self.load_image('COLONY2.LBX', 17, 0, 'COLONY2.LBX', 0x00)

        IMAGES['GAME_MENU'] = {}
        IMAGES['GAME_MENU']['main'] = self.load_image('GAME.LBX', 0, 0, 'GAME.LBX', None)

        IMAGES['GAME_MENU']['settings'] = self.load_image('GAME.LBX', 29, 0, 'GAME.LBX', None)
        IMAGES['GAME_MENU']['settings1'] = self.load_image('GAME.LBX', 31, 0, 'GAME.LBX', None)
        IMAGES['GAME_MENU']['settings2'] = self.load_image('GAME.LBX', 8, 0, 'GAME.LBX', None)
        IMAGES['GAME_MENU']['settings3'] = self.load_image('GAME.LBX', 30, 0, 'GAME.LBX', None)

        IMAGES['GAME_MENU']['load_game'] = self.load_image('GAME.LBX', 11, 0, 'GAME.LBX', None)
        IMAGES['GAME_MENU']['save_game'] = self.load_image('GAME.LBX', 14, 0, 'GAME.LBX', None)

        # main palette debug
#	i = 0
#	for color in PALETTES['BUFFER0.LBX']:
#	    print "%i ... %s" % (i, color)
#	    i += 1

#	PALETTES['BUFFER0.LBX'][32] = {'alpha': 1, 'rgb': 0xECECEC}	# 000c10 -> ececec
#	PALETTES['BUFFER0.LBX'][33] = {'alpha': 1, 'rgb': 0xF4F4F4}	# 00141c -> f4f4f4
#	PALETTES['BUFFER0.LBX'][34] = {'alpha': 1, 'rgb': 0xFCFCFC}	# 0c2834 -> fcfcfc
#	PALETTES['BUFFER0.LBX'][45] = {'alpha': 1, 'rgb': 0xAC9C94}	# 200c10 -> ac9c94
#	PALETTES['BUFFER0.LBX'][108] = {'alpha': 1, 'rgb': 0x000818}	# f4e094 -> 000818
#	PALETTES['BUFFER0.LBX'][109] = {'alpha': 1, 'rgb': 0x000818}	# fcecb0 -> 000818

        self.set_palette_color('BUFFER0.LBX', 32, {'alpha': 1, 'rgb': 0xECECEC})	# 000c10 -> ececec
        self.set_palette_color('BUFFER0.LBX', 33, {'alpha': 1, 'rgb': 0xF4F4F4})	# 00141c -> f4f4f4
        self.set_palette_color('BUFFER0.LBX', 34, {'alpha': 1, 'rgb': 0xFCFCFC})	# 0c2834 -> fcfcfc
        self.set_palette_color('BUFFER0.LBX', 45, {'alpha': 1, 'rgb': 0xECECEC})	# 200c10 -> ac9c94
        self.set_palette_color('BUFFER0.LBX', 108, {'alpha': 1, 'rgb': 0xECECEC})	# f4e094 -> 000818
        self.set_palette_color('BUFFER0.LBX', 109, {'alpha': 1, 'rgb': 0xECECEC})	# fcecb0 -> 000818

        IMAGES['INFO_SCREEN'] = {}
        IMAGES['INFO_SCREEN']['panel'] = self.load_image('INFO.LBX', 0, 0, 'BUFFER0.LBX', None)
        IMAGES['INFO_SCREEN']['return'] = self.load_image('INFO.LBX', 2, 0, 'BUFFER0.LBX', None)
        IMAGES['INFO_SCREEN']['history_graph_off'] = self.load_image('INFO.LBX', 3, 0, 'BUFFER0.LBX', None)
        IMAGES['INFO_SCREEN']['tech_review_off'] = self.load_image('INFO.LBX', 4, 0, 'BUFFER0.LBX', None)
        IMAGES['INFO_SCREEN']['race_statistics_off'] = self.load_image('INFO.LBX', 5, 0, 'BUFFER0.LBX', None)
        IMAGES['INFO_SCREEN']['turn_summary_off'] = self.load_image('INFO.LBX', 6, 0, 'BUFFER0.LBX', None)
        IMAGES['INFO_SCREEN']['reference_off'] = self.load_image('INFO.LBX', 7, 0, 'BUFFER0.LBX', None)

        IMAGES['APP_PICS'] = {}
#	PALETTES['APP_PICS.LBX'][176] = {'alpha': 1, 'rgb': 0x000c00}	# 686034 -> 000c00
#	PALETTES['APP_PICS.LBX'][177] = {'alpha': 1, 'rgb': 0x081c08}	# 787040 -> 081c08
#	PALETTES['APP_PICS.LBX'][179] = {'alpha': 1, 'rgb': 0x084408}	# b4ac78 -> 084408
#	PALETTES['APP_PICS.LBX'][180] = {'alpha': 1, 'rgb': 0x084408}	# b4ac78 -> 084408
#	PALETTES['APP_PICS.LBX'][181] = {'alpha': 1, 'rgb': 0x085008}	# c8c48c -> 085008

        self.set_palette_color('BUFFER0.LBX', 176, {'alpha': 1, 'rgb': 0x000c00})	# 686034 -> 000c00
        self.set_palette_color('BUFFER0.LBX', 177, {'alpha': 1, 'rgb': 0x081c08})	# 787040 -> 081c08
        self.set_palette_color('BUFFER0.LBX', 179, {'alpha': 1, 'rgb': 0x084408})	# b4ac78 -> 084408
        self.set_palette_color('BUFFER0.LBX', 180, {'alpha': 1, 'rgb': 0x084408})	# b4ac78 -> 084408
        self.set_palette_color('BUFFER0.LBX', 181, {'alpha': 1, 'rgb': 0x085008})	# c8c48c -> 085008

        IMAGES['RESEARCH_DIALOG'] = {}
        IMAGES['RESEARCH_DIALOG']['panel'] = self.load_image('TECHSEL.LBX', 0, 0, 'BUFFER0.LBX', None)

        IMAGES['COLONY_BUILD_SCREEN'] = {}
        IMAGES['COLONY_BUILD_SCREEN']['screen'] = self.load_image('COLBLDG.LBX', 0, 0, 'COLBLDG.LBX', None)

        IMAGES['PLANETS_SCREEN'] = {}
        IMAGES['PLANETS_SCREEN']['screen'] = self.load_image('PLNTSUM.LBX', 0, 0, 'BUFFER0.LBX', None)

        for i in range(212):
            if i == 0:
                IMAGES['APP_PICS'][i] = self.load_image('APP_PICS.LBX', i, 0, 'APP_PICS.LBX', None)
            elif i == 155:
                IMAGES['APP_PICS'][i] = self.load_image('APP_PICS.LBX', i, 0, 'APP_PICS.LBX', None)
            else:
                IMAGES['APP_PICS'][i] = None

    # /load_graphic

    def get_images(self):
        return self.__images
    # /get_images

    def bordered_text(self, surface, text, color, border, x, y, font):
        surface.blit(font.render(text, 1, border), (x - 1, y))
        surface.blit(font.render(text, 1, border), (x + 1, y))
        surface.blit(font.render(text, 1, border), (x, y - 1))
        surface.blit(font.render(text, 1, border), (x, y + 1))
        surface.blit(font.render(text, 1, color), (x, y))
