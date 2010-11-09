TECH_NONE	= 0
TECH_UNKNOWN	= 1
TECH_KNOWN	= 3

TECH_TABLE = {
    0:  {
        'name':		"",
        'area':		0,
    },
    1:	{
        'name':		"Achilles Targeting Unit",
        'area':		49,
    },
    2:	{
        'name':		"Adamantium Armor",
        'area':		48,
    },
    3:	{
        'name':		"Advanced City Planning",
        'area':		42,
    },
    4:	{
        'name':		"Advanced Damage Control",
        'area':		63,
    },
    5:	{
        'name':		"Alien Management Center",
        'area':		73,
    },
    6:	{
        'name':		"Android Farmers",
        'area':		24,
    },
    7:	{
        'name':		"Android Scientists",
        'area':		24,
    },
    8:	{
        'name':		"Android Workers",
        'area':		24,
    },
    9:	{
        'name':		"Anti-Gravity Harness",
        'area':		36,
    },
    10:	{
        'name':		"Anti-Matter Bomb",
        'area':		13,
    },
    11:	{
        'name':		"Anti-Matter Drive",
        'area':		13,
    },
    12:	{
        'name':		"Anti-Matter Torpedoes",
        'area':		13,
    },
    13:	{
        'name':		"Anti-Missile Rockets",
        'area':		4,
    },
    14:	{
        'name':		"Armor Barracks",
        'area':		20,
        'description':  "Creates tank battalions. It has 2 units when built, and ads 1 unit every 10 turns, up to half the planet's  population. Eliminates the morale penalty for dictatorship and feudal governments."
    },
    15:	{
        'name':		"Artemis System Net",
        'area':		58,
    },
    16:	{
        'name':		"Planet Construction",
        'area':		8,
    },
    17:	{
        'name':		"Assault Shuttles",
        'area':		63,
    },
    18:	{
        'name':		"Astro University",
        'area':		12,
    },
    19:	{
        'name':		"Atmospheric Renewer",
        'area':		47,
    },
    20:	{
        'name':		"Augmented Engines",
        'area':		5,
    },
    21:	{
        'name':		"Autolab",
        'area':		25,
    },
    22:	{
        'name':		"Automated Factories",
        'area':		3,
    },
    23:	{
        'name':		"Automated Repair Unit",
        'area':		8,
    },
    24:	{
        'name':		"Battleoids",
        'area':		19,
    },
    25:	{
        'name':		"Battle Pods",
        'area':		21,
    },
    26:	{
        'name':		"Battle Scanner",
        'area':		66,
    },
    27:	{
        'name':		"Battlestation",
        'area':		62,
    },
    28:	{
        'name':		"Bio-Terminator",
        'area':		17,
    },
    29:	{
        'name':		"Biomorphic Fungi",
        'area':		70,
    },
    30:	{
        'name':		"Black Hole Generator",
        'area':		0,
    },
    31:	{
        'name':		"Bomber Bays",
        'area':		11,
    },
    32:	{
        'name':		"Capitol",
        'area':		0,
    },
    33:	{
        'name':		"Class I Shield",
        'area':		7,
    },
    34:	{
        'name':		"Class III Shield",
        'area':		45,
    },
    35:	{
        'name':		"Class V Shield",
        'area':		64,
    },
    36:	{
        'name':		"Class VII Shield",
        'area':		61,
    },
    37:	{
        'name':		"Class X Shield",
        'area':		68,
    },
    38:	{
        'name':		"Cloaking Device",
        'area':		26,
    },
    39:	{
        'name':		"Cloning Center",
        'area':		1,
        'description':  "Allows doctors to replace failing or damaged organs, increasing the population grow by +100K each turn as long as the current population is below the planetary maximum."
    },
    40:	{
        'name':		"Colony Base",
        'area':		0,
        'description':  "Creates a colony on another planet inside the same star system as the building colony."
    },
    41:	{
        'name':		"Colony Ship",
        'area':		23,
        'description':  "Capable of creating a colony in a distant star system. Will not engage in combat and will be destroyed when attacked if not escorted by a military ship."
    },
    42:	{
        'name':		"Confederation",
        'area':		0,
    },
    43:	{
        'name':		"Cyber-Security Link",
        'area':		14,
    },
    44:	{
        'name':		"Cybertronic Computer",
        'area':		25,
    },
    45:	{
        'name':		"Damper Field",
        'area':		0,
    },
    46:	{
        'name':		"Dauntless Guidance System",
        'area':		56,
    },
    47:	{
        'name':		"Death Ray",
        'area':		0,
    },
    48:	{
        'name':		"Death Spores",
        'area':		1,
    },
    49:	{
        'name':		"Deep Core Mining",
        'area':		67,
    },
    50:	{
        'name':		"Core Waste Dumps",
        'area':		67,
    },
    51:	{
        'name':		"Deuterium Fuel Cells",
        'area':		9,
    },
    52:	{
        'name':		"Dimensional Portal",
        'area':		51,
    },
    53:	{
        'name':		"Displacement Device",
        'area':		71,
    },
    54:	{
        'name':		"Disrupter Cannon",
        'area':		51,
    },
    55:	{
        'name':		"Doom Star Construction",
        'area':		58,
    },
    56:	{
        'name':		"Reinforced Hull",
        'area':		4,
    },
    57:	{
        'name':		"ECM Jammer",
        'area':		7,
    },
    58:	{
        'name':		"Electronic Computer",
        'area':		28,
    },
    59:	{
        'name':		"Emissions Guidance System",
        'area':		14,
    },
    60:	{
        'name':		"Energy Absorber",
        'area':		37,
    },
    61:	{
        'name':		"Biospheres",
        'area':		18,
    },
    62:	{
        'name':		"Evolutionary Mutation",
        'area':		70,
    },
    63:	{
        'name':		"Extended Fuel Tanks",
        'area':		22,
    },
    64:	{
        'name':		"Fast Missile Racks",
        'area':		63,
    },
    65:	{
        'name':		"Federation",
        'area':		0,
    },
    66:	{
        'name':		"Fighter Bays",
        'area':		4,
    },
    67:	{
        'name':		"Fighter Garrison",
        'area':		20,
    },
    68:	{
        'name':		"Food Replicators",
        'area':		46,
    },
    69:	{
        'name':		"Freighters",
        'area':		55,
    },
    70:	{
        'name':		"Fusion Beam",
        'area':		31,
    },
    71:	{
        'name':		"Fusion Bomb",
        'area':		5,
    },
    72:	{
        'name':		"Fusion Drive",
        'area':		5,
    },
    73:	{
        'name':		"Fusion Rifle",
        'area':		31,
    },
    74:	{
        'name':		"Gaia Transformation",
        'area':		70,
    },
    75:	{
        'name':		"Galactic Currency Exchange",
        'area':		32,
    },
    76:	{
        'name':		"Galactic Cybernet",
        'area':		33,
    },
    77:	{
        'name':		"Galactic Unification",
        'area':		0,
    },
    78:	{
        'name':		"Gauss Cannon",
        'area':		64,
    },
    79:	{
        'name':		"Graviton Beam",
        'area':		16,
    },
    80:	{
        'name':		"Gyro Destabilizer",
        'area':		36,
    },
    81:	{
        'name':		"Hard Shields",
        'area':		26,
    },
    82:	{
        'name':		"Heavy Armor",
        'area':		3,
    },
    83:	{
        'name':		"Heavy Fighter Bays",
        'area':		42,
    },
    84:	{
        'name':		"Heightened Intelligence",
        'area':		30,
    },
    85:	{
        'name':		"High Energy Focus",
        'area':		37,
    },
    86:	{
        'name':		"Holo Simulator",
        'area':		60,
    },
    87:	{
        'name':		"Hydroponic Farms",
        'area':		18,
    },
    88:	{
        'name':		"Hyper Drive",
        'area':		38,
    },
    89:	{
        'name':		"MegaFluxers",
        'area':		37,
    },
    90:	{
        'name':		"Hyper-X Capacitors",
        'area':		38,
    },
    91:	{
        'name':		"Hyperspace Communications",
        'area':		39,
    },
    92:	{
        'name':		"Imperium",
        'area':		6,
    },
    93:	{
        'name':		"Inertial Nullifier",
        'area':		71,
    },
    94:	{
        'name':		"Inertial Stabilizer",
        'area':		36,
    },
    95:	{
        'name':		"Interphased Drive",
        'area':		40,
    },
    96:	{
        'name':		"Ion Drive",
        'area':		41,
    },
    97:	{
        'name':		"Ion Pulse Cannon",
        'area':		41,
    },
    98:	{
        'name':		"Iridium Fuel Cells",
        'area':		47,
    },
    99:	{
        'name':		"Jump Gate",
        'area':		65,
    },
    100:	{
        'name':		"Laser Cannon",
        'area':		57,
    },
    101:	{
        'name':		"Laser Rifle",
        'area':		57,
    },
    102:	{
        'name':		"Lightning Field",
        'area':		72,
    },
    103:	{
        'name':		"Marine Barracks",
        'area':		0,
    },
    104:	{
        'name':		"Mass Driver",
        'area':		7,
    },
    105:	{
        'name':		"Mauler Device",
        'area':		39,
    },
    106:	{
        'name':		"Merculite Missile",
        'area':		2,
    },
    107:	{
        'name':		"Microbiotics",
        'area':		34,
    },
    108:	{
        'name':		"Microlite Construction",
        'area':		53,
        'worker_bonus': +1,
    },
    109:	{
        'name':		"Outpost Ship",
        'area':		23,
        'description':  "Capable of creating an outpost on any uninhabited planet. Outposts function like a colony, except no population units may be moved there. Outpost ships are unarmed and will be destroyed if not escorted by military ships."
    },
    110:	{
        'name':		"Moleculartronic Computer",
        'area':		49,
    },
    111:	{
        'name':		"Multi-Wave Ecm Jammer",
        'area':		64,
    },
    112:	{
        'name':		"Multi-Phased Shields",
        'area':		52,
    },
    113:	{
        'name':		"Nano Disassemblers",
        'area':		53,
    },
    114:	{
        'name':		"Neural Scanner",
        'area':		15,
    },
    115:	{
        'name':		"Neutron Blaster",
        'area':		54,
    },
    116:	{
        'name':		"Neutron Scanner",
        'area':		54,
    },
    117:	{
        'name':		"Neutronium Armor",
        'area':		50,
    },
    118:	{
        'name':		"Neutronium Bomb",
        'area':		40,
    },
    119:	{
        'name':		"Nuclear Bomb",
        'area':		55,
    },
    120:	{
        'name':		"Nuclear Drive",
        'area':		55,
    },
    121:	{
        'name':		"Nuclear Missile",
        'area':		22,
    },
    122:	{
        'name':		"Optronic Computer",
        'area':		56,
    },
    123:	{
        'name':		"Particle Beam",
        'area':		0,
    },
    124:	{
        'name':		"Personal Shield",
        'area':		27,
    },
    125:	{
        'name':		"Phase Shifter",
        'area':		0,
    },
    126:	{
        'name':		"Phasing Cloak",
        'area':		68,
    },
    127:	{
        'name':		"Phasor",
        'area':		52,
    },
    128:	{
        'name':		"Phasor Rifle",
        'area':		52,
    },
    129:	{
        'name':		"Planetary Barrier Shield",
        'area':		68,
    },
    130:	{
        'name':		"Planetary Flux Shield",
        'area':		61,
    },
    131:	{
        'name':		"Planetary Gravity Generator",
        'area':		16,
    },
    132:	{
        'name':		"Planetary Missile Base",
        'area':		3,
    },
    133:	{
        'name':		"Ground Batteries",
        'area':		19,
    },
    134:	{
        'name':		"Planetary Radiation Shield",
        'area':		45,
    },
    135:	{
        'name':		"Planetary Stock Exchange",
        'area':		43,
    },
    136:	{
        'name':		"Planetary Supercomputer",
        'area':		60,
    },
    137:	{
        'name':		"Plasma Cannon",
        'area':		59,
    },
    138:	{
        'name':		"Plasma Rifle",
        'area':		59,
    },
    139:	{
        'name':		"Plasma Torpedoes",
        'area':		40,
    },
    140:	{
        'name':		"Plasma Web",
        'area':		59,
    },
    141:	{
        'name':		"Pleasure Dome",
        'area':		49,
    },
    142:	{
        'name':		"Pollution Processor",
        'area':		2,
    },
    143:	{
        'name':		"Positronic Computer",
        'area':		60,
    },
    144:	{
        'name':		"Powered Armor",
        'area':		62,
    },
    145:	{
        'name':		"Pulse Rifle",
        'area':		0,
    },
    146:	{
        'name':		"Proton Torpedoes",
        'area':		38,
    },
    147:	{
        'name':                             "Psionics",
        'area':                             30,
        'government_morale_bonus':          [0, 0, 10, 10, 0, 0, 0], # percent
    },
    148:	{
        'name':		"Pulsar",
        'area':		72,
    },
    149:	{
        'name':		"Pulson Missile",
        'area':		47,
    },
    150:	{
        'name':		"Quantum Detonator",
        'area':		0,
    },
    151:	{
        'name':		"Rangemaster Unit",
        'area':		14,
    },
    152:	{
        'name':		"Recyclotron",
        'area':		8,
    },
    153:	{
        'name':		"Reflection Field",
        'area':		0,
    },
    154:	{
        'name':		"Robotic Factory",
        'area':		11,
    },
    155:	{
        'name':		"Research Laboratory",
        'area':		56,
    },
    156:	{
        'name':		"Robo-Miners",
        'area':		62,
    },
    157:	{
        'name':		"Space Scanner",
        'area':		57,
    },
    158:	{
        'name':		"Scout Lab",
        'area':		15,
    },
    159:	{
        'name':		"Security Stations",
        'area':		15,
    },
    160:	{
        'name':		"Sensors",
        'area':		39,
    },
    161:	{
        'name':		"Shield Capacitors",
        'area':		41,
    },
    162:	{
        'name':		"Soil Enrichment",
        'area':		1,
    },
    163:	{
        'name':		"Space Academy",
        'area':		10,
    },
    164:	{
        'name':		"Spaceport",
        'area':		20,
    },
    165:	{
        'name':		"Spatial Compressor",
        'area':		0,
    },
    166:	{
        'name':		"Spy Network",
        'area':		0,
    },
    167:	{
        'name':		"Standard Fuel Cells",
        'area':		22,
    },
    168:	{
        'name':		"Star Base",
        'area':		0,
    },
    169:	{
        'name':		"Star Fortress",
        'area':		42,
    },
    170:	{
        'name':		"Star Gate",
        'area':		69,
    },
    171:	{
        'name':		"Stasis Field",
        'area':		26,
    },
    172:	{
        'name':		"Stealth Field",
        'area':		27,
    },
    173:	{
        'name':		"Stealth Suit",
        'area':		27,
    },
    174:	{
        'name':		"Stellar Converter",
        'area':		69,
    },
    175:	{
        'name':		"Structural Analyzer",
        'area':		25,
    },
    176:	{
        'name':		"Sub-Space Communications",
        'area':		65,
    },
    177:	{
        'name':		"Sub-Space Teleporter",
        'area':		71,
    },
    178:	{
        'name':		"Subterranean Farms",
        'area':		44,
    },
    179:	{
        'name':		"Survival Pods",
        'area':		21,
    },
    180:	{
        'name':		"Tachyon Communications",
        'area':		66,
    },
    181:	{
        'name':		"Tachyon Scanner",
        'area':		66,
    },
    182:	{
        'name':		"Telepathic Training",
        'area':		34,
    },
    183:	{
        'name':		"Terraforming",
        'area':		35,
    },
    184:	{
        'name':		"Thorium Fuel Cells",
        'area':		48,
    },
    185:	{
        'name':		"Time Warp Facilitator",
        'area':		69,
    },
    186:	{
        'name':		"Titan Construction",
        'area':		19,
    },
    187:	{
        'name':		"Titanium Armor",
        'area':		22,
    },
    188:	{
        'name':		"Tractor Beam",
        'area':		16,
    },
    189:	{
        'name':		"Transport",
        'area':		23,
    },
    190:	{
        'name':		"Transporters",
        'area':		46,
    },
    191:	{
        'name':		"Tritanium Armor",
        'area':		9,
    },
    192:	{
        'name':		"Troop Pods",
        'area':		21,
    },
    193:	{
        'name':		"Universal Antidote",
        'area':		17,
    },
    194:	{
        'name':		"Urridium Fuel Cells",
        'area':		50,
    },
    195:	{
        'name':             "Virtual Reality Network",
        'area':             33,
        'morale_bonus':     20, # percent
    },
    196:	{
        'name':		"Warp Dissipater",
        'area':		45,
    },
    197:	{
        'name':		"Warp Interdictor",
        'area':		72,
    },
    198:	{
        'name':		"Weather Control System",
        'area':		44,
    },
    199:	{
        'name':		"Wide Area Jammer",
        'area':		61,
    },
    200:	{
        'name':		"Xeno Psychology",
        'area':		73,
    },
    201:	{
        'name':		"Xentronium Armor",
        'area':		0,
    },
    202:	{
        'name':		"Zeon Missile",
        'area':		50,
    },
    203:	{
        'name':		"Zortrium Armor",
        'area':		53,
    },
    204:	{
        'name':		"Biology I",
        'area':		75,
    },
    205:	{
        'name':		"Power I",
        'area':		76,
    },
    206:	{
        'name':		"Physics I",
        'area':		77,
    },
    207:	{
        'name':		"Construction I",
        'area':		78,
    },
    208:	{
        'name':		"Fields I",
        'area':		79,
    },
    209:	{
        'name':		"Chemistry I",
        'area':		80,
    },
    210:	{
        'name':		"Computers I",
        'area':		81,
    },
    211:	{
        'name':		"Sociology I",
        'area':		82,
    },
}
