import pygame
import copy

import lbx

from splash_screen import SplashScreen

from main_screen import MainScreen

from starsystem_screen import StarsystemScreen
from colonies_screen import ColoniesScreen
from planets_screen import PlanetsScreen
from leaders_screen import LeadersScreen
from research_screen import ResearchScreen
from colony_screen import ColonyScreen
from colony_build_screen import ColonyBuildScreen
from info_screen import InfoScreen

from fonts_screen import FontsScreen

from input import Input

class Gui(object):

    def __init__(self): pass

    def init(self, moo2_dir):
        self.__images = {}
        self.__moo2_dir = moo2_dir
        pygame.init()
        pygame.display.set_mode((640, 480), 0, 24)
        self.__load_lbx_archives()
        self.__load_fonts()
        self.__load_palettes()
        self.__load_graphic()

    def get_display(self):
        return pygame.display.get_surface()

    def flip(self):
        pygame.display.flip()

    def __read_text_file(self, filename):
        """returns the content of the given text file as a list of strings"""
	fh = open(filename, 'rt')
	content = fh.read().strip().split("\n")
	fh.close()
        return content

    def __load_lbx_archives(self):
        """loads LBX archives listed in lbx.md5 file and checks them for expected MD5 checksum
        returns True if all loaded files match their expected checksum, otherwise returns False"""
        print("Loading LBX archive index")
        self.__lbx = {}
        lbx_md5 = self.__read_text_file("../lbx.md5")
        check = True
        for line in lbx_md5:
            md5, filename = line.split("  ")
            self.__lbx[filename] = lbx.Archive("%s/%s" % (self.__moo2_dir, filename), md5)
            if self.__lbx[filename].check_md5():
                print("    %s  %s ... OK" % (md5, filename))
            else:
                print("    %s  %s ... error" % (md5, filename))
                print("        MD5 sum does not match, actual MD5 sum is %s" % self.__lbx[filename].md5_hexdigest())
                check = False
        print("")
        if check:
            print("    Done")
        else:
            print("    Done with errors:")
            print("    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("    Warning!")
            print("")
            print("    Some LBX files don't match the expected MD5 checksum")
            print("    The OpenMOO2 supports only original LBX files from MOO2 version 1.31")
            print("")
            print("    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        return check

    def __load_fonts(self):
        self.__fonts = {
            'font1':  self.__lbx['FONTS.LBX'].read_font(0),
            'font2':  self.__lbx['FONTS.LBX'].read_font(1),
            'font3':  self.__lbx['FONTS.LBX'].read_font(2),
            'font4':  self.__lbx['FONTS.LBX'].read_font(3),
            'font5':  self.__lbx['FONTS.LBX'].read_font(4),
            'font6':  self.__lbx['FONTS.LBX'].read_font(5)
        }

    def get_font(self, font_id):
        return self.__fonts[font_id]

    def __load_raw_palettes(self):
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

    def __load_palettes(self):
        self.__load_raw_palettes()
        self.__palettes = {
            'APP_PICS':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'BUFFER0':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'COLBLDG':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'COLONY2':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'COLPUPS':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'COLSUM':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'COLSYSDI':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'GAME':         copy.deepcopy(self.__raw_palettes['FONTS_01']),
            'INFO':         copy.deepcopy(self.__raw_palettes['FONTS_01']),
            'MAINMENU':	copy.deepcopy(self.__raw_palettes['FONTS_06']),
            'OFFICER':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'PLANETS':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'RACEICON':	copy.deepcopy(self.__raw_palettes['FONTS_02']),
            'SR_R9_SC':	copy.deepcopy(self.__raw_palettes['FONTS_02'])
        }

    def set_palette_color(self, palette_key, color_num, color_def):
        self.__palettes[palette_key][color_num] = color_def

    def __get_img_key(self, img_key, subkey1 = None, subkey2 = None, subkey3 = None):
        for subkey in [subkey1, subkey2, subkey3]:
            if subkey is not None:
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
#	img_key = self.__get_img_key(img_key, subkey1, subkey2, subkey3).replace(":", ".")
#	print "LOADING: %s = %s | %i | %s" % (img_key, lbx_key, picture_id, palette_key)

    def load_transparent_image(self, lbx_key, picture_id, palette_key, color_key, img_key , subkey1 = None, subkey2 = None, subkey3 = None):
        self.set_image(self.__lbx[lbx_key].get_surface(picture_id, 0, self.__palettes[palette_key], color_key), img_key, subkey1, subkey2, subkey3)
#	img_key = self.__get_img_key(img_key, subkey1, subkey2, subkey3).replace(":", ".")
#	print "LOADING: %s = %s | %i | %s | transparent" % (img_key, lbx_key, picture_id, palette_key)

    def get_planet_background(self, terrain_id, picture_index):
        bg_pics = [0, 3, 6, 9, 12, 15, 18, 23, 24, 27]
        img_index = bg_pics[terrain_id] + picture_index
        if not self.has_image('background', 'planet_terrain', img_index):
            self.load_transparent_image('PLANETS.LBX', img_index, 'PLANETS', 0x0, 'background', 'planet_terrain', img_index)
        return self.get_image('background', 'planet_terrain', img_index)

    def get_planet_scheme(self, terrain, size):
        return self.__images['planet_schemes'][terrain][size]

    def __load_graphic(self):
	print "Loading graphic..."
	graphic_ini = self.__read_text_file("../graphic.ini")
	for line in graphic_ini:

	    if line and line[0] != "#":
		line = line.split("=", 1)
		img_keys = line[0].strip().split(".", 3)
#		print img_keys
		subkey1 = subkey2 = subkey3 = None
		img_key = img_keys.pop(0)
		if len(img_keys):
		    subkey1 = str(img_keys.pop(0))
		if len(img_keys):
		    subkey2 = str(img_keys.pop(0))
		if len(img_keys):
		    subkey3 = str(img_keys.pop(0))
		options = line[1].split("|")
		source_file = options[0].strip()
		source_type = source_file.split(".")[-1].lower()
		# TODO: add support for non-original graphic
		if source_type == "lbx":
		    # original LBX image = source_file | source_index | palette_key | <transparent>
		    source_index = int(options[1].strip())
		    lbx_palette = options[2].strip()
		    lbx_transparent = (len(options) == 4) and (options[3].strip() == "transparent")
		    if lbx_transparent:
			self.load_transparent_image(source_file, source_index, lbx_palette, 0x00, img_key, subkey1, subkey2, subkey3)
		    else:
			self.load_solid_image(source_file, source_index, lbx_palette, img_key, subkey1, subkey2, subkey3)

	print "...Done"


GUI = Gui()
