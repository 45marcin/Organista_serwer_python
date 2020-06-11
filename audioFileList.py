from os import *
import audioFile, fnmatch, sqlite3, os.path
from shutil import copy2
current_version = 201812
import sys


audioFiles = []
def importAudioFiles(Patch):
    try:
        for x in listdir(Patch):
            if not(path.isfile(Patch+"/"+x)):
                importAudioFiles(Patch+"/"+x)
            if Patch.__contains__("lost+found"):
                print("do nothing")
            elif fnmatch.fnmatch(x, '*.wav') or fnmatch.fnmatch(x, '*.WAV') or fnmatch.fnmatch(x, '*.flac') or fnmatch.fnmatch(x, '*.mp3') or fnmatch.fnmatch(x, '*.FLAC') or fnmatch.fnmatch(x, '*.MP3') or fnmatch.fnmatch(x, '*.MP4')or fnmatch.fnmatch(x, '*.mp4')or fnmatch.fnmatch(x, '*.AVI') or fnmatch.fnmatch(x, '*.avi') or fnmatch.fnmatch(x, '*.mpeg')or fnmatch.fnmatch(x, '*.MPEG')or fnmatch.fnmatch(x, '*.flv')or fnmatch.fnmatch(x, '*.FLV'):
                audioFiles.append(audioFile.audioFile(Patch+"/"+x))
            elif "version" in x:
                if int(x[7:13]) > current_version:
                    print(x[7:1])
                    update(Patch)
                else:
                    print("we have actually version of software")
    except: print("permission error on " + Patch)


def update(patch):
    try:
        for x in listdir(patch):
            if os.path.exists("/home/organista/Organista_python"+"/" + x):
                os.remove("/home/organista/Organista_python"+"/" + x)
                print("succesful removed")
            copy2(patch+"/"+x, "/home/organista/Organista_python")
            print(patch+"/"+x)
            copy2(patch + "/" + "tekst","/home/organista")
    except:
        None
        #WriteToFile("Update unsuccesfull")


def WriteToFile(text):
    while True:
        try:
            f= open("/home/organista/tekst", 'w')
            f.write(text)
            f.close()
            break
        except:
            None


def saveToDatabase():
    print("save to database")
    conn = sqlite3.connect("/home/organista/database.db")
    c = conn.cursor()
    c.execute('DELETE FROM audioFiles')
    for x in audioFiles:
        c.execute('INSERT INTO  audioFiles  VALUES (?, ?, ?, ?)', (str(x.title), str(x.album), str(x.artist), str(x.patch)))
    conn.commit()
    conn.close()

def createDatabaseTables():
    conn = sqlite3.connect("/home/organista/database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS  audioFiles (title text, album text, artist text, patch text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS  ulubione (title text, album text, artist text, patch text)''')
    conn.commit()
    conn.close()


def initialize():
    if not (os.path.exists("/home/organista/database.db")):
        createDatabaseTables()
    del audioFiles[:]
    rebuildDatabase()
    for i in audioFiles:
        print(i.patch)
    saveToDatabase()




def getFile(number):
    conn = sqlite3.connect("/home/organista/database.db")
    c = conn.cursor()
    for row in c.execute('SELECT * from audioFiles'):
        if int(row[3]) == number:
            return [row[4], row[0]]
            break
    conn.commit()
    conn.close()


def addToTop(patch):
    file = audioFile.audioFile(patch)
    conn = sqlite3.connect("/home/organista/database.db")
    c = conn.cursor()
    c.execute('INSERT INTO  ulubione  VALUES (?, ?, ?, ?)', (str(file.title), "ulubione", str(file.artist), str(file.patch)))
    print("add" + file.title + " - " + file.artist)
    conn.commit()
    conn.close()

def removeFromTop(patch):
    conn = sqlite3.connect("/home/organista/database.db")
    c = conn.cursor()
    print(patch)
    c.execute('DELETE FROM  ulubione  WHERE patch = ?', (patch,))
    conn.commit()
    conn.close()


def rebuildDatabase():
    importAudioFiles("/mnt")
    importAudioFiles("/home/organista/audioFiles")
    #importAudioFiles("/home/organista/update")



