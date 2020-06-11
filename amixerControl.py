import os, localSettings, IOSingleton, time





def setVolBal(vol, bal, tmp):
    x = int(65536*10**(vol/20))
    if bal > 0:
        xbal = int(x*10**(-bal/20))
    else:
        xbal = int(x*10**(bal/20))
    #print(x)


    io = IOSingleton.IOSingleton.getInstance()
    if bal > 0:
        os.popen("amixer sset Master "+str(xbal)+","+str(x))
        io.send("volgłośność: "+str(int(vol))+"dB organista: " + str(-bal) + "dB")
    elif bal <0:
        os.popen("amixer sset Master "+str(x)+","+str(xbal))
        io.send("volgłośność: "+str(int(vol))+"dB organy: " + str(bal) + "dB")
    else:
        os.popen("amixer sset Master " + str(x) + "," + str(x))
        io.send("volgłośność: "+str(int(vol))+"dB")
    if tmp:
        localSettings.saveVolume(vol)
        localSettings.saveBalance(bal)


def volumeUp():
    vol = localSettings.readVolume()
    bal = localSettings.readBalance()
    if vol == 0:
        setVolBal(vol,bal, True)
    else:
        setVolBal(vol + 1,bal, True)


def volumeDown():
    vol = localSettings.readVolume()
    bal = localSettings.readBalance()
    if vol == -97:
        setVolBal(-97,bal, True)
    else:
        setVolBal((vol - 1),bal, True)

def balanceRight():
    bal = localSettings.readBalance()
    vol = localSettings.readVolume()
    if bal == 60:
        setVolBal(vol, 60, True)
    else:
        setVolBal(vol, bal+1, True)


def balanceLeft():
    bal = localSettings.readBalance()
    vol = localSettings.readVolume()
    if bal == -60:
        setVolBal(vol, bal, True)
    else:
        setVolBal(vol, bal - 1, True)

def restoreVolBal():
    bal = localSettings.readBalance()
    vol = localSettings.readVolume()
    setVolBal(vol, bal, False)

def autoMute():
    bal = localSettings.readBalance()
    vol = localSettings.readVolume()
    vol2 = vol
    while vol2 > (vol - 15):
        vol2 = vol2-0.3
        setVolBal(vol2, 60, False)
        time.sleep(0.005)
    return True



