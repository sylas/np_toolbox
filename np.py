# Toolbox for running scripts for Omnisim

import sys

modules = \
{\
1:["np_change_plane","Change plane from xy to xz (and some other options) in the input file"],\
2:["np_truncate","Truncate the spheres by some factor in the input file"],\
3:["np_txt_to_cht","Convert .txt sensor data into the .cht format"],\
4:["np_combine_cht","Combine two .cht files to substract data, unpolarize, calculate absorbance and transmitance"],\
5:["np_abs_max","Finds maximum in the input .cht/.txt file (e.g. with absorbance)"],\
6:["np_plot_cht","Plots 1D data from the .cht file, and saves plot in the .png format"],\
}

if len(sys.argv) >= 2:
    try:
        choice = int(sys.argv[1])
    except ValueError:
        choice = 0
    if not choice in modules:
        print("Wrong module number, exiting...")
        sys.exit()                
else:    
    print("   ------------------------------")
    print("  | NP Toolbox for OmniSim by PS |")
    print("   ------------------------------")
    for k,v in modules.items():
        print(" {0}. {2} [{1}]".format(k, v[0], v[1]))
    print(" 0. Exit")

    print()
    choice = -1
    while not choice in modules and choice != 0:
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            choice = 0
        
    if choice == 0:
        print("Exiting...")
        sys.exit()
        
module_name = modules[choice][0]  
module = __import__(module_name)

# Pass the additional argument(s) to a module and run it
module.args = sys.argv[2:]
print("Running the {} module...".format(module_name))
print(module.main.__doc__)
try:
    module.main()
except KeyboardInterrupt:
    pass
print("Program completed.")
