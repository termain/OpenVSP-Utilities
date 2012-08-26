Utilities for [OpenVSP](http://www.openvsp.org/). 

Author:  Nathan Alday (n.c.alday@gmail.com)

License: [BSD 2 Clause](http://www.opensource.org/licenses/BSD-2-Clause)


Currently contains only the airfoil\_utilities.py. airfoil\_utilities.py converts airfoil data files in the [UIUC formats](http://www.ae.illinois.edu/m-selig/ads.html) run 

        python airfoil_utilities.py -h 

for more information.

As a demonstration, try running python airfoil_utilities.py demo.selig. This should convert the airfoil described in demo.selig to an OpenVSP formatted airfoil in a file named demo.af.
