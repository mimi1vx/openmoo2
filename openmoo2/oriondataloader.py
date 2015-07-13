# vim: set ts=4 sw=4 et: coding=UTF-8

import os
from .orionexception import OrionException

class OrionDataLoader(object):
    """
    Class providing interface to load various datafiles
    """

    def __init__(self):
        self.datadir = self.find_datadir()


    def find_datadir(self):
        """
        Determine datadir we want to work with
        """
        datadirs = [
            '{0}/../data'.format(os.path.dirname(os.path.realpath(__file__))),
            '/usr/share/openmoo2',
        ]
        for datadir in datadirs:
            if os.path.isdir(datadir):
                return datadir

        raise OrionException('Failed to find datadir, something is fishy')

    def provide_lbx_datadir(self):
        """
        Provide path for lbx datafiles
        """

        return '{0}/lbx/'.format(self.datadir)

    def provide_datadir(self):
        """
        Provide path to datadir itself
        """

        return '{0}/'.format(self.datadir)
