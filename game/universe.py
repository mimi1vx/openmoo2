# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="peterman"
__date__ ="$May 15, 2010 12:52:51 PM$"

if __name__ == "__main__":
    print "Hello World";

class GameObject():

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

class SpaceObject(GameObject):

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y