
__author__="peterman"
__date__ ="$Jan 10, 2009 11:23:18 PM$"

import _tech_table

def planet_size(size):
    return ["Tiny", "Small", "Medium", "Large", "Huge"][size]

def planet_terrain(terrain):
    return ["Toxic", "Radiated", "Baren", "Desert", "Tundra", "Ocean", "Swamp", "Arid", "Terran", "Gaia", "k", "l"][terrain]

def planet_minerals(minerals):
    return ["Ultra Poor", "Poor", "Abundant", "Rich", "Ultra Rich"][minerals]

def greek_num(num):
    return ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"][num]

def planet_gravity(gravity):
    return ['Low G', 'Normal G', 'Heavy G'][gravity];

def get_dictionary():
    return {
    'COLONY_TYPES':             ["Colony", "Outpost"],
    'COLONY_ASSIGNMENT':        {0x00: "???", 0x01:"Agricultural Colony", 0x02: "Industrial Colony", 0x03: "Research Colony", 0xff: "Colony"},

    'RACE_PICTURES ':           ["Alkari", "Bulrathi", "Darlok", "Elerian", "Gnolam", "Human", "Klackon", "Meklar", "Mrrshan", "Psilon", "Sakkra", "Silicoid", "Trilarian"],

    'PLANET_TYPES':             ['?', 'Asteroids', 'Gas Giant', 'Planet', '??', '???', '????', '?????'],
    'PLANET_SIZES':             ['Tiny', 'Small', 'Medium', 'Large', 'Huge'],
    'PLANET_GRAVITIES':         ['Low G', 'Normal G', 'Heavy G'],
    'PLANET_TERRAINS':          ['Toxic', 'Radiated', 'Baren', 'Desert', 'Tundra', 'Ocean', 'Swamp', 'Arid', 'Terran', 'Gaia', 'k', 'l'],
    'PLANET_MINERALS':          ['Ultra Poor', 'Poor', 'Abundant', 'Rich', 'Ultra Rich'],
    'PLANET_SPECIALS':          ['-', 'Wormhole', 'Space Debris', 'Pirate Cache', 'Gold Deposits', 'Gem Deposits', 'Natives', 'Splinter', 'Hero', 'Monster', 'Artifacts', 'Orion'],

    'PLAYER_COLORS':		["red", "yellow", "green", "white", "blue", "brown", "purple", "orange"],
    'PLAYER_PERSONALITIES':	["Xenophobic", "Ruthless", "Aggressive", "Erratic", "Honorable", "Pacifist", "Dishonored"],
    'PLAYER_OBJECTIVES':	["Diplomat", "Militarist", "Expansionist", "Technologist", "Industrialist", "Ecologist"],
    'PLAYER_GOVERMENTS':	["Feudal", "Confederation", "Dictatorship", "Imperium", "Democracy", "Federation", "Unification", "Galactic Unification"],

    'SHIP_SIZES':               ["Frigate", "Destroyer", "Cruiser", "Battleship", "Titan", "Doomstar"],
    'SHIP_TYPES':               ["Combat Ship", "Colony Ship", "Transport Ship", "???", "Outpost Ship"],
    'DRIVES':                   ["-", "Nuclear", "Fusion", "Ion", "Antimatter", "Hyperdrive", "Interphased", "no unit"],
    'ARMORS':                   ["-", "Titanium", "Tritanium", "Zortrium", "Neutronium", "Adamantium", "Xentronium"],
    'SHIELDS':                  ["-", "Class I", "Class III", "Class V", "Class VII", "Class X"],
    'COLONIST_TYPE':		{0x02: "farmer", 0x03: "scientist", 0x82: "worker"},
    'COMPUTERS':                ["-", "Electronic", "Optronic", "Positronic", "Cybertronic", "Moleculartronic"],
    'WEAPONS':                  ["None", "Mass Driver", "Gauss Cannon", "Laser Cannon", "Particle Beam", "Fusion Beam", "Ion Pulse Cannon", "Graviton Beam", "Neutron Blaster", "Phasor", "Disrupter", "Death Ray", "Plasma Cannon", "Spatial Compressor", "Nuclear Missile", "Merculite Missile", "Pulson Missile", "Zeon Missile", "Anti-Matter Torpedo", "Proton Torpedo", "Plasma Torpedo", "Nuclear Bomb", "Fusion Bomb", "Anti-Matter Bomb", "Neutronium Bomb", "Death Spore", "Bio Terminator", "Mauler Device", "Assault Shuttle", "Heavy Fighter", "Bomber", "Interceptor", "Stasis Field", "Anti-Missile Rocket", "Gyro Destabilizer", "Plasma Web", "Pulsar", "Black Hole Generator", "Stellar Converter", "Tractor Beam", "Dragon Breath", "Phasor Eye", "Crystal Ray", "Plasma Breath", "Plasma Flux", "Caustic Slime"],
    'WEAPON_ARCS':              ["-", "Forward", "Forward ext.", "", "Back ext.", "", "", "", "Back", "", "", "", "", "", "", "360", "x"],
    'WEAPON_MODS_BEAM':         ["-", "Heavy Mount", "Point Defense", "Armor piercing", "Continous", "No Range Dissipation", "Shield Piercing", "AutoFire"],
    'WEAPON_MODS_MISILLE':      ["-", "Enveloping", "Mirv", "ECCM", "Heavily Armored", "Fast", "Emimisions Guidance", "Overloaded"],

    'SHIP_EXP_LEVEL':           ["Green", "Regular", "Veteran", "Elite", "Ultra Elite"],

    'SHIP_SPECIALS':            [
                                    "-no-special-", "Achilles Targeting Unit", "Augmented Engines", "Automated Repair Unit", "Battle Pods", "Battle Scanner", "Cloaking Device", "Damper Field",
                                    "Displacement Device", "ECM Jammer", "Energy Absorber", "Extended Fuel Tanks", "Fast Missile Racks", "Hard Shields", "Heavy Armor", "High Energy Focus",
                                    "Hyper X Capacitors", "Inertial Nullifier", "Inertial Stabilizer", "Lightning Field", "Multi-Phased Shields", "Multi-Wave ECM Jammer", "Phase Shifter", "Phasing Cloak",
                                    "Quantum Dentonator", "Range Master Unit", "Reflection Field", "Reinforced Hull", "Scout Lab", "Security Stations", "Shield Capacitor", "Stealth Field",
                                    "Structual Analyzer", "Sub Space Teleporter", "Time Warp Facilitator", "Transporters", "Troop Pods", "Warp Dissipator", "Wide Area Jammer", "unknown special 2"
                                ],


    'STAR_SIZES':               ['Small', 'Medium', 'Large'],
    'STAR_CLASSES':             ['Blue', 'White', 'Yellow', 'Orange', 'Red', 'Gray', 'Black Hole'],

    'SYSTEM_SPECIALS':		["-", "stable wormhole", "space debris", "pirate cache", "gold deposits", "gem deposits", "natives", "splinter colony", "lost hero", "space monster", "ancient artifacts", "orion", "MAX_SYSTEM_AND_PLANET_SPECIALS"],

    'TECH_LIST':                _tech_table.TECH_TABLE
    }
