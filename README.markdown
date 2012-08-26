Utilities for [OpenVSP](http://www.openvsp.org/). 

Author:  Nathan Alday (n.c.alday@gmail.com)

License: [BSD 2 Clause](http://www.opensource.org/licenses/BSD-2-Clause)


Currently contains only the airfoil\_utilities.py. airfoil\_utilities.py converts airfoil data files in the [UIUC formats](http://www.ae.illinois.edu/m-selig/ads.html) run 

        python airfoil_utilities.py -h 

for more information. Note that airfoil_utilities.py requires Python 2.7 or later.

As a demonstration, try running python airfoil_utilities.py demo.selig. This should convert the airfoil described in demo.selig to an OpenVSP formatted airfoil in a file named demo.af.

#Quickstart Guide

A set of guides for downloading and using the utilities.

##Ubuntu 12.04

1. Open a terminal (Perhaps using Ctrl+Alt+T).

2. Install git if not already installed.

    $ sudo apt-get install git

3. Clone the OpenVSP-Utilities repository from github.

    $ git clone https://github.com/termain/OpenVSP-Utilities.git

4. Move to the OpenVSP-Utilities directory.

    $ cd OpenVSP-Utilities

5. Run the airfoil_utilities.py script on the demo.selig airfoil file.

    $ python airfoil_utilities.py demo.selig

6. Check to see that the OpenVSP formatted demo.af was created with `ls`.

    $ ls demo.af
    demo.af

7. Open the two files in gedit to compare them.

    $ gedit demo.af demo.selig &

8. Use the `-h` flag for more info.

    $ python airfoil_utilities.py -h

