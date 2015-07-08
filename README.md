OpenMOO2
open source clone of Microprose game "Master of Orion II: Battle at Antares"

version: 0.1 / alpha preview

=== General info ===

	Licensing / copying

		OpenMOO2 is licensed under the GNU General Public License version 2.0.
		For more information, see the file GPL-2.0.TXT or visit http://www.gnu.org/licenses/

	Requirements:

		Python 2.6
		Pygame 1.8.1 or 1.9.1

		Original MOO2 version 1.31
		    - the game uses original MOO2's .LBX files
		    required LBX files are listed in the lbx-list.txt file

	Supported operating systems

		tested on

			GNU/Linux - Ubuntu	- Python 2.6.4 + Pygame 1.8.1
			Open Solaris		- Python 2.6.5 + Pygame 1.8.1
			Windows XP		- Python 2.6.5 + Pygame 1.9.1
			Windows Vista Home	- Python 2.6.5 + Pygame 1.8.1
			Mac OS X 10.0.6.3	- Python 2.6.5 + Pygame 1.9.1

		probably should work on (not tested)

			Windows 98/2000
			*BSD

=== Installation ===

	* download and install recent version of Python 2.6 using your package manager or get it from http://python.org/

	* download and install Pygame 1.8.1 using your package manager or get it from http://pygame.org/

		link to Pygame 1.8.1 for Python 2.6 - Windows 32-bit:
		ftp://pygame.org/pub/pygame/pygame-1.8.1release.win32-py2.6.msi

	Windows users:

		use the c:\python26 as install directory
		or
		edit server.bat and client.bat files and change c:\python26 path to your install directory


	* copy/link original MOO2 game data (.LBX files) into the "moo2" subdirectory
		actual list of required .LBX files is available in lbx-list.txt file

	the moo2 directory contains 10 SAVE*.GAM files - those are used for the game development right now...

=== Running the server ===

	run server.bat (server.sh for unix like systems)

	by default, the server listens on localhost on port 9999

	both address and port can be changed using the command line options:
		-h <address>
		-p <port>

	by default the SAVE1.GAM is used to load the game
	if you want to try another savegame file use command line option:
		-g <savegame file>

=== Running the game client ===

	run the client.bat (client.sh for unix like systems)

	by default client connects to localhost to port 9999

	both address and port can be changed using the command line options:
		-h <address>
		-p <port>

=== The game ===

	Actually the game is a bit far from being full playable...

	Game screens available:

		Main screen with starmap
			possible to click on a star to see star system details with planets
				possible to click on a planet to visit a colony screen
		
		Colonies list screen
			possible to click on colony's name to visit the colony screen
			possible to click on most right field to directly visit colony build screen

		Leaders screen
			possible to switch view between colony leaders and ship officers

		Research screen
			it is possible to change the research area

		Next turn
			server performs next turn recount and raises the stardate:
				population grow
				BC points are raised
				Research advances
