import pygame
import os
import hashlib

DEBUG	= 0

#COLORKEY = (253, 254, 255)
COLORKEY = (0xdf, 0x32, 0xef)



def read_byte(data, offset):
    """returns 1 byte on given offset"""
    return ord(data[offset])
# /read_byte

def read_signed_byte(data, offset):
    """returns 1-byte signed integer on given offset"""
    v = ord(data[offset])
    if v > 0x7f:
        v -= 0x100
    return v
# /read_signed_byte

def read_char(buffer, offset):
    return ord(buffer[offset])
# /read_char

def read_short_int(data, offset):
    """returns 2-byte unsigned integer on given offset"""
    return ord(data[offset]) + (ord(data[offset+1]) << 8)
# /read_short_int

def read_signed_short_int(data, offset):
    """returns 2-byte unsigned integer on given offset"""
    si = ord(data[offset]) + (ord(data[offset+1]) << 8)
    if si > 0x7fff:
        return si - 0x10000
    else:
        return si
# /read_short_int

def read_long_int(data, offset):
        """returns 4-byte unsigned integer on given offset"""
        return ord(data[offset]) + (ord(data[offset+1]) << 8) + (ord(data[offset+2]) << 16) + (ord(data[offset+3]) << 24)
# /read_long_int

def read_string(data, offset, length):
    """returns string on given offset"""
    return data[offset:offset + length].rstrip(chr(0) + chr(1) + chr(2) + chr(3)).split(chr(0))[0]
# /read_string


def debug_output(s):
    print(s)

#def moo2_draw_image_frame(surface, picture, frame, globalPalette, x=0, y=0):
def moo2_draw_image_frame(surface, picture, frame, localPalette, x=0, y=0, DEBUG = None):
#    localPalette = []
#    debug_output("	Drawing frame #%i (frame offset is 0x%x)" % (frame, picture['offsets'][frame]))
#    print "* globalPalette: " + str(globalPalette)
#    print "globalPalette ID: " + str(id(globalPalette))
#    localPalette = copy.deepcopy(globalPalette)
#    localPalette = globalPalette[:]
#    localPalette = globalPalette
#    print "localPalette ID: " + str(id(localPalette))
#    print
#    print "* localPalette: " + str(localPalette)
#    print "tested palette ... before applycation of local palette: " + str(localPalette)
#    print "tested palette ... before applycation of local palette: " + str(localPalette)
#    return
#    print picture['palette'][1]

# dump set the black color as transparent, let's see if it will break something :-O

    px = pygame.PixelArray(surface)

    pos = 12 + (len(picture['offsets']) << 2)	# offset * 4

    if picture['f_junction']:
        debug_output("		TODO: junction")

    if picture['f_functional_color']:
        debug_output("		TODO: functional color")

    if picture['f_fill_background']:
        # FIXME: COLORKEY is hardcoded, should be determined somehow?
        surface.fill(COLORKEY)
        surface.set_colorkey(COLORKEY)
        
    if picture['f_no_compression']:
        debug_output("		TODO: no compression")

    if picture['f_internal_palete']:
#        debug_output("		Image has local palette")
        colorShift = ord(picture['data'][pos]) + (ord(picture['data'][pos+1]) << 8)
        pos += 2
        localColors = ord(picture['data'][pos]) + (ord(picture['data'][pos+1]) << 8)
        pos += 2
#        debug_output("		Local palette shift: " + str(colorShift))
#        debug_output("		Local palette colors: " + str(localColors))
        for i in range(localColors):
            a = ord(picture['data'][pos])
            r = ord(picture['data'][pos+1]) * 4
            g = ord(picture['data'][pos+2]) * 4
            b = ord(picture['data'][pos+3]) * 4
#            debug_output("* localPalette COLOR BEFORE update: " + str(localPalette[colorShift + i]))
#            debug_output("* globalPalette COLOR BEFORE update: " + str(globalPalette[colorShift + i]))
            localPalette[colorShift + i]['alpha'] = a
            localPalette[colorShift + i]['rgb'] = (r << 16) + (g << 8) + b
#            debug_output("* localPalette [%i] COLOR AFTER update: %s" % (i, str(localPalette[colorShift + i])))
#            debug_output("* globalPalette [%i] COLOR AFTER: %s" % (i, str(globalPalette[colorShift + i])))
            pos += 4
#        debug_output()
#        debug_output("* localPalette UPDATED: " + str(localPalette))
#        debug_output("* globalPalette: " + str(globalPalette))
    X = x
    pos = picture['offsets'][frame]
    if (ord(picture['data'][pos]) == 1) and (ord(picture['data'][pos+1]) == 0):
#		print "heading 0x01 0x00 looks ok"
        pos += 2
        startY = ord(picture['data'][pos]) + (ord(picture['data'][pos+1]) << 8)
#		print "startY: " + str(startY)
        Y = y + startY
        pos += 2
        while pos < picture['offsets'][frame+1]:
            pixelCount = ord(picture['data'][pos]) + (ord(picture['data'][pos+1]) << 8)
#	    print "pixelCount: %i" % pixelCount
#	    if pixelCount == 1:
#		print "color at [0,0] %i" % px[0][0]
            pos += 2
#			print "pixelCount: " + str(pixelCount)
            if pixelCount > 0:
                xIndent = ord(picture['data'][pos]) + (ord(picture['data'][pos+1]) << 8)
                X += xIndent
                pos += 2
#				print "xIndent: " + str(xIndent)
                for i in range(pixelCount):
                    pixel = ord(picture['data'][pos])
#		    if localPalette[pixel]['alpha']:
#                	px[X][Y] = localPalette[pixel]['rgb']
#                	pixel = ord(picture['data'][pos])
#			print "		got alpha: %i" % localPalette[pixel]['alpha']
#		    else:
            	    px[X][Y] = localPalette[pixel]['rgb']
#                	pixel = ord(picture['data'][pos])
            	    pos += 1
# put-pixel onto surface
#                    px[X][Y] = localPalette[pixel]['rgb']
                    X += 1
                if (pixelCount % 2) == 1:
                    pos += 1
#				print
            else:
                yIndent = ord(picture['data'][pos]) + (ord(picture['data'][pos+1]) << 8)
                pos += 2
                if yIndent != 1000:
                    Y += yIndent
                    X = x
                else:
#					pygame.display.flip()
#					pos = 999999999
#                    print
                    return

# end func moo2_draw_image_frame

def load_surface(picture, picture_frame, local_palette, colorkey = None):
#    debug_output("@ load_surface")
#    debug_output("	lbx_source_filename: %s" % lbx_source_filename)
#    debug_output("	lbx_file_index: %i" % lbx_file_index)
#    debug_output("	picture_frame: %i" % picture_frame)
#    debug_output("	colorkey: %s" % colorkey)
#    debug_output("")
    """
    """

    surface = pygame.Surface((picture['width'], picture['height']))
#    if lbx_source_filename == "APP_PICS.LBX":
#	moo2_draw_image_frame(surface, picture, picture_frame, local_palette, 0, 0, True)
#	moo2_draw_image_frame(surface, picture, picture_frame, local_palette)
#    else:
#	moo2_draw_image_frame(surface, picture, picture_frame, local_palette)
    moo2_draw_image_frame(surface, picture, picture_frame, local_palette)
    if colorkey is not None:
#	print("	setting colorkey!")
        surface.set_colorkey(colorkey)
    return surface
# end func load_surface


class Archive():

#    __filename = None
#    __filesize = 0
#    __version = None

#    __info = None

#    __files_info = None

    def __init__(self, filename, md5sum = ""):
#        print("lbx::Archive::__init__() ... MD5 = %s ... filename = %s" % (md5sum, filename))
        self.__filename = filename
        self.__filesize = os.path.getsize(filename)
        self.__file = None
        self.open()
        self.__md5_expected = md5sum
        self.__count_md5_hexdigest()
        self.__load_info()

    def get_filename(self):
        return self.__filename

    def open(self):
        if self.__file is None:
            self.__file = open(self.__filename, 'rb')

    def close(self):
        if self.__file:
            self.__file.close()
            self.__file = None

    def __count_md5_hexdigest(self):
        checksum = hashlib.md5()
        for one_line in self.__file.readlines():
            checksum.update(one_line)
        self.__md5_real = str(checksum.hexdigest())

    def md5_hexdigest(self):
        return self.__md5_real

    def md5_hexdigest_expected(self):
        return self.__md5_expected

    def check_md5(self):
        return self.__md5_expected == self.__md5_real

    def read(self, n):
        return self.__file.read(n)

    def seek(self, offset):
        return self.__file.seek(offset)

    def __read_int_2b_le(self):
        """reads 2-byte little-endian integer"""
        n = self.read(2)
        return ord(n[0]) + (ord(n[1]) << 8)

    def __read_int_4b_le(self):
        """reads 4-byte little-endian integer"""
        n = self.read(4)
        return ord(n[0]) + (ord(n[1]) << 8) + (ord(n[2]) << 16) + (ord(n[3]) << 24)

    def check_lbx_signature(self, signature):
        """returns True if the given string is a correct LBX signature"""
        return signature == "\xAD\xFE\x00\x00"

    def __load_info(self):
        """loads archived files descriptors"""
        self.seek(0)
        n = self.__read_int_2b_le()
        if self.check_lbx_signature(self.read(4)):
#                print "good signature"
                self.__version = self.read(2)

            	self.__info = []
                off2 = self.__read_int_4b_le()
                for i in range(n):
                        off1 = off2
                        if i == (n):
                                off2 = filesize
                        else:
                                off2 = self.__read_int_4b_le()
                        size = off2 - off1
                        self.__info.append({'size': size, 'offset': off1})
                return True
        else:
#                print "bad signature"
                return False

    def get_info(self):
        """returns archived files descriptors"""
        return self.__info

    def has_file(self, i):
#        print "LbxArchive::has_file ... i = " + str(i)
        return (i >= 0) and (i <= len(self.__info))

    def get_file_info(self, i):
        if self.has_file(i):
            return self.__info[i]
        else:
            return None

    def read_file(self, i):
        f_info = self.get_file_info(i)
        if not f_info:
            return None
        else:
            self.seek(f_info['offset'])
            return self.read(f_info['size'])

    def read_picture(self, i):
        data = self.read_file(i)
        if not data:
            return None
        else:
            flags = ord(data[10]) + (ord(data[11]) << 8)
            picture = {
                'width':                ord(data[0]) + (ord(data[1]) << 8),
                'height':               ord(data[2]) + (ord(data[3]) << 8),
                'frames':               ord(data[6]) + (ord(data[7]) << 8),
                'frame_delay':          ord(data[8]) + (ord(data[9]) << 8),
                'flags':                flags,
                'flags_hex':            hex(flags),
                'f_junction':           flags & 8192,
                'f_internal_palete':    flags & 4096,
                'f_functional_color':   flags & 2048,
                'f_fill_background':    flags & 1024,
                'f_no_compression':     flags & 256,
                'offsets':              [],
                'data':                 data
            }

            for i in range(picture['frames'] + 1):
                    ii = 12 + (i * 4)
                    picture['offsets'].append(ord(data[ii]) + (ord(data[ii+1]) << 8) + (ord(data[ii+2]) << 16) + (ord(data[ii+3]) << 24))

            return picture

    def load_surface(self, picture, frame, local_palette, color_key):
        return load_surface(picture, frame, local_palette, color_key)

    def get_surface(self, picture_id, picture_frame, local_palette, color_key = None):
        return self.load_surface(self.read_picture(picture_id), picture_frame, local_palette, color_key)

    def read_palette(self, i):
        data = self.read_file(i)
        if not data:
            return None
        else:
            palette = []
            for i in range(256):
                a = ord(data[i*4])
                r = ord(data[(i*4)+1]) * 4
                g = ord(data[(i*4)+2]) * 4
                b = ord(data[(i*4)+3]) * 4
                palette.append({
                    'alpha': a,
                    'rgb': (r << 16) + (g << 8) + b
                })
            return palette

    def read_palette2(self, i):
        data = self.read_file(i)
        if not data:
            return None
        else:
            palette = []
            for i in range(256):
                o = i << 2
                a = ord(data[o])
                r = ord(data[o + 1]) << 2
                g = ord(data[o + 2]) << 2
                b = ord(data[o + 3]) << 2
                palette.append({
                    'alpha': a,
                    'rgb': (r << 16) + (g << 8) + b
                })
            return palette

# end class Archive
