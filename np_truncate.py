from math import sqrt
from np_ps import select_file

def main():
    '''
    Program adjusts y-positions of the spheres in the input script for Omnisim, 
    so they will appear as the truncated spheres in the baseline.
    It is done by applying the truncating factor, given in percent.

    More info: http://www.ambrsoft.com/TrigoCalc/Sphere/Cap/SphereCap.htm
 
    Input:
          File with the following structure:
          (...)
          f.Exec("app.subnodes[project].subnodes[device].fsdevice.addellipsoid(layer,z,x,angle,y,sizez,sizex,sizey)")
          (...)
          Assumption: nanoparticles are placed in the "zx" or "xz" plane, so y value is to be adjusted.    
    Output: 
          File with a "_truncate-x" suffix, where x is the truncating factor.
    '''

    # Read input file
    filename = select_file('py')
    file = open(filename,"rt")
    data = file.readlines()
    file.close()

    # Truncating factor for the spheres [%]
    truncate = -1
    while truncate < 0 or truncate > 100: 
        truncate = int(input("Enter the percent where the sphere will be cut [0-100%]: "))

    # The new device number (optionally) 
    try:
        new_device = int(input("Enter device number, or <cr> to keep existing one: "))
    except ValueError:
        new_device = -1
                
    # Output file 
    output_filename = "{}_trunc-{}.py".format(filename[:-3], truncate)
    file = open(output_filename, "w")

    for line in data:
        if line.find("fsdevice.addellipsoid") == -1:
            # Not a line with addellipsoid function, so simply rewrite it to output
            file.write(line)
        else:
            idx1 = line.index("[")+1
            idx2 = line.index("]", idx1)
            project = int(line[idx1:idx2])

            idx1 = line.index("[",idx2)+1
            idx2 = line.index("]", idx1)
            if new_device == -1:
                device = int(line[idx1:idx2])
            else:
                device = new_device
            
            idx1 = line.index("(", idx2)
            idx2 = line.index(")", idx1+1)
            line_list = line[idx1+1:idx2].split(",")

            layer = int(line_list[0])
            z = float(line_list[1])
            x = float(line_list[2])
            angle = float(line_list[3])
            y = float(line_list[4])
            sizex = float(line_list[5])
            sizey = float(line_list[6])
            sizez = float(line_list[7])
            
            # Calculate new size and y position
            R = sizex/2.0            # Radius of the original sphere
            h = (100-truncate)*sizex / 100.0 # Height of the cap
            r = sqrt(2*R*h-h*h)      # Radius of the cap
            t = r/R                  # Ratio between radiuses
            rc = R/t                 # New radius of the sphere, adjusted of the ratio
            #a = R - h
            #y = R + y + a            # New y positon
            y = 2*R + y - h
            
            if 50 < truncate < 100:
                sizex = rc * 2
                sizey = rc * 2
                sizez = rc * 2
                    
            # addellipsoid     FUNCTION ( layer, z, x, angle, y, sizez, sizex, sizey )
            newline = 'f.Exec("app.subnodes[{0}].subnodes[{1}].fsdevice.addellipsoid({2},{3},{4},{5},{6},{7},{8},{9})")\n'\
            .format(project, device, layer, z, x, angle, y, sizez, sizex, sizey)
            
            file.write(newline)

    file.close()
    print("Output file {} has been created.".format(output_filename))
