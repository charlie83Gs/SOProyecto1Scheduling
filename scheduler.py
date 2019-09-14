import core
import sys

HELP = "\n -i <filename> specifies input file for the program \n -o <filename> specifies output file for the program \n -h displays this help screen \n \n The format of the input file is \n \n \t <period> <duration> NEWLINE \n \t <period> <duration> NEWLINE \n \n One line per process "
inputFile = ""
outputFile = ""

#load arguments from console
arguments = sys.argv[1:]

print(arguments)

#excutes known commands
def proccessArg(args):
    global inputFile
    if(len(args) <= 0):
        return []
    head = args[0]

    if(head == "-input" or head == "-i"  and len(args) > 1):
        inputFile = args[1] 
        #print("f " + inputFile)       
        return args[2:]
    elif(head == "-output" or head == "-o" and len(args) > 1):
        outputFile = args[1]  
        return args[2:]
    elif(head == "-help" or head == "-h"):
        print(HELP)
        return args[1:]
    else: 
        print("Unknown command " + head)
        print("Or maybe you are missing a option after your " + head + " command")
        return args[1:]

#process input arguments
while(len(arguments) > 0):
    arguments = proccessArg(arguments)

pFile = open(inputFile,"r")
decoder = core.FileDecoder()
decoded = decoder.decodeFile(pFile)
scheduler = core.RateMonotonicScheduler(300)
scheduler.schedule(decoded)
pFile.close() 