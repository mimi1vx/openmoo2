
__author__="peterman"
__date__ ="$Jan 10, 2009 11:23:18 PM$"

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
    'SHIELDS':                  ["-", "class 1", "class 3", "class 5", "class 7", "class 10"],
    'COLONIST_TYPE':		{0x02: "farmer", 0x03: "scientist", 0x82: "worker"},
    'COMPUTERS':                ["-", "Electronic", "Optronic", "Positronic", "Cybertronic", "Moleculartronic"],
    'WEAPONS':                  ["None", "Mass Driver", "Gauss Cannon", "Laser Cannon", "Particle Beam", "Fusion Beam", "Ion Pulse Cannon", "Graviton Beam", "Neutron Blaster", "Phasor", "Disrupter", "Death Ray", "Plasma Cannon", "Spatial Compressor", "Nuclear Missile", "Merculite Missile", "Pulson Missile", "Zeon Missile", "Anti-Matter Torpedo", "Proton Torpedo", "Plasma Torpedo", "Nuclear Bomb", "Fusion Bomb", "Anti-Matter Bomb", "Neutronium Bomb", "Death Spore", "Bio Terminator", "Mauler Device", "Assault Shuttle", "Heavy Fighter", "Bomber", "Interceptor", "Stasis Field", "Anti-Missile Rocket", "Gyro Destabilizer", "Plasma Web", "Pulsar", "Black Hole Generator", "Stellar Converter", "Tractor Beam", "Dragon Breath", "Phasor Eye", "Crystal Ray", "Plasma Breath", "Plasma Flux", "Caustic Slime"],
    'WEAPON_ARCS':              ["-", "Forward", "Forward ext.", "", "Back ext.", "", "", "", "Back", "", "", "", "", "", "", "360", "x"],
    'WEAPON_MODS_BEAM':         ["-", "Heavy Mount", "Point Defense", "Armor piercing", "Continous", "No Range Dissipation", "Shield Piercing", "AutoFire"],
    'WEAPON_MODS_MISILLE':      ["-", "Enveloping", "Mirv", "ECCM", "Heavily Armored", "Fast", "Emimisions Guidance", "Overloaded"],

    'SHIP_EXP_LEVEL':           ["Green", "Regular", "Veteran", "Elite", "Ultra Elite"],

    'SHIP_SPECIALS':            [
                                    ["unknown special 1", "Achilles Targeting Unit", "Augmented Engines", "Automated Repair Unit", "Battle Pods", "Battle Scanner", "Cloaking Device", "Damper Field"],
                                    ["Displacement Device", "ECM Jammer", "Energy Absorber", "Extended Fuel Tanks", "Fast Missile Racks", "Hard Shields", "Heavy Armor", "High Energy Focus"],
                                    ["Hyper X Capacitors", "Inertial Nullifier", "Inertial Stabilizer", "Lightning Field", "Multi-Phased Shields", "Multi-Wave ECM Jammer", "Phase Shifter", "Phasing Cloak"],
                                    ["Quantum Dentonator", "Range Master Unit", "Reflection Field", "Reinforced Hull", "Scout Lab", "Security Stations", "Shield Capacitor", "Stealth Field"],
                                    ["Structual Analyzer", "Sub Space Teleporter", "Time Warp Facilitator", "Transporters", "Troop Pods", "Warp Dissipator", "Wide Area Jammer", "unknown special 2"]
                                ],


    'STAR_SIZES':               ['Small', 'Medium', 'Large'],
    'STAR_CLASSES':             ['Blue', 'White', 'Yellow', 'Orange', 'Red', 'Gray', 'Black Hole'],

    'SYSTEM_SPECIALS':		["-", "stable wormhole", "space debris", "pirate cache", "gold deposits", "gem deposits", "natives", "splinter colony", "lost hero", "space monster", "ancient artifacts", "orion", "MAX_SYSTEM_AND_PLANET_SPECIALS"],

    'TECH_LIST':                ["Achilles Targeting Unit", "Adamantium Armor", "Advanced City Planning", "Advanced Damage Control", "Alien Management Center", "Android Farmers", "Android Scientists", "Android Workers", "Anti-Gravity Harness", "Anti-Matter Bomb", "Anti-Matter Drive", "Anti-Matter Torpedoes", "Anti-Missile Rockets", "Armor Barracks", "Artemis System Net", "Artifical Planet", "Assault Shuttles", "Astro University", "Atmospheric Renewer", "Augmented Engines", "Autolab", "Automated Factories", "Automated Repair Unit", "Battleoids", "Battle Pods", "Battle Scanner", "Battlestation", "Bio-Terminator", "Biomorphic Fungi", "Black Hole Generator", "Bomber Bays", "Capitol", "Class I Shield", "Class III Shield", "Class V Shield", "Class VII Shield", "Class X Shield", "Cloaking Device", "Cloning Center", "Colony Base", "Colony Ship", "Confederation", "Cyber-Security Link", "Cybertronic Computer", "Damper Field", "Dauntless Guidance System", "Death Ray", "Death Spores", "Deep Core Mining", "Core Waste Dumps", "Deuterium Fuel Cells", "Dimensional Portal", "Displacement Device", "Disrupter Cannon", "Doom Star Construction", "Reinforced Hull", "ECM Jammer", "Electronic Computer", "Emissions Guidance System", "Energy Absorber", "Biospheres", "Evolutionary Mutation", "Extended Fuel Tanks", "Fast Missile Racks", "Federation", "Fighter Bays", "Fighter Garrison", "Food Replicators", "Freighters", "Fusion Beam", "Fusion Bomb", "Fusion Drive", "Fusion Rifle", "Gaia Transformation", "Galactic Currency Exchange", "Galactic Cybernet", "Galactic Unification", "Gauss Auto-Cannon", "Graviton Beam", "Gyro Destabilizer", "Hard Shields", "Heavy Armor", "Heavy Fighter Bays", "Heightened Intelligence", "High Energy Focus", "Holo Simulator", "Hydroponic Farms", "Hyper Drive", "MegaFluxers", "Hyper-X Capacitors", "Hyperspace Communications", "Imperium", "Inertial Nullifier", "Inertial Stabilizer", "Interphased Drive", "Ion Drive", "Ion Pulse Cannon", "Iridium Fuel Cells", "Jump Gate", "Laser Cannon", "Laser Rifle", "Lightning Field", "Marine Barracks", "Mass Driver", "Mauler Device", "Merculite Missile", "Microbiotics", "Microlite Construction", "Outpost Ship", "Moleculartronic Computer", "Multi-Wave Ecm Jammer", "Multi-Phased Shields", "Nano Disassemblers", "Neural Scanner", "Neutron Blaster", "Neutron Scanner", "Neutronium Armor", "Neutronium Bomb", "Nuclear Bomb", "Nuclear Drive", "Nuclear Missile", "Optronic Computer", "Particle Beam", "Personal Shield", "Phase Shifter", "Phasing Cloak", "Phasor", "Phasor Rifle", "Planetary Barrier Shield", "Planetary Flux Shield", "Planetary Gravity Generator", "Planetary Missile Base", "Ground Batteries", "Planetary Radiation Shield", "Planetary Stock Exchange", "Planetary Supercomputer", "Plasma Cannon", "Plasma Rifle", "Plasma Torpedoes", "Plasma Web", "Pleasure Dome", "Pollution Processor", "Positronic Computer", "Powered Armor", "Pulse Rifle", "Proton Torpedoes", "Psionics", "Pulsar", "Pulson Missile", "Quantum Detonator", "Rangemaster Unit", "Recyclotron", "Reflection Field", "Robotic Factory", "Research Laboratory", "Robo-Miners", "Space Scanner", "Scout Lab", "Security Stations", "Sensors", "Shield Capacitors", "Soil Enrichment", "Space Academy", "Spaceport", "Spatial Compressor", "Spy Network", "Standard Fuel Cells", "Star Base", "Star Fortress", "Star Gate", "Stasis Field", "Stealth Field", "Stealth Suit", "Stellar Converter", "Structural Analyzer", "Sub-Space Communications", "Sub-Space Teleporter", "Subterranean Farms", "Survival Pods", "Tachyon Communications", "Tachyon Scanner", "Telepathic Training", "Terraforming", "Thorium Fuel Cells", "Time Warp Facilitator", "Titan Construction", "Titanium Armor", "Tractor Beam", "Transport", "Transporters", "Tritanium Armor", "Troop Pods", "Universal Antidote", "Uridium Fuel Cells", "Virtual Reality Network", "Warp Dissipater", "Warp Interdictor", "Weather Control System", "Wide Area Jammer", "Xeno Psychology", "Xentronium Armor", "Zeon Missile", "Zortrium Armor"]
    }
