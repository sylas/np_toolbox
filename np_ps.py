#from builtins import input
import os, sys

def set(name, value, typeof=None):
    '''Sets the new value to a variable named "name".'''
    if typeof == None:
        typeof = str(type(value))
        idx1 = typeof.index("'")
        idx2 = typeof.index("'", idx1+1)
        typeof = typeof[idx1+1:idx2]
    print ("<{}> {} = {} | ".format(typeof, name, value), end="")
    ans = input("Enter new value, or <cr> to keep default: ")
    if (ans == ""):
        return value
    if "int" in typeof:
        try:
            new_value = int(ans)
        except ValueError:
            new_value = value
            print("Wrong number entered, keeping the original value.")
    elif "float" in typeof:
        try:
            new_value = float(ans)
        except ValueError:
            new_value = value
            print("Wrong number entered, keeping the original value.")
    elif "str" in typeof:
        new_value = str(ans)
    elif "bool" in typeof:
        new_value = ans
        if new_value not in ["True", "False"]:
            new_value = value
            print("Wrong boolean entered, keeping the original value.")            
    if new_value != value:
        print ("Set <{}> {} = {}".format(typeof, name, new_value))
    return new_value

def select_file(extension, display=True, prompt="Select file: "):
    '''Allows to select file from a list of files of a given extension'''
    input_filenames = []
    for filename in os.listdir("."):
        if filename.endswith("."+extension):
            input_filenames.append(filename)
    input_filenames.sort()
    
    if display:
        print("Input files list:")
        if len(input_filenames) > 8:
            # Display files in columns
            input_filenames_A = input_filenames[:len(input_filenames)//2]
            input_filenames_B = input_filenames[len(input_filenames)//2:]
            print(input_filenames_A)
            print(input_filenames_B)
            print()
            maxlen = len(max(input_filenames_A, key=len))
            nl = 1
            nr = len(input_filenames_A)+1
            for i,j in zip(input_filenames_A, input_filenames_B):
                print("%d. %s\t%d. %s" % (nl,i.ljust(maxlen, " "), nr, j))
                nl = nl+1
                nr = nr+1
            if len(input_filenames_B) > len(input_filenames_A):
                print("%d. %s" % (nr,input_filenames_B[-1:][0]))
        else:
            # One-column
            for i in range(len(input_filenames)):
                print ("{}. {}".format(i+1,input_filenames[i]))
        
        print("0. Exit")
    
    # Collect the filename
    idx = -1
    while idx not in range(len(input_filenames)+1):
        try:
            idx = int(input(prompt))
        except ValueError:
            idx = 0
    if idx == 0:
        print("Exiting...")
        sys.exit()
    filename = input_filenames[idx-1]

    return(filename)
    