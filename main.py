#! /usr/bin/python

import audioFileList, time, sqlite3, localSettings, amixerControl as mixer, socket, audioFile, time,  threading, IOSingleton, vlcPlayer, singletonStatus
import subprocess
import sys


from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

from kivy.config import Config
from shutil import copy2

def WriteToFile(text):
    while True:
        try:
            file = open('/home/organista/tekst', 'w')
            file.write(text)
            file.close()
            print(text)
            break
        except:
            None

version = 201812
WriteToFile("Organista")


localSettings.initialize()
audioFileList.initialize()


mixer.restoreVolBal()

io = IOSingleton.IOSingleton.getInstance()





def ioKeep():
            while 1:
                io2 = IOSingleton.IOSingleton.getInstance()
                try:
                    if not io2.connected:
                        io2.connect()
                        # print("server started")
                        # threading.main_thread(io = IOSingleton.IOSingleton())
                    else:
                        io2.send(" ")
                except:
                    io2.connect()
                time.sleep(2)

def sendMusic():
            tmp = IOSingleton.IOSingleton.getInstance()
            con = sqlite3.connect("/home/organista/database.db")
            c = con.cursor()
            try:
                for row in c.execute('SELECT * from audioFiles'):
                    tmp.send(audioFile.audioFile.serialize(row[0], row[1], row[2], row[3]))
                for row in c.execute('SELECT * from ulubione'):
                    tmp.send(audioFile.audioFile.serialize(row[0], "uuulubioneee", row[2], row[3]))
            except:
                print()
            time.sleep(1)
            tmp.send("SendedAll")

def playThis(number):
            z = number[8:len(number) - 1]
            p = vlcPlayer.player.getInstance()
            points, text = p.setFile(str(z))
            print("playing: ", p.nowPlaying)
            print(text)
            print(points)
            if len(points) is not 0:
                WriteToFile(text[str(int(points[0]))])
                i = 1
                time.sleep(3)
                while p.isPlaying():
                    time.sleep(0.5)
                    if i != len(points):
                        if points[i] < p.getPosition()*p.getLength()/1000:
                            try:
                                WriteToFile(text[str(points[i])])
                            except:
                                try:
                                    WriteToFile(text[str(int(points[i]))])
                                except:
                                    None
                            finally:
                                i = i+1
                WriteToFile(" ")
            else:
                WriteToFile(p.nowPlaying[0])
                time.sleep(4)
                while p.isPlaying():
                    time.sleep(4)
                WriteToFile(" ")


def ShowText(points, text):
            p = vlcPlayer.player.getInstance()



def addToTop(patch):
            z = patch[12:len(patch) - 1]
            audioFileList.addToTop(z)

def removeFromTop(patch):
            z = str(patch[17:len(patch) - 1])
            audioFileList.removeFromTop(z)

def send(msg):
            io.send(msg)

def status():
            while True:
                io2 = IOSingleton.IOSingleton.getInstance()
                p = vlcPlayer.player.getInstance()
                if io2.connected:
                    if p.isPlaying():
                        try:
                            io2.send("now" + str(p.nowPlaying)[2:len(str(p.nowPlaying)) - 2])
                            print("now: " + p.nowPlaying[2:len(p.nowPlaying) - 2])
                        except:
                            None
                    else:
                        io2.send("nowbezczynny")
                time.sleep(5)

def stopNow():
            p = vlcPlayer.player.getInstance()
            if p.isPlaying():
                p.stopNow()

def stopWhenYouCan():
            k = singletonStatus.SingletonStatus.getInstance()
            if k.run:
                k.run = False
                io.send("CanceledStopByUser")
            else:
                p = vlcPlayer.player.getInstance()
                p.stopWhenYouCan()



t = threading.Thread(target=ioKeep)
t.start()

z = threading.Thread(target=status)
z.start()


#g = threading.Thread(target=playThis, args={"12345678/run/media/marcin/RosiekM/organista/do_urzadzenia/_flac_/Ciebie_Boga_wysławiamy_170611-011.flac1"})
#g.start()

while 1:
            io = IOSingleton.IOSingleton.getInstance()
            z = io.receive()

            if z:
                print(z)
                if "Title1" in z:
                    break
                if "Title2" in z:
                    t = threading.Thread(target=send, args={"message"})
                    t.start()
                if "SendMeSomeMusic" in z:
                    sendMusic()
                if "PlayThis" in z:
                    t = threading.Thread(target=playThis, args={z})
                    t.start()
                if "connectionTest" in z:
                    t = threading.Thread(target=send, args={"responTest"})
                    t.start()
                if "volumeUp" in z:
                    t = threading.Thread(target=mixer.volumeUp())
                    t.start()
                if "volumeDown" in z:
                    t = threading.Thread(target=mixer.volumeDown())
                    t.start()
                if "balanceRight" in z:
                    t = threading.Thread(target=mixer.balanceRight())
                    t.start()
                if "balanceLeft" in z:
                    t = threading.Thread(target=mixer.balanceLeft())
                    t.start()
                if "removeThisFromTop" in z:
                    t = threading.Thread(target=removeFromTop, args={z})
                    t.start()
                if "addThisToTop" in z:
                    t = threading.Thread(target=addToTop, args={z})
                    t.start()
                if "stopNow" in z:
                    t = threading.Thread(target=stopNow)
                    t.start()
                if "stopWhenYouCan" in z:
                    t = threading.Thread(target=stopWhenYouCan())
                    t.start()
                if "rebuildDatabase" in z:
                    None
                if "ShowThis" in z:
                    k = z.replace("zxcv", "\n")
                    k = k[8: len(k)-1]
                    t = threading.Thread(target=WriteToFile, args={k})
                    t.start()
                if "Hide" in z:
                    t = threading.Thread(target=WriteToFile, args={" "})
                    t.start()



io.close()








