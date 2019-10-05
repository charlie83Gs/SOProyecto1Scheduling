import core
import sys

HELP = "\n -i <filename> \tspecifies input file for the program "
HELP += "\n -o <filename> \tspecifies output file for the program "
HELP += "\n -t <duration> \tspecifies the time this program is going to simulate process scheduling "
HELP += "\n -h \t\tdisplays this help screen  "
HELP += "\n \n To select algorith use the flags "
HELP += "\n\n \t -edf \tfor EDF algorithm "
HELP += "\n \t -rtm \tfor Rate Monotonic Algorithm "
HELP += "\n \n The format of the input file is "
HELP += "\n \n \t <period> <duration>"
HELP += "\n \t <period> <duration> "
HELP += "\n \t <period> <duration> "
HELP += "\n \n One line per process"
inputFile = None
outputFile = None
displayHelp = False
algorithm = None
duration = 300

#load arguments from console
arguments = sys.argv[1:]

#print(arguments)

#TODO

#excutes known commands
def proccessArg(args):
    global inputFile
    global outputFile
    global displayHelp
    global algorithm
    global duration
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
    elif(head == "-t"):
        duration = int(args[1]) 
        return args[2:]
    elif(head == "-edf" or head == "-rtm"):
        algorithm = head
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
    '''
    iFile = open(inputFile,"r")
    decoder = core.FileDecoder()
    decoded = decoder.decodeFile(iFile)

    #create scheduler
    scheduler =  core.EdfScheduler(duration)
    if(algorithm == "-rtm"):
        scheduler = core.RateMonotonicScheduler2(duration)
        
    timeline = scheduler.schedule(decoded)
    schedule = timeline.toString(duration)
    iFile.close()
    '''
    try:
        iFile = open(inputFile,"r")
        decoder = core.FileDecoder()
        decoded = decoder.decodeFile(iFile)

        #create scheduler
        scheduler =  core.EdfScheduler(duration)
        if(algorithm == "-rtm"):
            scheduler = core.RateMonotonicScheduler2(duration)
        
        timeline = scheduler.schedule(decoded)
        schedule = timeline.toString(duration)
        
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
