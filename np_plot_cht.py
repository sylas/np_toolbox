import matplotlib as mpl
import matplotlib.pyplot as plt
from np_ps import select_file

def main():
    '''
    Plots data from the .cht file and saves it as the png file.
    
    Input: 
           .cht file from Omnisim. 
           Shortcut: np [...] gamma
    Output: 
           .png graphics file with a plot.
    '''

    # Read data from input file
    filename = select_file('cht')
    file = open(filename,"rt")
    data = file.readlines()
    file.close()
    data = [x.strip() for x in data] 

    # Output filename
    output_filename = filename[:-4]+".png"

    # Graph and font size
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 15
    fig_size[1] = 9
    plt.rcParams["figure.figsize"] = fig_size
    plt.rcParams.update({'font.size': 22})

    xtable = []
    ytable = []

    # The main part - plots
    if data[0].find("SGCHART:2 // signature:verNo") != -1:
        # 1D data
            
        # Plot title
        index1 = data[1].find('"')+1
        index2 = data[1].find('"',index1)
        plot_title = data[1][index1:index2]
        plot_title = plot_title.replace("In positive flux relative to Out positive flux from FDTD","Absorbance ") 
        # Keep the space (hack ;) )!

        # x label
        index1 = data[4].find('"')+1
        index2 = data[4].find('"',index1)
        plot_x_label = data[4][index1:index2]
        plot_x_label = plot_x_label.replace(" /fs"," (fs)")
        plot_x_label = plot_x_label.replace(" /um"," (µm)")

        # y label
        index1 = data[5].find('"')+1
        index2 = data[5].find('"',index1)
        plot_y_label = data[5][index1:index2]
        plot_y_label = plot_y_label.replace("/V/m","(V/m)")
        plot_y_label = plot_y_label.replace("/A/m","(A/m)")
        plot_y_label = plot_y_label.replace("/J/m","(J/m)")
        plot_y_label = plot_y_label.replace(" /W/m"," (W/m)")
        plot_y_label = plot_y_label.replace(" /W/um"," (W/µm)")
        plot_y_label = plot_y_label.replace(" /W"," (W)")

        # Read data
        for i in range(10,len(data)):

            linesplitted = data[i].split(",")
                
            # x-value:
            try:
                x = float(linesplitted[0])
            except ValueError:
                continue
            
            # y-value:
            try:
                y = float(linesplitted[1])
            except ValueError:
                continue
            
            if plot_title == "Absorbance":
                y = y *100
                plot_y_label = "Absorbance (%)"
                            
            xtable.append(x)
            ytable.append(y)

        plt.plot(xtable,ytable)
        plt.title(plot_title, loc="left", pad="30")
        plt.xlabel(plot_x_label)
        plt.ylabel(plot_y_label)    
        plt.savefig(output_filename)
        plt.show()
            
    else:    
        # 2D data

        ztable = []
            
        # Plot title
        index1 = data[1].find('"')+1
        index2 = data[1].find('"',index1)
        plot_title = data[1][index1:index2]

        # x label
        index1 = data[2].find('"')+1
        index2 = data[2].find('"',index1)
        plot_x_label = data[2][index1:index2]
        plot_x_label = plot_x_label.replace("/um","(µm)")

        # y label
        index1 = data[3].find('"')+1
        index2 = data[3].find('"',index1)
        plot_y_label = data[3][index1:index2]
        plot_y_label = plot_y_label.replace("/um","(µm)")
        
        # z label (bar)
        index1 = data[4].find('"')+1
        index2 = data[4].find('"',index1)
        plot_z_label = data[4][index1:index2]
        plot_z_label = plot_z_label.replace("/V/m/THz","(V/m/THz)")
        plot_z_label = plot_z_label.replace("/A/m/THz","(A/m/THz)")
        plot_z_label = plot_z_label.replace("/J/m^3/THz","(J/m^3/THz)")
        plot_z_label = plot_z_label.replace("/W/m^2/THz","(W/m^2/THz)")
        
        ytable = data[8].split()
        ytable = [float(x) for x in ytable]

        # Number of y-data
        ycount = int(data[5].split()[0])
        
        for i in range(10,len(data)):

            if len(data[i]) == 0:
                # Skipping empty lines (appears sometimes, maybe due to line endings?)
                continue

            linesplitted = data[i].split()
                
            # x-value:
            try:
                x = float(linesplitted[0])
            except ValueError:
                continue
            
            # z-values:
            try:
                z = []
                for j in range(1,ycount+1):
                    z.append(float(linesplitted[j]))
            except ValueError:
                continue
                        
            xtable.append(x)
            ztable.append(z)
            
        # Borders of the graph
        extent_data = (round(ytable[0],1),round(ytable[-1],1),round(xtable[0],1),round(xtable[-1],1))
                
        # Initial gamma for color normalization
        if len(args) > 0:
            try:
                gamma = args[0]
            except:
                gamma = 1.0
        else:
            gamma = 1.0

        while gamma != "": 
        
            try:
                gamma = float(gamma)
            except ValueError:
                gamma = 1.0
            
            # Normalization
            norm = mpl.colors.PowerNorm(gamma=gamma)

            plt.clf() # Clear the previous graph
            plt.imshow(ztable, origin="lower", norm=norm, cmap='hot', extent=extent_data, interpolation='nearest', 
                        aspect='auto')
            plt.colorbar().set_label(plot_z_label)
            plt.xlabel(plot_x_label)
            plt.ylabel(plot_y_label)
            plt.title(plot_title, loc="left", pad="30")    
            plt.savefig(output_filename)
            plt.ion() # This is for non-blocking .show()
            plt.show()
        
            print("Current gamma = {}.".format(gamma))
            gamma = input("Input new gamma [0,1] or <cr> to accept current value: ")
        
    print("Plot saved to the {} file.".format(output_filename))
