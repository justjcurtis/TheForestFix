import winreg
import re
import os

#VARS
regex = re.compile('(?:SharedSection=1024,)(\d+)')

key = "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\SubSystems"
saveState=os.getenv('APPDATA') + "\\forestfix.state"
hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_ALL_ACCESS)

#FUNCS
def getState():
    result = winreg.QueryValueEx(hKey, "Windows")
    res=regex.search(result[0])
    return res.group(1)

def firstRun():
    writer = open(saveState, "w")
    writer.write(getState())
    writer.close()

def runCommand(command):
    os.system(command)

def setForest(state):
    result = winreg.QueryValueEx(hKey, "Windows")
    old = ","+getState()+","
    new = ","+state+","
    res = result[0].replace(old,new)
    winreg.SetValueEx(hKey, "Windows", 0, winreg.REG_EXPAND_SZ, res)
    command = "bcdedit /set IncreaseUserVa " + state
    runCommand(command)

#MAIN
def main():
    if not os.path.isfile(saveState):
        firstRun()
    if getState() == "4096":
        print("You're currently in The Forest.")
        print("Would you like to leave?(y/n)")
        go=input("=> ")
        if go=="y" or go=="Y" or go=="":
            print("Leaving Forest..")
            reader = open(saveState, "r")
            s = reader.read()
            setForest(s)
            if getState() == "4096":
                print("unable to leave forest")
                print("try running as administrator")
                input("Press any key to exit")
                exit()
            print("Got out with no problems")
            input("Press any key to exit")
            exit()
        else:
            print("You will remain in the forest")
            input("Press any key to exit")
            exit()

    else:
        print("You're currently out of The Forest.")
        print("Would you like to enter?(y/n)")
        go=input("=> ")
        if go=="y" or go=="Y" or go=="":
            print("Entering Forest..")
            setForest("4096")
            if getState() != "4096":
                print("unable to enter forest")
                print("try running as administrator")
                input("Press any key to exit")
                exit()
            print("Got in with no problems")
            input("Press any key to exit")
            exit()
        else:
            print("You will remain outside of the forest")
            input("Press any key to exit")
            exit()

#RUN
main()
