# OpenMOO2

open source clone of Microprose game "Master of Orion II: Battle at Antares"

## General info

### Licensing / copying

OpenMOO2 is licensed under the GNU General Public License version 2.0.
For more information, see the file LICENSE or visit
http://www.gnu.org/licenses/.

### Requirements

Python
Pygame 1.8.1 or newer
Original MOO2 game release
 * the game uses original MOO2's .LBX files
 * required LBX files are listed in the data/lbx.md5 file

### Supported operating systems

 * GNU/Linux
 * Mac OS X

### Installation

 * Install python 2.7 or newer on your system
 * Use python setup.py to install the package
   * Requires python module pygame
 * copy/link original MOO2 game data (.LBX files) into the game data folder

### Running the server

Run "openmoo2-server" binary to execute the server.
 * by default the server listens on localhost on port 9999
 * the values can be changed using the command line options
   * -h &gt;address&lt;
   * -p &gt;port&lt;
   * -g &gt;savegame file&lt;

### Running the game client

Run "openmoo2" binary to start the game client.
 * by default the client connect to server running on localhost port 9999
 * the values can be changed using the command line options
   * -h &gt;address&lt;
   * -p &gt;port&lt;
