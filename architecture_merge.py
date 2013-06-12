#!/usr/bin/env python
# encoding: utf-8

###############################################################################
# architecture_merge.py
#
# python script to convert a .cpp file generated (at least initially) by faust
# (compiled without an architecture specified) and merge it with the relevant
# architecture file.
###############################################################################

from optparse import OptionParser
import re #regex
import os

def main():
    argParser = OptionParser(
        usage="usage: %prog [options] myfile.cpp path/to/architectureFile.cpp"
    )

    (options, args) = argParser.parse_args()

    # Open input file and architecture file, error if something is awry
    if len(args) == 2:
        print("Your C++ file:     {}".format(args[0]))
        try:
            myfile = open(args[0],"r")
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            exit(-1)
        if (os.path.splitext(os.path.basename(args[0]))[1]!=".cpp"):
            print("{} is not a .cpp file".format(os.path.basename(args[0])))
            exit(-1)
        print("Architecture file: {}".format(args[1]))
        try:
            archfile = open(args[1],"r")
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            exit(-1)
        if (os.path.splitext(os.path.basename(args[1]))[1]!=".cpp"):
            print("{} is not a .cpp file".format(os.path.basename(args[1])))
            exit(-1)
    else:
        argParser.print_help()
        exit(-1)

    # open output file
    try:
        outputfile = open(
                os.path.splitext(os.path.basename(args[0]))[0] + "_" +\
                os.path.splitext(os.path.basename(args[1]))[0] + ".cpp",
                "w")
    except IOError as e:
        print "Output file I/O error({0}): {1}".format(e.errno, e.strerror)
        exit(-1)

    # Right now, we don't do anything with the vector instrinsics.
    # Look for the <<includeIntrinsic>> tag and erase it.
    # Then go to the <<includeclass>> tag, erase it, and paste in the whole
    # input .cpp file.

    intrinsic = re.compile('<<includeIntrinsic>>')
    dspclass = re.compile('<<includeclass>>')

    for line in archfile:
        if ((intrinsic.findall(line)==[]) and (dspclass.findall(line)==[])):
            #add line from architecture file to output file
            outputfile.write(line)
        elif ((intrinsic.findall(line)==[]) and (dspclass.findall(line)!=[])):
            #add entire input .cpp file here
            for cppline in myfile:
                outputfile.write(cppline)

    myfile.close()
    archfile.close()
    outputfile.close()



if __name__ == "__main__":
    main()
