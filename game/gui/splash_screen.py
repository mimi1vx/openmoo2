import screen

import gui

class SplashScreen(screen.Screen):

    def __init__(self):
        screen.Screen.__init__(self)

    def draw(self):
        gui.GUI.get_display().blit(self.get_image('splash_screen'), (0, 0))
        self.flip()

    def run(self):
        self.draw()

Screen = SplashScreen()