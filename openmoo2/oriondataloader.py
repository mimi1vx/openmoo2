# vim: set ts=4 sw=4 et: coding=UTF-8

from .orionexception import OrionException

class OrionDataLoader(Object):
    """
    Class providing interface to load various datafiles
    """

def find_lbx_datadir(self):
    """
    Try to find where we can finx the lbx datafiles
    """
    
    datadir = '{0}/../data/lbx'.format(os.path.dirname(os.path.realpath(__file__)))
    if os.path.isdir(datadir):
        return datadir
    
    datadir='/usr/share/openmoo2/lbx'
    if os.path.isdir(datadir):
        return datadir

    raise OrionException('Failed to find datadir with lbx content, something is fishy')