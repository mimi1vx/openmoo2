from game_object import GameObject

__author__="peterman"
__date__ ="$May 16, 2010 1:31:45 PM$"

class Player(GameObject):

    def __init__(self, player_id):
        self.__explored_stars = []
        self.set_id(player_id)

    def alive(self):
        return self.get_emperor_name()

    def set_moo2data(self, moo2data):
        self.__moo2data = moo2data

    def get_moo2data(self):
        return self.__moo2data

    def set_emperor_name(self, emperor_name):
        self.__emperor_name = emperor_name

    def get_emperor_name(self):
        return self.__emperor_name

    def set_race_name(self, race_name):
        self.__race_name = race_name

    def get_race_name(self):
        return self.__race_name

    def set_picture(self, picture):
        self.__picture = picture

    def get_picture(self):
        return self.__picture

    def set_color(self, color):
        self.__color = color

    def get_color(self):
        return self.__color

    def set_personality(self, personality):
        self.__personality = personality

    def get_personality(self):
        return self.__personality

    def set_objective(self, objective):
        self.__objective = objective

    def get_objective(self):
        return self.__objective

    def set_tax_rate(self, tax_rate):
        self.__tax_rate = tax_rate

    def get_tax_rate(self):
        return self.__tax_rate

    def set_bc(self, bc):
        self.__bc = bc

    def get_bc(self):
        return self.__bc

    def raise_bc(self):
        self.set_bc(self.get_bc() + self.get_bc_income())

    def set_total_frighters(self, total_frighters):
        self.__total_frighters = total_frighters

    def get_total_frighters(self):
        return self.__total_frighters

    def set_used_frighters(self, used_frighters):
        self.__used_frighters = used_frighters

    def get_used_frighters(self):
        return self.__used_frighters

    def set_command_points(self, command_points):
        self.__command_points = command_points

    def get_command_points(self):
        return self.__command_points

    def set_industry(self, industry):
        self.__industry = industry

    def get_industry(self):
        return self.__industry

    def set_research(self, research):
        self.__research = research

    def get_research(self):
        return self.__research

    def add_research(self, research):
        self.__research += research

    def set_food(self, food):
        self.__food = food

    def add_food(self, food):
        self.__food += food

    def get_food(self):
        return self.__food

    def set_bc_income(self, bc_income):
        self.__bc_income = bc_income

    def get_bc_income(self):
        return self.__bc_income

    def set_research_progress(self, research_progress):
        self.__research_progress = research_progress

    def get_research_progress(self):
        return self.__research_progress

    def raise_research(self):
        self.__research_progress += self.get_research()

    def reseatch_completed(self):
        return self.get_research_progress() >= self.get_research_costs()

    def set_research_area(self, research_area):
        self.__research_area = research_area

    def get_research_area(self):
        return self.__research_area

    def set_research_item(self, research_item):
        self.__research_item = research_item

    def get_research_item(self):
        return self.__research_item

    def set_research_costs(self, research_costs):
        self.__research_costs = research_costs

    def get_research_costs(self):
        return self.__research_costs

    def set_research_turns_left(self, research_turns_left):
        if (research_turns_left) < 0:
            self.__research_turns_left = 0
        else:
            self.__research_turns_left = research_turns_left

    def get_research_turns_left(self):
        return self.__research_turns_left

    def set_racepicks(self, racepicks):
        self.__racepicks = racepicks

    def get_racepicks(self):
        return self.__racepicks

    def set_racepick_item(self, item, value):
        self.__racepicks[item] = value

    def get_racepick_item(self, item):
        return self.__racepicks[item]

    def set_known_techs(self, known_techs):
        self.__known_techs = known_techs

    def get_known_techs(self):
        return self.__known_techs

    def add_known_technology(self, tech_id):
        self.__known_techs.append(tech_id)

    def knows_technology(self, tech_id):
        return tech_id in self.__known_techs

    def set_prototypes(self, prototypes):
        self.__prototypes = prototypes

    def get_prototypes(self):
        return self.__prototypes

    def add_prototype(self, prototype):
        self.__prototypes.append(prototype)

    def set_tributes(self, tributes):
        self.__tributes = tributes

    def get_tributes(self):
        return self.__tributes

    def add_tribute(self, tribute):
        self.__tributes.append(tribute)

    def update_research_areas(self, research_areas):
        self.__research_areas = research_areas

    def list_research_areas(self):
        return self.__research_areas

    def knows_star_id(self, star_id):
        return star_id in self.__explored_stars

    def add_explored_star_id(self, star_id):
        if star_id and not self.knows_star_id(star_id):
            self.__explored_stars.append(star_id)

    def print_debug(self):
        print
        print("=== player_id = %i ===" % self.get_id())
        print("     race     = %s" % self.get_race_name())
        print("     emperor  = %s" % self.get_emperor_name())
        print("     color    = %i" % self.get_color())
        print
        print("     food     = %i" % self.get_food())
        print
        print("     research = %i" % self.get_research())
        print("     research_area = %i" % self.get_research_area())
        print("     research_item = %i" % self.get_research_item())
        print("     research_costs = %i" % self.get_research_costs())
        print("     research_progress = %i" % self.get_research_progress())
        print("     research_turns_left = %i" % self.get_research_turns_left())

    def print_research_debug(self):
        print("research_item = %i, research_area = %i, research_progress = %i, " % (self.get_research_item(), self.get_research_area(), self.get_research_progress()))
