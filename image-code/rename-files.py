import glob
import os
import sys

def renamefiles(path, prefix):
    g = glob.glob(path + "*.jpg")
    for i in range(len(g)):
        os.rename(g[i], os.path.join(path,prefix + str(i+1) + ".jpg"))

if 3 != len(sys.argv):
    print "Usage: python " + sys.argv[0] + " PATH PREFIX"
    exit(1)
print "renaming the files ..."
renamefiles(sys.argv[1], sys.argv[2])

