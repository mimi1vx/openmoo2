from screen import Screen

class SplashScreen(Screen):

    def __init__(self, ui):
        Screen.__init__(self, ui)

    def draw(self):
        self.get_display().blit(self.get_image('splash_screen'), (0, 0))
        self.flip()

    def run(self):
        self.draw()
