import os


def buildADSFilename(filename, streamname):
    return filename + ":" + streamname


decoy = "benign.txt"
resultfile = buildADSFilename(decoy, "results.txt")
commandfile = buildADSFilename(decoy, "commands.txt")

# Write commands to file for later execution
with open(commandfile, "w") as output:
    output.write("ipconfig")

# Run commands from file
with open(commandfile, "r") as c:
    for line in c:
        str(os.system(line + " >> " + resultfile))

# Read results
with open(resultfile, "r") as results:
    print(results.read())

# # Run executable
# exefile = "malicious.exe"
# exepath = os.path.join(os.getcwd(),buildADSFilename(decoy,exefile))
# os.system("wmic process call create "+exepath)
