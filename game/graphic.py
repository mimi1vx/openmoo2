import copy
import lbx

class Gui():

    def __init__(self, pg):
        self.__pygame = pg
        self.__images = {}

    def init(self):
        self.__pygame.init()
        self.__pygame.display.set_mode((640, 480), 0, 24)

    def get_display(self):
        return self.__pygame.display.get_surface()

    def flip(self):
        self.__pygame.display.flip()

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
            'DIPLOMAT.LBX':     lbx.Archive("%s/DIPLOMAT.LBX" % moo2_dir, "1e8c0a90e8836d9cc83e4614ece8011d"),
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
            'TECHSEL.LBX':      lbx.Archive("%s/TECHSEL.LBX" % moo2_dir, "db472e2a7f8185536a21db6e9c73a7a5"),
            'TEXTBOX.LBX':      lbx.Archive("%s/TEXTBOX.LBX" % moo2_dir, "5f50e2cbdcbe89ad084be2024477f9c5")
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

    def load_fonts(self):
        self.__fonts = {
            'font1':  self.__lbx['FONTS.LBX'].read_font(0),
            'font2':  self.__lbx['FONTS.LBX'].read_font(1),
            'font3':  self.__lbx['FONTS.LBX'].read_font(2),
            'font4':  self.__lbx['FONTS.LBX'].read_font(3),
            'font5':  self.__lbx['FONTS.LBX'].read_font(4),
            'font6':  self.__lbx['FONTS.LBX'].read_font(5)
        }

    def get_all_fonts(self):
        return self.__fonts

    def get_font(self, font_id):
        return self.__fonts[font_id]

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

    def get_raw_palettes(self):
        return self.__raw_palettes
    
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
    
    def set_palette_color(self, palette_key, color_num, color_def):
        self.__palettes[palette_key][color_num] = color_def
    
    def get_palettes(self):
        return self.__palettes

    def __get_img_key(self, img_key, subkey1 = None, subkey2 = None, subkey3 = None):
        for subkey in [subkey1, subkey2, subkey3]:
            if subkey:
                img_key += ":%s" % subkey
            else:
                break
        return img_key

    def set_image(self, image_data, img_key, subkey1 = None, subkey2 = None, subkey3 = None):
        self.__images[self.__get_img_key(img_key, subkey1, subkey2, subkey3)] = image_data

    def get_image(self, img_key, subkey1 = None, subkey2 = None, subkey3 = None):
        return self.__images[self.__get_img_key(img_key, subkey1, subkey2, subkey3)]

    def has_image(self, img_key, subkey1 = None, subkey2 = None, subkey3 = None):
        return self.__images.has_key(self.__get_img_key(img_key, subkey1, subkey2, subkey3))

    def load_solid_image(self, lbx_key, picture_id, palette_key, img_key , subkey1 = None, subkey2 = None, subkey3 = None):
        self.set_image(self.__lbx[lbx_key].get_surface(picture_id, 0, self.__palettes[palette_key], None), img_key, subkey1, subkey2, subkey3)

    def load_transparent_image(self, lbx_key, picture_id, palette_key, color_key, img_key , subkey1 = None, subkey2 = None, subkey3 = None):
        self.set_image(self.__lbx[lbx_key].get_surface(picture_id, 0, self.__palettes[palette_key], color_key), img_key, subkey1, subkey2, subkey3)

    def get_planet_background(self, terrain_id, picture_index):
        bg_pics = [0, 3, 6, 9, 12, 15, 18, 23, 24, 27]
        img_index = bg_pics[terrain_id] + picture_index
        if not self.has_image('background', 'planet_terrain', img_index):
            self.load_transparent_image('PLANETS.LBX', img_index, 'PLANETS.LBX', 0x0, 'background', 'planet_terrain', img_index)
        return self.get_image('background', 'planet_terrain', img_index)

    def get_planet_scheme(self, terrain, size):
        return self.__images['planet_schemes'][terrain][size]

    def load_graphic(self):
        IMAGES = self.__images

        self.load_solid_image('MAINMENU.LBX', 0, 'MAINMENU.LBX', 'splash_screen')

        self.load_solid_image('COLONY2.LBX', 49, 'COLONY2.LBX', 'background', 'starfield')
        self.load_transparent_image('BUFFER0.LBX', 0, 'BUFFER0.LBX', 0x00, 'main_screen', 'panel')
        self.load_solid_image('OFFICER.LBX', 0, 'BUFFER0.LBX', 'leaders_screen', 'panel')

        self.load_solid_image('BUFFER0.LBX', 3, 'BUFFER0.LBX', 'main_screen', 'button', 'left3')
        self.load_solid_image('BUFFER0.LBX', 6, 'BUFFER0.LBX', 'main_screen', 'button', 'zoom_in')
        self.load_solid_image('BUFFER0.LBX', 7, 'BUFFER0.LBX', 'main_screen', 'button', 'zoom_out')
        self.load_solid_image('BUFFER0.LBX', 12, 'BUFFER0.LBX', 'main_screen', 'button', 'turn_hover')

        self.load_solid_image('COLSUM.LBX', 0, 'COLSUM.LBX', 'colonies_screen', 'panel')

        #	star map
        for star_class in range(7):
            for star_size in range(6):
                pic = 148 + (6 * star_class) + (5 - star_size)
                self.load_solid_image('BUFFER0.LBX', pic, 'BUFFER0.LBX', 'star_icon', star_class, star_size)

        self.load_transparent_image('BUFFER0.LBX', 73, 'BUFFER0.LBX', 0x00, 'starsystem_map', 'panel')

        for i in range(5):
            self.load_transparent_image('BUFFER0.LBX', 77 + i, 'BUFFER0.LBX', 0x00, 'starsystem_map', 'orbit', i)

        for i in range(1):
            self.load_transparent_image('BUFFER0.LBX', 91 + i, 'BUFFER0.LBX', lbx.COLORKEY, 'starsystem_map', 'asteroids', i)

        for i in range(6):
            self.load_transparent_image('BUFFER0.LBX', 83 + i, 'BUFFER0.LBX', 0x00, 'starsystem_map', 'star', i)
        self.load_transparent_image('BUFFER0.LBX', 184 , 'BUFFER0.LBX', 0x00, 'starsystem_map', 'star', 6)

        for terrain in range(10):
            for size in range(5):
                self.load_solid_image('BUFFER0.LBX', (92 + (5 * terrain) + size), 'BUFFER0.LBX', 'starsystem_map', 'planet', terrain, size)

        for size in range(5):
            self.load_solid_image('BUFFER0.LBX', 142, 'BUFFER0.LBX', 'starsystem_map', 'gas_giant', size)

        for color in range(8):
            self.load_transparent_image('BUFFER0.LBX', 35 + color, 'BUFFER0.LBX', 0x00, 'starsystem_map', 'colony_mark', color)
            self.load_transparent_image('BUFFER0.LBX', 43 + color, 'BUFFER0.LBX', 0x00, 'starsystem_map', 'outpost_mark', color)

        #	COLONY VIEW

        self.load_solid_image('COLPUPS.LBX', 5, 'COLPUPS.LBX', 'colony_screen', 'panel')
        self.load_transparent_image('COLSYSDI.LBX', 64, 'COLSYSDI.LBX', 0x00, 'colony_screen', 'scheme_arrow')

        for terrain in range(10):
            for size in range(5):
                self.load_solid_image('COLSYSDI.LBX', 11 + (5 * terrain) + size, 'COLSYSDI.LBX', 'planet_scheme',terrain , size)

        self.load_transparent_image('COLSYSDI.LBX', 61, 'COLSYSDI.LBX', 0x00, 'colony_screen', 'gasgiant_scheme')
        self.load_transparent_image('COLSYSDI.LBX', 63, 'COLSYSDI.LBX', 0x00, 'colony_screen', 'asteroids_scheme')

        for picture in range(13):
            for icon in range(13):
                self.load_transparent_image('RACEICON.LBX', (picture * 13) + icon, 'RACEICON.LBX', 0x00, 'race_icon', picture, icon)

        self.load_transparent_image('COLONY2.LBX', 0, 'COLONY2.LBX', 0x00, 'production_1food')
        self.load_transparent_image('COLONY2.LBX', 1, 'COLONY2.LBX', 0x00, 'production_1industry')
        self.load_transparent_image('COLONY2.LBX', 2, 'COLONY2.LBX', 0x00, 'production_1research')
        self.load_transparent_image('COLONY2.LBX', 3, 'COLONY2.LBX', 0x00, 'production_1money')

        self.load_transparent_image('COLONY2.LBX', 4, 'COLONY2.LBX', 0x00, 'production_10food')
        self.load_transparent_image('COLONY2.LBX', 5, 'COLONY2.LBX', 0x00, 'production_10industry')
        self.load_transparent_image('COLONY2.LBX', 6, 'COLONY2.LBX', 0x00, 'production_10research')
        self.load_transparent_image('COLONY2.LBX', 3, 'COLONY2.LBX', 0x00, 'production_10money')

        self.load_solid_image('OFFICER.LBX', 3, 'BUFFER0.LBX', 'leaders_screen', 'colony_leaders_button')
        self.load_solid_image('OFFICER.LBX', 3, 'BUFFER0.LBX', 'leaders_screen', 'ship_officers_button')

        for leader_id in range(67):
            self.load_solid_image('OFFICER.LBX', 21 + leader_id, 'BUFFER0.LBX', 'leader', 'face', leader_id)

        self.load_solid_image('OFFICER.LBX', 88, 'BUFFER0.LBX', 'leader', 'skill_icon', 'assassin')
        self.load_solid_image('OFFICER.LBX', 89, 'BUFFER0.LBX', 'leader', 'skill_icon', 'commando')
        self.load_solid_image('OFFICER.LBX', 90, 'BUFFER0.LBX', 'leader', 'skill_icon', 'diplomat')
        self.load_solid_image('OFFICER.LBX', 91, 'BUFFER0.LBX', 'leader', 'skill_icon', '91')
        self.load_solid_image('OFFICER.LBX', 92, 'BUFFER0.LBX', 'leader', 'skill_icon', '92')
        self.load_solid_image('OFFICER.LBX', 93, 'BUFFER0.LBX', 'leader', 'skill_icon', 'famous')
        self.load_solid_image('OFFICER.LBX', 94, 'BUFFER0.LBX', 'leader', 'skill_icon', 'farmer')
        self.load_solid_image('OFFICER.LBX', 95, 'BUFFER0.LBX', 'leader', 'skill_icon', 'fighter_pilot')
        self.load_solid_image('OFFICER.LBX', 96, 'BUFFER0.LBX', 'leader', 'skill_icon', 'financial_leader')
        self.load_solid_image('OFFICER.LBX', 97, 'BUFFER0.LBX', 'leader', 'skill_icon', 'galactic_role')
        self.load_solid_image('OFFICER.LBX', 98, 'BUFFER0.LBX', 'leader', 'skill_icon', 'helmsman')
        self.load_solid_image('OFFICER.LBX', 99, 'BUFFER0.LBX', 'leader', 'skill_icon', 'instructor')
        self.load_solid_image('OFFICER.LBX', 100, 'BUFFER0.LBX', 'leader', 'skill_icon', 'labor_leader')
        self.load_solid_image('OFFICER.LBX', 101, 'BUFFER0.LBX', 'leader', 'skill_icon', 'medicine')
        self.load_solid_image('OFFICER.LBX', 102, 'BUFFER0.LBX', 'leader', 'skill_icon', 'megawealth')
        self.load_solid_image('OFFICER.LBX', 103, 'BUFFER0.LBX', 'leader', 'skill_icon', 'navigator')
        self.load_solid_image('OFFICER.LBX', 104, 'BUFFER0.LBX', 'leader', 'skill_icon', 'operations')
        self.load_solid_image('OFFICER.LBX', 105, 'BUFFER0.LBX', 'leader', 'skill_icon', 'ordnance')
        self.load_solid_image('OFFICER.LBX', 106, 'BUFFER0.LBX', 'leader', 'skill_icon', 'researcher')
        self.load_solid_image('OFFICER.LBX', 107, 'BUFFER0.LBX', 'leader', 'skill_icon', 'science_leader')
        self.load_solid_image('OFFICER.LBX', 108, 'BUFFER0.LBX', 'leader', 'skill_icon', '108')
        self.load_solid_image('OFFICER.LBX', 109, 'BUFFER0.LBX', 'leader', 'skill_icon', 'spiritual_leader')
        self.load_solid_image('OFFICER.LBX', 110, 'BUFFER0.LBX', 'leader', 'skill_icon', 'spy_master')
        self.load_solid_image('OFFICER.LBX', 111, 'BUFFER0.LBX', 'leader', 'skill_icon', 'tactics')
        self.load_solid_image('OFFICER.LBX', 112, 'BUFFER0.LBX', 'leader', 'skill_icon', 'telepath')
        self.load_solid_image('OFFICER.LBX', 113, 'BUFFER0.LBX', 'leader', 'skill_icon', 'trader')
        self.load_solid_image('OFFICER.LBX', 114, 'BUFFER0.LBX', 'leader', 'skill_icon', 'weaponry')

        for c in range(9):
            for i in range(4):
                self.load_solid_image('BUFFER0.LBX', 205 + (c * 4 + i), 'BUFFER0.LBX', 'main_screen', 'ship_icon', c, i)

        for c in range(9, 14):
            for i in range(4):
                self.load_solid_image('BUFFER0.LBX', 205 + (c * 4 + (3 - i)), 'BUFFER0.LBX', 'main_screen', 'ship_icon', c, i)

        for gov_id in range(8):
            self.load_transparent_image('COLONY2.LBX', 19 + gov_id, 'COLONY2.LBX', 0x00, 'government', 'icon', gov_id)

        self.load_transparent_image('COLONY2.LBX', 16, 'COLONY2.LBX', 0x00, 'morale_icon', 'good')
        self.load_transparent_image('COLONY2.LBX', 17, 'COLONY2.LBX', 0x00, 'morale_icon', 'bad')

#        IMAGES['GAME_MENU'] = {}
#        IMAGES['GAME_MENU']['main'] = self.load_solid_image('GAME.LBX', 0, 'GAME.LBX')

#        IMAGES['GAME_MENU']['settings'] = self.load_solid_image('GAME.LBX', 29, 'GAME.LBX')
#        IMAGES['GAME_MENU']['settings1'] = self.load_solid_image('GAME.LBX', 31, 'GAME.LBX')
#        IMAGES['GAME_MENU']['settings2'] = self.load_solid_image('GAME.LBX', 8, 'GAME.LBX')
#        IMAGES['GAME_MENU']['settings3'] = self.load_solid_image('GAME.LBX', 30, 'GAME.LBX')

#        IMAGES['GAME_MENU']['load_game'] = self.load_solid_image('GAME.LBX', 11, 'GAME.LBX')
#        IMAGES['GAME_MENU']['save_game'] = self.load_solid_image('GAME.LBX', 14, 'GAME.LBX')

        # main palette debug
#	i = 0
#	for color in PALETTES['BUFFER0.LBX']:
#	    print "%i ... %s" % (i, color)
#	    i += 1

        self.set_palette_color('BUFFER0.LBX', 32, {'alpha': 1, 'rgb': 0xECECEC})	# 000c10 -> ececec
        self.set_palette_color('BUFFER0.LBX', 33, {'alpha': 1, 'rgb': 0xF4F4F4})	# 00141c -> f4f4f4
        self.set_palette_color('BUFFER0.LBX', 34, {'alpha': 1, 'rgb': 0xFCFCFC})	# 0c2834 -> fcfcfc
        self.set_palette_color('BUFFER0.LBX', 45, {'alpha': 1, 'rgb': 0xECECEC})	# 200c10 -> ac9c94
        self.set_palette_color('BUFFER0.LBX', 108, {'alpha': 1, 'rgb': 0xECECEC})	# f4e094 -> 000818
        self.set_palette_color('BUFFER0.LBX', 109, {'alpha': 1, 'rgb': 0xECECEC})	# fcecb0 -> 000818

        self.load_solid_image('INFO.LBX', 0, 'BUFFER0.LBX', 'info_screen', 'panel')
        self.load_solid_image('INFO.LBX', 2, 'BUFFER0.LBX', 'info_screen', 'button', 'return')
        self.load_solid_image('INFO.LBX', 3, 'BUFFER0.LBX', 'info_screen', 'button', 'history_graph', 'off')
        self.load_solid_image('INFO.LBX', 4, 'BUFFER0.LBX', 'info_screen', 'button', 'tech_review', 'off')
        self.load_solid_image('INFO.LBX', 5, 'BUFFER0.LBX', 'info_screen', 'button', 'race_statistics', 'off')
        self.load_solid_image('INFO.LBX', 6, 'BUFFER0.LBX', 'info_screen', 'button', 'turn_summary', 'off')
        self.load_solid_image('INFO.LBX', 7, 'BUFFER0.LBX', 'info_screen', 'button', 'reference', 'off')

        self.set_palette_color('BUFFER0.LBX', 176, {'alpha': 1, 'rgb': 0x000c00})	# 686034 -> 000c00
        self.set_palette_color('BUFFER0.LBX', 177, {'alpha': 1, 'rgb': 0x081c08})	# 787040 -> 081c08
        self.set_palette_color('BUFFER0.LBX', 179, {'alpha': 1, 'rgb': 0x084408})	# b4ac78 -> 084408
        self.set_palette_color('BUFFER0.LBX', 180, {'alpha': 1, 'rgb': 0x084408})	# b4ac78 -> 084408
        self.set_palette_color('BUFFER0.LBX', 181, {'alpha': 1, 'rgb': 0x085008})	# c8c48c -> 085008

        self.load_solid_image('TECHSEL.LBX', 0, 'BUFFER0.LBX', 'research_screen', 'panel')
        self.load_solid_image('COLBLDG.LBX', 0, 'COLBLDG.LBX', 'colony_build_screen', 'panel')
        self.load_solid_image('PLNTSUM.LBX', 0, 'BUFFER0.LBX', 'planets_screen', 'panel')

        self.load_solid_image('APP_PICS.LBX', 0, 'APP_PICS.LBX', 'app_pic', 0)
        self.load_solid_image('APP_PICS.LBX', 155, 'APP_PICS.LBX', 'app_pic', 155)
        """
        for i in range(212):
            if i == 0:
                self.load_solid_image('APP_PICS.LBX', i, 'APP_PICS.LBX', 'app_pic', i)
            elif i == 155:
                self.load_solid_image('APP_PICS.LBX', i, 'APP_PICS.LBX', 'app_pic', i)
            else:
                IMAGES['APP_PICS'][i] = None
        """

        self.load_transparent_image('DIPLOMAT.LBX', 0, 'COLONY2.LBX', 0x00, 'mouse_cursor', 'default')
        
        self.load_solid_image('TEXTBOX.LBX', 0, 'BUFFER0.LBX', 'text_box', 'top');
        self.load_solid_image('TEXTBOX.LBX', 1, 'BUFFER0.LBX', 'text_box', 'middle');
        self.load_solid_image('TEXTBOX.LBX', 2, 'BUFFER0.LBX', 'text_box', 'bottom');

       