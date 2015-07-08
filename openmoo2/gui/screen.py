import time

from pygame.locals import *

import gui

MOUSE_LEFT_BUTTON       = 1
MOUSE_MIDDLE_BUTTON     = 2
MOUSE_RIGHT_BUTTON      = 3
MOUSE_WHEELUP		= 4
MOUSE_WHEELDOWN		= 5

class Screen(object):
    """Base gui screen class
    every game screen class should inherit from this one

    """

    __triggers = []

    __old_hover = None
    __hover = None
    __hover_changed = False

    def __init__(self):
        pass


    def log_info(self, message):
        """Prints an INFO message to standard output"""
        ts = int(time.time())
        print("# INFO %i ... %s" % (ts, message))

    def log_error(self, message):
        """Prints an ERROR message to standard output"""
        ts = int(time.time())
        print("! ERROR %i ... %s" % (ts, message))


    def reset_triggers_list(self):
        """Clears the screen's trigger list"""
        self.__triggers = []

    def add_trigger(self, trigger):
        """Appends given trigger to the end of screen's trigger list"""
        if not trigger.has_key('hover_id'):
            trigger['hover_id'] = None
        self.__triggers.append(trigger)

    def list_triggers(self):
        """Returns the screen's list of triggers"""
        return self.__triggers


    def get_timestamp(self, zoom = 1):
        """Returns an actual timestamp"""
        return int(time.time() * zoom)


    def get_image(self, img_key, subkey1 = None, subkey2 = None, subkey3 = None):
        """Returns an image object from GUI engine, identified by its key(s)"""
        return gui.GUI.get_image(img_key, subkey1, subkey2, subkey3)


    def redraw_flip(self):
        """Redraws the screen, takes care about mouse cursor and flips the graphic buffer to display"""
        self.draw()
        gui.GUI.highlight_triggers(self.list_triggers())
        gui.GUI.flip()

    def redraw_noflip(self):
        """Redraws the screen, takes care about mouse cursor but doesn't flip the buffer to display"""
        self.draw()
        gui.GUI.highlight_triggers(self.list_triggers())


    def prepare(self):
        """This method should be implemented by screens that require some
        special actions each time before the screen is run.

        For example to reset screen to a well known state to prevent unexpected behaviour.

        """
        pass

    def draw(self):
        """All static graphic output should be implemented in this method.

        Unless there is only a dynamic graphic (animations),
        every screen should implement this method.

        """
        pass

    def animate(self):
        """Entry point for Screen animations, e.g. ship trajectory on MainScreen.

        GUI engine calls this method periodically
        Animations should be time-dependant - such screens have to implement the timing!

        """
        pass


    def get_escape_trigger(self):
        """Returns standard trigger for sending escape action"""
        return {'action': "ESCAPE"}


    def on_mousebuttonup(self, event):
        """Default implementation of mouse click event serving.
        
        Checks the mouse wheel events (up and down scrolling) and regular mouse buttons.
        If the event's subject is the left mouse button it checks the mouse position against the trigger list and
        returns the first trigger where mouse positions is within its rectangle.

        There is a good chance that no screen would have to override this method.
        
        """
        if event.button == MOUSE_MIDDLE_BUTTON:
            print event

        elif event.button == MOUSE_WHEELUP:
            return {'action': "SCROLL_UP"}

        elif event.button == MOUSE_WHEELDOWN:
            return {'action': "SCROLL_DOWN"}

        else:
            triggers_list = self.list_triggers()
            for trigger in triggers_list:
                if trigger['rect'].collidepoint(event.pos):
                    if event.button == MOUSE_LEFT_BUTTON:
                        trigger['mouse_pos'] = event.pos
                        return trigger

                    elif event.button == MOUSE_RIGHT_BUTTON:
                        return {'action': "help", 'help': trigger['action']}
        

    def on_keydown(self, event):
        """Default implementation of a keyboard event handling.
        
        If keypress is detected by a GUI engine it calls this method.
        The pressed key is checked against the trigger list.
        Returns the first trigger where the key matches the pressed or
        None if no trigger matches the keypress

        There is a good chance that no screen would have to override this method.

        """
        print("@ screen.Screen::on_keydown()")
        print("    scancode = %i" % event.scancode)
        print("    key = %i" % event.key)
        if event.key == K_ESCAPE:
            return {'action': "ESCAPE"}
        else:
            triggers_list = self.list_triggers()
            for trigger in triggers_list:
                if trigger.has_key('key') and trigger['key'] == event.key:
                    return trigger
            return {'action': "key", 'key': event.key}


    def update_hover(self, mouse_pos):
        """This method is invoked by a GUI engine on every pure mouse move
        and right before the screen's on_mousemotion() method.

        Mouse position is checked against screen's trigger list.
        If hover is detected (=mouse position is inside the trigger's rectangle)
        the trigger is copied and can be returned by get_hover() method

        Also if the previously stored value is different than the new one,
        the __hover_changed flag is set to True

        The idea is to handle mouse hover detection separately,
        so other methods could rely on get_hover() and hover_changed() methods.
        
        Probably no screen should require to override this method.
        
        """
	for trigger in self.list_triggers():
            if trigger.has_key('hover_id') and trigger['rect'].collidepoint(mouse_pos):
                if self.__hover != trigger:
                    self.__hover_changed = True
                self.__hover = trigger
                break

    def get_hover(self):
        """Returns the current hover trigger"""
        return self.__hover

    def hover_changed(self):
        """Returns True if screen's hover has changed since last call of this method"""
        if self.__hover_changed:
            self.__hover_changed = False
            return True
        else:
            return False


    def on_mousemotion(self, event):
        """Invoked by a GUI engine on every pure (non-dragging) mouse move.

        Currently no screen requires to override this empty implementation.

        """
        pass

    def get_drag_item(self, mouse_pos):
        """"""
        for trigger in self.list_triggers():
            if trigger.has_key('drag_id') and trigger['rect'].collidepoint(mouse_pos):
                return trigger['drag_id']
        return None

    def on_mousedrag(self, drag_item, pos, rel):
        """Invoked by a GUI engine when left mouse button is being held, drag item is set and mouse moves"""
        pass

    def on_mousedrop(self, drag_item, (mouse_x, mouse_y)):
        """Invoked by a GUI engine when mouse dragging stops
        (drag item was set and left mouse button was released).

        """
        pass

    def process_trigger(self, trigger):
        """Empty implementation of a trigger handling

        If a screen trigger is positively evaluated
        (e.g. returned from on_mousebuttonup() or on_keydown() methods)
        it's passed as a trigger argument to this method

        Every screen should override this method to handle the proper actions.

        """
        pass

    def enter(self):
        """ Called by GUI engine right before gui_client::run_screen() is invoked
        Suitable for saving initial state that can be reveresed by the screen's cancel() method

        """
        pass

    def leave_confirm(self):
        """ Called by GUI engine when CONFIRM trigger is activated
        Every screen that sends data to the game server should implement this method

        """
        pass

    def leave_cancel(self):
        """ Called by GUI engine when ESCAPE trigger is activated
            This is the right place to implement things like getting the screen to state before any changes were made
        """
        pass
