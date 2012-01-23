from decimal import Decimal
from argparse import ArgumentParser

supported_formats="Supported formats are: \
'af': OpenVSP airfoil format.\n           \
'lednicer': Lednicer format as found at http://www.ae.illinois.edu/m-selig/ads.html.\n \
'selig': Selig format as found at http://www.ae.illinois.edu/m-selig/ads.html."""

def _closest_to_origin( points ):
    """Take list of points (2-tuples) and retun the index of the one closest
    to the origin."""
    norm = lambda xx: ( xx[0]**2 + xx[1]**2 )**Decimal(0.5) #two-norm function for sorting

    sorted_points = sorted( points, key=norm ) #ascending sort by distance from origin (leading edge)
    
    return points.index( sorted_points[0] )

class Airfoil(object):
    comment = ""
    name = ""
    symmetric_flag = False
    num_upper_surface_points = 0
    num_lower_surface_points = 0

    upper_surface_points = []
    lower_surface_points = []

    def __str__(self):
        string = "{comment}\n{name}\n{symmetric}\n{upper}\n{lower}\n".format(
                    comment=self.comment,
                    name=self.name,
                    symmetric=int(self.symmetric_flag),
                    upper=self.num_upper_surface_points,
                    lower=self.num_lower_surface_points )
            
        for point in self.upper_surface_points:
            string = string + "{0} {1}\n".format( point[0], point[1] )

        #pad space between upper and lower points
        string = string+"\n"

        for point in self.lower_surface_points:
            string = string + "{0} {1}\n".format( point[0], point[1] )

        return( string )

        
    def _load_lednicer_like( self, lines ):
        """Common subroutines between load_from_af_format and load_from_lednicer_format
           
        Loads from a list of lines from a file in Lednicer format. Only the point locations are loaded. """

        #read upper surface points
        for xx in range( self.num_upper_surface_points):
            chord_position = Decimal( lines[xx].split()[0] )
            height = Decimal( lines[xx].split()[1] )
            self.upper_surface_points.append( (chord_position, height) )
            
        #read lower surface points starting from the line after the blank line
        #that separates upper and lower surface points
        for xx in range( 1+self.num_upper_surface_points,
                         1+self.num_upper_surface_points+self.num_lower_surface_points ):
            chord_position = Decimal( lines[xx].split()[0] )
            height = Decimal( lines[xx].split()[1] )
            self.lower_surface_points.append( (chord_position, height) )

    def load_from_af_format( self, file_id ):
        """Load airfoil from file object in .af format"""
        lines = file_id.readlines()
        self.comment = lines.pop(0).strip('\n')
        self.name = lines.pop(0).strip('\n')
        self.symmetric_flag = bool( int( lines.pop(0).split()[0] ) )
        self.num_upper_surface_points = int( lines.pop(0).split()[0] )
        self.num_lower_surface_points = int( lines.pop(0).split()[0] )
        self._load_lednicer_like( lines )

    def load_from_lednicer_format(self, file_id):
        """Load files from Lednicer format. Seems identical to .af format except
           there is no comment field, no symmetrical field and number of points in different format (upper and lower on the same line)"""
        lines = file_id.readlines()
        self.name = lines.pop(0).strip('\n')
        num_points_line = lines.pop(0).strip().split()
        self.num_upper_surface_points = int( Decimal(num_points_line[0]) )
        self.num_lower_surface_points = int( Decimal(num_points_line[1]) )
        lines.pop(0) #remove blank line
        self._load_lednicer_like( lines )

    def load_from_selig_format(self, file_id ):
        """Load from the Selig format. http://www.ae.illinois.edu/m-selig/ads.html"""
        lines = file_id.readlines()
        self.name = lines.pop(0).strip('\n')
        pointify = lambda xx: (Decimal(line.split()[0]),Decimal(line.split()[1]))

        points = [ pointify(line) for line in lines ]

        #find point closest to leading edge. put preceding points in upper surface points. put points after in lower surface points. if it's positive in height, put it in upper surface points, if it's negative, put it in lower surface points. 
        closest_to_le = _closest_to_origin( points )

        upper_points = points[0:closest_to_le]
        upper_points.reverse()
        lower_points = points[closest_to_le+1:]

        if points[closest_to_le][1] >= Decimal(0.0):
            upper_points.insert( 0, points[closest_to_le] )
        else:
            lower_points.insert( 0, points[closest_to_le] )
         
        #insert leading edge
        upper_points.insert(0, (Decimal(0,0), Decimal(0,0) ) )
        lower_points.insert(0, (Decimal(0,0), Decimal(0,0) ) )

        self.symmetric_flag = False #just set this to false for now. could implement symmetry checking later
        self.num_upper_surface_points = len(upper_points)
        self.num_lower_surface_points = len(lower_points)
        
        self.upper_surface_points = upper_points
        self.lower_surface_points = lower_points        


    def load( self, file_id, format = 'af' ):
        """Load airfoil from file object in file format 'format' 

            {}""".format(supported_formats)
        
        if format == 'af':
            self.load_from_af_format( file_id )

        if format == 'lednicer':
            self.load_from_lednicer_format( file_id )

        if format == 'selig':
            self.load_from_selig_format( file_id )

    def load_file( self, file_name, format = 'selig' ):
        """Load airfoil from file in file format 'format' 

            {}""".format(supported_formats)
        file_id = open(file_name)
        self.load( file_id, format )
        file_id.close()

def convert_file( in_file_name, out_file_name, format='selig'  ):
    """Convert in_file_name to out_file_name in OpenVSP .af format from format 'format'. Default input format is 'selig'

       {}""".format(supported_formats)

    out_file = open(out_file_name,'w')

    af = Airfoil()
    af.load_file(in_file_name, format)
    out_file.write( str(af) )
    out_file.close()
    
def convert_multiple_files( file_list, suffix='.af', format='selig',change_suffix='True' ):
    """Convert list of files in file_list. Appends/changes the suffix. Defaults to changing suffix to .af"""
    for file_name in file_list:
        if change_suffix:
            stem = file_name.rpartition('.')[0]
        else:
            stem = file_name
        
        new_name = stem+suffix
        convert_file( file_name, new_name, format )
       

if __name__=="__main__":
    parser = ArgumentParser( description="""Convert airfoil files into OpenVSP airfoil (.af) files. 

{}""".format(supported_formats),
    epilog="Author: Nathan Alday, n.c.alday@gmail.com")

    parser.add_argument( 'files', metavar='FILE', 
        help='Name of file to be converted',nargs='+')
    parser.add_argument( '--format', metavar='FORMAT',
        help='Format of output files, defaults to selig', 
        action='store', default='selig', type=str  )

    args=parser.parse_args()

    convert_multiple_files( args.files, format = args.format )

    
