from PIL import Image
import os, sys, readchar
from fnmatch import fnmatch

def main():
    '''
    Converts all .bmp files in the directory and it's subdirectories into the .png format
    
    Input: 
           .bmp files in the current directory and it's subdirectiories.       
    Output: 
           .png files.
    '''


    print("Press <cr> to continue or the other key to cancel.")
    ans = readchar.readkey()
    if ans != readchar.key.ENTER:
        print("Exiting...")
        sys.exit()

    root = '.'
    pattern = "*.bmp"

    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                print("Converting: {} => {}.png".format(name, name[:-4]))
                bmppath = os.path.join(path, name)
                img = Image.open(bmppath)
                pngpath = bmppath[:-4]+".png"
                img.save(pngpath, quality=100, optimize=True, progressive=True)
                os.remove(bmppath)
    print("Done.")
