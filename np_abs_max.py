from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import os, sys, readchar
from datetime import datetime
from np_ps import set

def main():
    '''
    Calculates maxima of absorption spectra given in the the *.txt or .cht files.
    
    Input: 
           All .cht and .txt files from current directory, containing sensor data from Omnisim.           
           For best results (e.g. automatic determination of variable names), 
           Omnisim should be run in FDTD Scanner mode, scanning for np_size, inglass, trunc etc.
    Output: 
           abs-max-out file
    '''
    
    plot_partial = False
    plot_final = True
    do_linear_regression = True
    output_filename = "abs-max-out"

    # Maximum will be searched in range [xminint, xmaxint] with accuracy intstep
    # (by interpolating data in this range with given step, then taking the maximum)
    xminint = 305
    xmaxint = 600

    print("Program looks for maximum in the [xmin, xmax] range.")
    print("Current xmin = {}, xmax = {}".format(xminint, xmaxint))
    print("Press <cr> to accept, the other key to change")
        
    ans = readchar.readkey()
    if ans != readchar.key.ENTER:
        print()
        print("Modify settings:")
        xminint = set("xmin", xminint)    
        xmaxint = set("xmax", xmaxint)

    intstep = 0.01
    intpoints = int((xmaxint - xminint) / intstep)

    # Default value for comparison with the experimental data
    np_size = 50 # [nm]

    # Experimental maxima {size [nm] : maximum [nm]}
    # http://www.cytodiagnostics.com/store/pc/Gold-Nanoparticle-Properties-d2.htm
    experimental_maxima = {5:515, 10:517, 15:525, 20:524, 30:526, 40:530, 50:535, \
    60:540, 70:548, 80:553, 90:564, 100:572}

    # Collect the filenames with the absorption spectra
    input_filenames = []
    for filename in os.listdir("."):
        if filename.endswith(".txt") or filename.endswith(".cht"):
            input_filenames.append(filename)

    if len(input_filenames) == 0:
        print("No proper files found in the directory, exiting...")
        sys.exit()
            
    input_filenames.sort()
       
    # Get the variable name from first file, second line.
    # If variable does not exists (i.e. Omnisim was not run in Scanner mode),
    # ask for a variable name
    idx1 = 0
    idx2 = 0
    if input_filenames[0].endswith(".txt"):
        file = open(input_filenames[0],"rt")
        line = file.readlines()[1]
        file.close()
        idx1 = line.find("(")+1
        idx2 = line.find("=")-1
    if idx1 != 0 and idx2 != 0:
        var_name = line[idx1:idx2]
    else:
        var_name = input("No variable name was found in the input file. Enter variable name or leave blank for none: ")
        
    # Save output file header
    file = open(output_filename,"w")
    file.write("# File created on {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    file.write("# {}   lambda_max [nm]\n".format(var_name)) 
    file.close()

    xmax_list = []
    var_list = []        
    output_file = open(output_filename,'a')

    # Iterate over the all input files        
    for filename in input_filenames:

        file = open(filename,"rt")
        data = file.readlines()
        file.close()
        
        # Check, if the file is the sensor data file
        if data[0].find("OmniSim + CrystalWave Sensor Data") == -1 and \
    data[0].find("SGCHART:2 // signature:verNo") == -1:
            # Skipping file
            continue

        
        print("Analyzing file {},".format(filename)),
        
        x = []   # x input values 
        y = []   # y input values
        
        # Take the variable value from input     
        idx1 = data[1].find("=")      
        idx2 = data[1].find(")")      
        if idx1 != -1 and idx2 !=-1:
            var_value = float(data[1][idx1+1:idx2])
        else:
            # There is no data (Omnisim was probably not run in Scanner mode), 
            # so take the core file name as the var_value
            var_value = filename[:-4]
            print("[Warning - variable value was taken from the filename]"),
            # now try to convert to float
            try:
                var_value = float(filename[:-4])
            except ValueError:
                # Skip plots and regression, since there are no numeric var_values
                plot_partial = False
                plot_final = False
                do_linear_regression = False            

            # Do some rescaling etc.
            if var_name == "np_size":
                # Convert to nanometers
                var_value *= 1000 
            if var_name == "inglass" and var_value < 1:
                # Convert from [%/100] to [%], if necessary 
                #(some older results were given in [%/100])
                var_value *= 100 
            
            print("var_value = {},".format(var_value)),

        # Now read data
        if filename.endswith(".txt"):
            for line in data[5:]:
                linelist = line.strip().split('   ')
                x.append(round(float(linelist[0])*1000,2)) # Conversion to nanometers
                y.append(float(linelist[1]))
        else:
            for line in data[10:]:
                linelist = line.strip().split(',')
                if linelist[0] == "":
                    continue
                x.append(round(float(linelist[0])*1000,2)) # Conversion to nanometers
                y.append(float(linelist[1]))
            
     
        # Data from Omnisim are in the reverse wavelength order, so unreversing :)
        x.reverse()
        y.reverse()
        
        # Interpolating function (it looks that cubic variant work best)
        fint = interp1d(x, y, kind='cubic')

        # x values for interpolation
        xnew = np.linspace(xminint, xmaxint, num=intpoints, endpoint=True)
        
        # Interpolated y values
        yint = list(fint(xnew))
                
        ### Find all of the maxima 
        xmax = []
        for i in range(1,len(yint)-1):
            if yint[i-1]<yint[i]>yint[i+1]:
                xmax.append(round(xnew[i],2))
        
        # If no local maximum is found, skip the file
        if not xmax:
            print("no max in range [{}, {}]".format(xminint,xmaxint))
            continue
        
        print("max = ",xmax)
        
        # Append result to a list
        xmax_list.append(xmax)
        var_list.append(var_value)
            

        # Plot the absorption spectra for given variable value
        if plot_partial:
            plt.plot(xnew, fint(xnew))
            plt.plot(xmax, ymax, "x")
            if var_name == "np_size" and experimental_maxima.has_key(var_value):
                # If the experimental value exists for specific np_size, find it and plot 
                xmax_exp = experimental_maxima[var_value]
                plt.plot(xmax_exp,ymax,"x")
                plt.text("{}{}  Difference: {} (nm)".format(xmax_exp,ymax,abs(xmax_exp-xmax)))
            plt.title("Absorption spectra, {} = {}".format(var_name, var_value))
            plt.xlabel("Wavelength (nm)")
            plt.ylabel("Absorbance (a.u.)")
            plt.show()

        # Append result to output file
        output_file.write("{}    {}\n".format(var_value,str(xmax)[1:-1].replace(","," ")))
        
    output_file.close()

    if xmax_list:
        print("Output file {} has been saved.".format(output_filename))
    else:
        print("No proper input files were found, cleaning and exiting...")
        os.remove(output_filename)
        sys.exit()

    if len(xmax_list) < 2:
        do_linear_regression = False
        
    if xmax_list and plot_final:
        try:
            plt.plot(var_list, xmax_list, ".")
            if do_linear_regression:
                # Linear regression
                a,b = np.polyfit(var_list, xmax_list, 1)
                xmax_reg = [a*i+b for i in var_list]    
                plt.plot(var_list, xmax_reg)
            
            if var_name in ["trunc", "inglass"]:
                plot_title = "Position of the maximum of the absorption spectra \n for the truncated spheres of size 50 nm on glass"    
                plot_xlabel = "Sphere truncate factor (%)\n(0% - full sphere; 50% - half sphere, etc.)"
            elif var_name == "np_size":    
                plot_title = "Position of the maximum of the absorption spectra \n for the spheres of variable size in air"        
                plot_xlabel = "Sphere size (µm)"
            elif var_name == "al2o3":    
                plot_title = "Position of the maximum of the absorption spectra \n for the spheres covered by Al2O3 layer"
                plot_xlabel = "Thickness of the Al2O3 layer (µm)"
            else:
                plot_title = "Position of the maximum of the absorption spectra"    
                plot_xlabel = var_name
               
            plt.title(plot_title)
            plt.xlabel(plot_xlabel)
            plt.ylabel("Wavelength (nm)")
            plt.show()
            
        except ValueError:
            print("Different numbers of maxima in datasets, skipping plot.") 

    