import sys, readchar
from math import sqrt, log10
from np_ps import select_file

def main():
    '''
    Combines two .cht files containing field, absorbance or flux, e.g.
    - s: subtract: E = E1 - E2 (e.g. absorbance - reference absorbance)
    - u: unpolarize: |E| = sqrt(0.5|E_TE|^2 + 0.5|E_TM|^2) (e.g. EZ and HZ polarized fluxes)
    - a: calculate absorbance: E = log10(E1/E2) (e.g. input flux / output flux)
    - t: calculate transmitance: E = E2/E1 (e.g. output flux / input flux)

    Shortcut call: np [...] [s|u|a|t]

    Input:  
           Two .cht files from Omnisim (2D/1D).
    Output:
           .cht file with suffix "_x", where x is a selected option.
           In (u) case: "_ez" or "_hz" are removed from filename.
           In (a) case: prefix "abs_" is added instead of "_a" suffix.
    '''

    option = ""
    if len(args) > 0:
        option = args[0]
    if option not in ["s","u","a","t"]:
        print("Select operation, s:subtract, u:unpolarize, a:absorbance, t:transmitance; 0:exit")
        while option not in ["0","s","u","a","t"]:
            option = readchar.readkey()

    if option == "s":
        print("Subtracting.")
    elif option == "u":
        print("Unpolarizing.")
    elif option == "a":
        print("Calculating absorbance.")
    elif option == "t":
        print("Calculating transmitance.")
    elif option == "0":
        print("Exiting...")
        sys.exit()
    print()    
            
    # Read data from the input files
    filename1 = select_file('cht', prompt="Select first file:  ")
    filename2 = select_file('cht', display=False, prompt="Select second file: ")
    file = open(filename1,"rt")
    data1 = file.readlines()
    file.close()
    file = open(filename2,"rt")
    data2 = file.readlines()
    file.close()

    # Check if both files are of the same type
    if data1[0] != data2[0]:
        print("Input files are of a different type, exiting...")
        sys.exit()

    # Output filename
    output_filename = filename1[:-4]+"_"+option+".cht"
    if option == "u":
        output_filename = output_filename.replace("_ez", "")
        output_filename = output_filename.replace("_hz", "")
    if option == "a":
        output_filename = output_filename.replace("F_in", "abs")
        output_filename = output_filename.replace("_a", "")
    file = open(output_filename, "w")

    # 2D and 1D graphs have different file format
    if data1[0].startswith("SGCHART:2"):
        graph = "1D"
        data_separator = ","
        justify = 13
    elif data1[0].startswith("SGCHART2D(1.0)"):
        data_separator = " "
        graph = "2D"
        justify = 10
    else:
        print("Not a proper cht file, exiting...")
        sys.exit()

        
    # Parse the CHT files   
    for i in range(len(data1)):
        line1 = data1[i]
        line2 = data2[i]
        if i < 10:
            # Rewrite header to the output file
            if option == "a":
                line1 = line1.replace("In positive flux relative to Out positive flux from FDTD", "Absorbance")
                line1 = line1.replace("In positive flux from FDTD", "Absorbance")
                line1 = line1.replace("/um", "(µm)")
                line1 = line1.replace("Positive flux /W/um", "Absorbance (%/100)")
                line1 = line1.replace("Positive flux /dB", "Absorbance (%/100)")
            file.write(line1)
        else:    
            if graph == "2D":
                line1splitted = line1.split()
                line2splitted = line2.split()
            else:
                line1splitted = line1.split(data_separator)
                line2splitted = line2.split(data_separator)
            
            # x-value:
            x = line1splitted[0]
            
            # Sometimes x is read as a new line char. This is to avoid this
            if x.strip() == "":
                continue

            #if  x != line2splitted[0]:
            if round(float(x),3) != round(float(line2splitted[0]),3):
                print("x-axis is different in the input files, exiting...")
                sys.exit()    
            if graph == "2D":
                file.write(x.ljust(justify+1))
            else:
                file.write(x.ljust(justify))
            
            # y-values:
            y_values = len(line1splitted)
            if graph == "1D":
                # This is because of additional "," at the end of 1D data
                y_values = y_values - 1
            
            for j in range(1, y_values):
                y1 = float(line1splitted[j])
                y2 = float(line2splitted[j])
                if option == "u":
                    # |E| = sqrt(0.5|E_TE|^2 + 0.5|E_TM|^2)
                    y = sqrt(0.5*abs(y1)**2 + 0.5*abs(y2)**2)
                elif option == "s":
                    # E = E1 - E2
                    y = y1 - y2
                elif option == "a":
                    # E = log10(E1/E2)
                    try: 
                        y = log10(y1 / y2) 
                    except (ZeroDivisionError, ValueError):
                        y = 0
                elif option == "t":
                    # E = E2/E1
                    try:
                        y = y2 / y1
                    except ZeroDivisionError:
                        y = 0
                            
                file.write(data_separator + str(y).ljust(justify) + data_separator)
            
            file.write("\r\n")    

    file.close()
    print("Combined file saved as the {} file.".format(output_filename))
    
    