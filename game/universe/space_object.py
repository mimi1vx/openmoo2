from game_object import GameObject

class SpaceObject(GameObject):

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_coords(self, x, y):
        self.__x, self.__y = x, y

    def get_coords(self):
        return (self.__x, self.__y)
