import os 

def main():
    '''
    Program converts the .txt file with sensor data from OmniSim, to the corresponding .cht file.
    
    Input:  
        .txt file
    Output:
        .cht file
    '''

    # Collect the .txt filenames
    input_filenames = []
    for filename in os.listdir("."):
        if filename.endswith(".txt"):
            input_filenames.append(filename)

    if len(input_filenames) == 0:
        print("No .txt files found in the directory, exiting...")
        sys.exit()

    # Output file header templates
    cht_line1 = 'SGCHART:2 // signature:verNo\n'
    cht_line2 = '"{}" // title\n'
    cht_line3 = '1 // oneXdata\n'
    cht_line4 = '//----------------------------------------------------------\n'
    cht_line5 = 'XSCALE "{} {}" "0.3" "0.7" 1 0 0 6 // title min max position logscale tickstyle nano\n'
    cht_line6 = 'YSCALE "{} {}" "0" "1" 1 0 0 6 // title min max position logscale tickstyle nano\n'
    cht_line7 = 'YSCALE "" "" "" 2 0 0 6 // title min max position logscale tickstyle nano\n'
    cht_line8 = 'YREAL {} "{} {}" "" "" 1 0 0 6 0 4 0 1 1 // numPts title min max position logscale tickstyle nano linestyle linecolour markstyle plotstyle include\n'
    cht_line9 = '//----------------------------------------------------------\n'
    cht_line10 = '        Xvals,      Yvals1 ,\n'
    cht_data_lines = '{:13s},{:13s},\n'
        
    for filename in input_filenames:
    
        file = open(filename,"rt")
        data = file.readlines()
        file.close()

        if data[0].strip() != "OmniSim + CrystalWave Sensor Data":
            continue
            
        file = open(filename[:-4]+".cht","w")
        
        title = data[1].strip()
        x_title = data[3].split("   ")[1].strip()
        y_title = data[3].split("   ")[2].strip()
        x_unit = data[4].split()[0].strip()
        y_unit = data[4].split()[1].strip()
        no_data = len(data)-5

        # Header
        file.write(cht_line1)
        file.write(cht_line2.format(title))
        file.write(cht_line3)
        file.write(cht_line4)
        file.write(cht_line5.format(x_title,x_unit))
        file.write(cht_line6.format(y_title,y_unit))
        file.write(cht_line7)
        file.write(cht_line8.format(no_data, y_title,y_unit))
        file.write(cht_line9)
        file.write(cht_line10)
        
        # Main data
        for xy in data[5:]:
            x = float(xy.split()[0])
            y = float(xy.split()[1])
            file.write(cht_data_lines.format(str(x),str(y)))
               
        file.close()
        
