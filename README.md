## A toolbox for [OmniSim](https://www.photond.com/products/omnisim.htm)

Toolbox allows for manipulating input and output files. 
Especially useful when simulating electromagnetic field propagation through ellipsoids (e.g. nanoparticles - NPs) on a plane.

In use at Gdańsk University of Technology,
[Department of Theoretical Physics and Quantum Information](https://ftims.pg.edu.pl/katedra-fizyki-teoretycznej-i-informatyki-kwantowej/research). Written in Python 3.

Main features:

* Make material database for a material of a given refractive index
* Change NPs plane from xy to xz, adjust project and device numbers, NPs layer index, NPs plane baseline, optionally inverse the x and z axes and reverse x-values
* Truncate and/or flatten NPs by some factor, with given standard deviation
* Convert .txt sensor data into the .cht format
* Combine two .cht files to substract, unpolarize, calculate absorbance and transmitance
* Find local maxima in the .cht/.txt files (e.g. with absorbance), and plot the result, if possible
* Plot 2D or color map graph from the .cht file, then save it in the .png format 
