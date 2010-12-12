__author__="peterman"
__date__ ="$May 16, 2010 1:24:40 PM$"

from space_object import SpaceObject

class Starship(SpaceObject):

    def __init__(self, ship_id):
        self.set_id(ship_id)

    def set_design(self, design):
        self.__design = design

    def get_design(self):
        return self.__design

    def set_owner(self, player_id):
        self.__owner = player_id

    def get_owner(self):
        return self.__owner

    def set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status

    def exists(self):
        return self.get_status() != 5

    def get_status_text(self):
        t = ["orbit", "travel", "launch", "???", "refit", "deleted", "build"]
        return t[self.get_status()]

    def set_orbiting(self):
        self.set_status(0)

    def is_orbiting(self):
        return self.get_status() == 0

    def set_travelling(self):
        self.set_status(1)

    def is_travelling(self):
        return self.get_status() == 1

    def set_launching(self):
        self.set_status(2)

    def is_launching(self):
        return self.get_status() == 2

    def set_destination(self, destination):
        self.__destination = destination

    def get_destination(self):
        return self.__destination

    def set_group_has_navigator(self, group_has_navigator):
        self.__group_has_navigator = group_has_navigator

    def get_group_has_navigator(self):
        return self.__group_has_navigator

    def set_travelling_speed(self, travelling_speed):
        self.__travelling_speed = travelling_speed

    def get_travelling_speed(self):
        return self.__travelling_speed

    def set_turns_left(self, turns_left):
        self.__turns_left = turns_left

    def get_turns_left(self):
        return self.__turns_left

    def set_shield_damage_percent(self, shield_damage_percent):
        self.__shield_damage_percent = shield_damage_percent

    def get_shield_damage_percent(self):
        return self.__shield_damage_percent

    def set_drive_damage_percent(self, drive_damage_percent):
        self.__drive_damage_percent = drive_damage_percent

    def get_drive_damage_percent(self):
        return self.__drive_damage_percent

    def set_computer_damage(self, computer_damage):
        self.__computer_damage = computer_damage

    def get_computer_damage(self):
        return self.__computer_damage

    def set_crew_quality(self, crew_quality):
        self.__crew_quality = crew_quality

    def get_crew_quality(self):
        return self.__crew_quality

    def set_crew_experience(self, crew_experience):
        self.__crew_experience = crew_experience

    def get_crew_experience(self):
        return self.__crew_experience

    def set_officer_id(self, officer_id):
        self.__officer_id = officer_id

    def get_officer_id(self):
        return self.__officer_id

    def set_special_device_damage(self, special_device_damage):
        self.__special_device_damage = special_device_damage

    def get_special_device_damage(self):
        return self.__special_device_damage

    def set_armor_damage(self, armor_damage):
        self.__armor_damage = armor_damage

    def get_armor_damage(self):
        return self.__armor_damage

    def set_structural_damage(self, structural_damage):
        self.__structural_damage = structural_damage

    def get_structural_damage(self):
        return self.__structural_damage

    def set_mission(self, mission):
        self.__mission = mission

    def get_mission(self):
        return self.__mission

    def set_just_built(self, just_built):
        self.__just_built = just_built

    def get_just_built(self):
        return self.__just_built

    def print_debug(self, owner_player, stars):
        print
        print("=== ship # %i ... %s ===" % (self.get_id(), owner_player.get_race_name()))
        print("    status = %i" % self.get_status())
        print("    coords = %i, %i" % (self.get_x(), self.get_y()))
#	print("    group_has_navigator = %i" % self.get_group_has_navigator())
#	print("    missin = %i" % self.get_mission())
        print("    destination = %i" % (self.get_destination()))
        print("    turns_left = %i" % self.get_turns_left())
#        print("     star: %s" % stars[self.get_location()].get_name())
#        print("     star: %s" % stars[self.get_location_x()].get_name())

#        for star_id in stars:
#            print("star # %i ... %s" % (star_id, stars[star_id].get_name()))
#        print("/ship")
        print
