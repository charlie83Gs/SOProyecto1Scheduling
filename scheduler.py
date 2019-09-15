import core
import sys

HELP = "\n -i <filename> specifies input file for the program \n -o <filename> specifies output file for the program \n -h displays this help screen \n \n The format of the input file is \n \n \t <period> <duration> NEWLINE \n \t <period> <duration> NEWLINE \n \n One line per process "
inputFile = None
outputFile = None
displayHelp = False

#load arguments from console
arguments = sys.argv[1:]

#print(arguments)

#excutes known commands
def proccessArg(args):
    global inputFile
    global outputFile
    global displayHelp
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
    elif(head == "-help" or head == "-h" or head == "-?"):
        print(HELP)
        displayHelp = True
        return args[1:]
    else: 
        print("Unknown command " + head)
        print("Or maybe you are missing an option after your " + head + " command")
        return args[1:]

#process input arguments
while(len(arguments) > 0):
    arguments = proccessArg(arguments)




if(inputFile != None and outputFile != None):
    schedule = ""
    try:
        iFile = open(inputFile,"r")
        decoder = core.FileDecoder()
        decoded = decoder.decodeFile(iFile)
        scheduler = core.RateMonotonicScheduler(300)
        timeline = scheduler.schedule(decoded)
        schedule = timeline.toString()
        iFile.close()
    except:
        print("failed to open input file")
    
    

    #create store file
    try:
        oFile = open(outputFile,"w+")
        oFile.write(schedule)
        oFile.close()
    except:
        print("failed to create output file")


if(inputFile == None and not displayHelp):
    print("mising input file must specify \n\t -i  <filename> ")
if(outputFile == None and not displayHelp):
    print("mising output file must specify \n\t -o  <filename> ")