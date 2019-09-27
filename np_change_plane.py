import readchar
from np_ps import set, select_file

def main():
    '''
    Manipulates the Omnisim input file, created by the Nanoparticle Detector:
    changes plane in which nanoparticles are located - from xy to xz (or zx), 
    and also allows for some other corrections as change project and device numbers,
    layer indices, baseline, and reversing values on the x-axis.
 
    Input:
          Python file (.py) with the following structure:
          (...)
          f.Exec("app.subnodes[project].subnodes[device].fsdevice.addellipsoid(layer,z,x,angle,y,sizez,sizex,sizey)")
          (...)    
    Output: 
          Python file (.py) with a "_xz" suffix.
    '''

    # New project, device, and nanoparticles layer
    # Old values will be overwritten
    project = 1
    device = 2
    layer = 1

    # New baseline (y-axis) for nanoparticles
    baseline = 0.5

    # In omnisim, z axis is horizontal, and x axis is vertical, 
    # so it may be convenient to exchange x and z in the output to achieve
    # direct comparison to the SEM image
    set_orientation_zx = True

    # Reverse x-axis or not, to have the the same view as on the SEM image
    # To do this, x_max needs to be known
    x_reverse = False
    x_max = 1.285 # for SEM: mag 100 000 x

    # Collect input file name
    filename = select_file('py')

    # Collect parameters
    ans = ""
    while ans != readchar.key.ENTER:
        print()
        print("Current settings:")
        print("Project number = ", project)
        print("Device number = ", device)
        print("NP layer index = ", layer)
        print("NP baseline = ", baseline)
        print("Set orientation ZX = ", set_orientation_zx)
        print("Reversing x values = ", x_reverse)
        print("Maximum x value for reversing = ", x_max)
        print()
        print("Press <cr> to accept, or anything else to change.")

        ans = readchar.readkey()
        if ans != readchar.key.ENTER:
            print()
            print("Modify settings:")
            project = set("project", project)    
            device = set("device", device)
            layer = set("layer", layer)
            baseline = set("baseline", baseline)
            set_orientation_zx = set("set_orientation_zx", set_orientation_zx)
            x_reverse = set("x_reverse", x_reverse)
            if x_reverse:
                x_max = set("x_max", x_max)


    # Read data
    file = open(filename,"rt")
    data = file.readlines()
    file.close()

    # Output file 
    file = open(filename[:-3]+"_xz.py", "w")

    for line in data:
        idx = line.find("fsdevice.addellipsoid")
        if idx == -1:
            # Not a line with addellipsoid function, so simply rewrite it to output
            file.write(line)
        else:
            try:
                idx1 = line.index("(", idx)
            except ValueError:
                continue
            try:
                idx2 = line.index(")", idx1+1)
            except:
                continue
            line_list = line[idx1+1:idx2].split(",")
            z = float(line_list[1])
            x = float(line_list[2])
            angle = float(line_list[3])
            y = float(line_list[4])
            sizex = float(line_list[5])
            sizey = float(line_list[6])
            sizez = float(line_list[7])
                           
            # Correct the value for the border between substrate and NPs
            old_baseline = z + sizez/2.0
            if baseline != old_baseline:
                baseline_correction = baseline - old_baseline
                z = z + baseline_correction
            
            # Exchange z and y and construct a new line 
            z,y = y,z        
            if set_orientation_zx:
                x,z = z,x
            if x_reverse:
                x = -x + x_max
                
            # addellipsoid     FUNCTION ( layer, z, x, angle, y, sizez, sizex, sizey )
            newline = 'f.Exec("app.subnodes[{0}].subnodes[{1}].fsdevice.addellipsoid({2},{3},{4},{5},{6},{7},{8},{9})")\n'\
            .format(project, device, layer, z, x, angle, y, sizez, sizex, sizey)
            
            file.write(newline)

    file.close()
    print("Output file {}_xz.py has been created.".format(filename[:-3]))
