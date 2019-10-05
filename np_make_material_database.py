import os, readchar
from np_ps import set, select_file

def main():
    '''
    This program creates the material description in the Omnisim material database file.

    Input 1 - real part of the refractive index as a function of wavelength (CSV):
    lambda [nm], Re(n)
    (...)

    Input 2 - imaginary part of the refractive index as a function of wavelength (CSV):
    lambda [nm], Im(n)
    (...)

    Example source of data: https://refractiveindex.info
    (n -> Re(n); k -> Im(n))
    To obtain material loss [1/cm], the Im(n) should be multiplied by 2 Pi * 10000 / lambda 
    '''

    # Data validity range [um]
    min_wavelength = 0.25 
    max_wavelength = 1.45

    # Collect input file names
    filename_re = select_file('csv', prompt="Select CSV file containing the Re(n): ")
    filename_im = select_file('csv', display=False, prompt="Select CSV file containing the Im(n): ")

    print("Current epsilon validity range (um): [{}, {}]".format(min_wavelength, max_wavelength))
    print("Press <cr> to accept, the other key to change")
        
    ans = readchar.readkey()
    if ans != readchar.key.ENTER:
        print()
        print("Modify range:")
        xminint = set("min wavelength (um)", min_wavelength)    
        xmaxint = set("max wavelength (um)", max_wavelength)
    
    material_name = input("Enter material name (<cr> = NEW_MATERIAL):")
    if not material_name:
        material_name = "NEW_MATERIAL"
    
    file = open(filename_re,"rt")
    data_re = file.readlines()
    file.close()

    file = open(filename_im,"rt")
    data_im = file.readlines()
    file.close()

    output_filename = "ps_refbase.mat"
    file = open(output_filename, "w")

    header = '''// Materials Parameters Database - PS
    //--------------------------------------------
    <materbase(2.21)>
    INCLUDE refbase.mat
    //--------------------------------------------
    '''
    file.write(header)


    file.write("BEGIN {}\n".format(material_name))

    file.write("RIX_EXPRESSION \"spline(lambda")
    for line in data_re:
        _lambda = float(line.split(",")[0])
        re = float(line.split(",")[1])
        file.write(", {}, {}".format(_lambda,re))
    file.write(")\"\n")
            
    file.write("MATLOSS_EXPRESSION \"4*_PI*10000/lambda * spline(lambda")
    for line in data_im:
        _lambda = float(line.split(",")[0])
        im = float(line.split(",")[1])
        file.write(", {}, {}".format(_lambda,im))
    file.write(")\"\n")

    file.write("LAMBDA_REF 0\n")
    file.write("LAMBDA_RANGE {} {}\n".format(min_wavelength, max_wavelength))
        
    file.write("END\n")
        
    print("Output file {} has been created.".format(output_filename))
