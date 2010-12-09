import screen

import gui

class SplashScreen(screen.Screen):

    def __init__(self):
        screen.Screen.__init__(self)

    def draw(self):
	gui.GUI.draw_image_by_key('splash_screen', (0, 0))



Screen = SplashScreen()