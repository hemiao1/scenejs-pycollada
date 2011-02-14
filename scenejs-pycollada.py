#! /usr/bin/env python

# Main entry point for the scenejs-pycollada translator utility.

import collada
import sys
import getopt
import os.path
from translator import translate
from stream import ScenejsJsonStream, ScenejsJavascriptStream, ScenejsBinaryStream

def main(argv):
    # Get the command-line options given to the program
    try:                                
        opts, args = getopt.getopt(argv, "hvdo:", ["help", "verbose", "output="]) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)
    
    debug = 0
    outputFormat = ScenejsJavascriptStream
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "Translate a Collada file to a JSON formatted SceneJS file"
            usage()     
            sys.exit()
        elif opt == '-d':
            debug = 1
        elif opt in ("-o", "--output"):
            try: 
              outputFormat = { 
                "json":   ScenejsJsonStream,
                "js":     ScenejsJavascriptStream,
                "binary": ScenejsBinaryStream }[arg]
            except KeyError:
              print "Unknown output format '" + arg + "'"
              usage()
              sys.exit(2)
        elif opt in ("-v", "--verbose"): 
            global _verbose
            _verbose = 1
        else:
            print "Unknown option supplied '" + opt + "'"
            usage()
            sys.exit(2)

    if not args:
        print "No input files specified"
        usage()
        sys.exit(2)
    
    # Load and translate each file specified
    for filename in args:
        # Check whether the file exists and try to load it into a collada object
        if not os.path.isfile(filename):
            print "'" + filename + "' is not a valid file path."
            sys.exit(2)
        colladaObj = collada.Collada(filename, ignore=[collada.DaeUnsupportedError])
        
        # Create an output file write the SceneJS scene to
        basePath = os.path.splitext(filename)[0]
        outputFile = open(basePath + "." + outputFormat.fileExtension,"w")
        translate(outputFormat(outputFile), colladaObj, debug)

def usage():
    print "Usage: "
    print "    python scenejs-collada --help"
    print "    python scenejs-collada [OPTION]... [FILE]..."
    print ""
    print "Miscelaneous options:"
    print "  -h, --help                     Display this help message"
    print "  -v, --verbose                  Display verbose warnings and translation information"
    print "  --libraries-only               TODO: export only libraries, excluding scenes"
    print "  --geometry-only                TODO: export only geometry"
    print "  --geometry-materials           TODO: geometry and materials only"
    print "  -o [FORMAT], --output=[FORMAT] Use the specified output mode, FORMAT may be any one of the following"
    print "                                 json   - Raw JSON data is output"
    print "                                 js     - JavaScript code is output and nodes created"
    print "                                 binary - Output JavaScript code along with accompanying binary"
    print "  -d                             Turn on debug mode"

if __name__ == "__main__":
    main(sys.argv[1:])
