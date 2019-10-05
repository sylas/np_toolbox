## A toolbox for [OmniSim](https://www.photond.com/products/omnisim.htm)

Toolbox allows for manipulating input and output files. Especially useful when simulating electromagnetic field propagation through ellipsoids (e.g. nanoparticles on a substrate).

In use at Gdańsk University of Technology,
[Department of Theoretical Physics and Quantum Information](https://ftims.pg.edu.pl/katedra-fizyki-teoretycznej-i-informatyki-kwantowej/research). Written in Python 3.

Main features:

* Make material database using the refractive index
* Change plane from xy to xz (and some other options)
* Truncate the spheres by some factor
* Convert .txt sensor data into the .cht format
* Combine two .cht files to substract data, unpolarize, calculate absorbance and transmitance
* Find local maxima in the .cht/.txt files with absorbance, and plot the result if possible
* Plot (and save in the .png format) the .cht file
