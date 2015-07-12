# vim: set ts=4 sw=4 et: coding=UTF-8

import random

def determine_probability(percentage):
    """
    Figure if we are match for probability or not:
    @param: percentage: probability against which we play
    @return: True/False bool
    """
    if random.randrange(0,100,1) <= percentage:
        return True
    return False

def get_50_50(option1, option2, penalize=0):
    """
    Determine 50-50 winner from 2 choices
    @param option1: first choice
    @param option2: second choice
    @param penalize: penalization agaisnt 1st choice (0-50)
    @return: option1 or option2
    """
    if random.randrange(0,100,1) <= 50-penalize:
        return option1
    return option2