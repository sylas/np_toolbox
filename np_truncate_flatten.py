from math import sqrt
from np_ps import select_file
from random import normalvariate

def main():
    '''
    Program adjusts y-positions of the spheres in the input script for Omnisim, 
    so they will appear as the truncated and flattened spheres in the baseline.
    It is done by applying the truncating and flattening factors, given in percent
    with some standard deviation.

    More info: http://www.ambrsoft.com/TrigoCalc/Sphere/Cap/SphereCap.htm
 
    Input:
          File with the following structure:
          (...)
          f.Exec("app.subnodes[project].subnodes[device].fsdevice.addellipsoid(layer,z,x,angle,y,sizez,sizex,sizey)")
          (...)
          Assumption: nanoparticles are placed in the "zx" or "xz" plane, so y value is to be adjusted.    
    Output: 
          File with a "_truncx_flaty" suffix, 
          where x is the truncating factor and y is the flattening factor
    '''

    # Read input file
    filename = select_file('py')
    file = open(filename,"rt")
    data = file.readlines()
    file.close()

    # Truncating factor for the spheres [%]
    truncate = -1
    print("Spheres could be cut (truncated). 100% - full sphere, 50% - hemisphere, etc.")
    while truncate < 0 or truncate > 100: 
        truncate = int(input("Enter the percent where the spheres will be cut [0-100%]: "))
    sigma_truncate = -1
    while sigma_truncate < 0: 
        sigma_truncate = int(input("Enter the standard deviation for sphere cut, or 0: "))

    # Flattening factor for the spheres [%]
    print("Spheres could be flattened. Y-size = 100% - full size, 50% - flatten by a half, etc.")
    flatten = -1
    while flatten < 0 or flatten > 100: 
        flatten = int(input("Enter the percent of the nominal y-size of the spheres [0-100%]: "))
    sigma_flatten = -1
    while sigma_flatten < 0: 
        sigma_flatten = int(input("Enter the standard deviation for sphere flatten, or 0: "))

        
    # The new device number (optionally) 
    try:
        new_device = int(input("Enter device number, or <cr> to keep existing one: "))
    except ValueError:
        new_device = -1
                
    # Output file 
    output_filename = "{}_trunc{}s{}_flat{}s{}.py".format(filename[:-3],truncate,sigma_truncate,flatten,sigma_flatten)
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
            # Truncate distribution:
            truncate_dist = normalvariate(truncate,sigma_truncate)
            h = (100-truncate_dist)*sizex / 100.0 # Height of the cap
            r = sqrt(2*R*h-h*h)      # Radius of the cap
            t = r/R                  # Ratio between radiuses
            rc = R/t                 # New radius of the sphere, adjusted of the ratio
            #a = R - h
            #y = R + y + a            # New y positon
            y = 2*R + y - h
            
            if 50 < truncate_dist < 100:
                sizex = rc * 2
                sizey = rc * 2
                sizez = rc * 2

            # Flattening
            flatten_dist = normalvariate(flatten,sigma_truncate)
            y = y + sizey*(1-flatten_dist/100)/4
            sizey = sizey*flatten_dist/100
            
                    
            # addellipsoid     FUNCTION ( layer, z, x, angle, y, sizez, sizex, sizey )
            newline = \
            'f.Exec("app.subnodes[{0}].subnodes[{1}].fsdevice.addellipsoid({2},{3},{4},{5},{6},{7},{8},{9})")\n'\
            .format(project, device, layer, z, x, angle, y, sizez, sizex, sizey)
            
            file.write(newline)

    file.close()
    print("Output file {} has been created.".format(output_filename))
