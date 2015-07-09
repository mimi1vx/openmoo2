# vim: set ts=4 sw=4 et: coding=UTF-8

class Orion(object):
    """
    Main object creating the game up to our likings
    """

    options = None

    def __init__(self, options): 
        self.options = options
        self.moo2_dir = OrionDataLoader.provide_lbx_datadir()

    def start_server(self):
        """
        Run all the operations required to initialize server
        """
        return

    def start_client(self):
        """
        Run all operations to start the client
        """
        return

    def run(self):
        self.start_server()
        if not option.server:
            self.start_client()
