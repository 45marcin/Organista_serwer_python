import   vlc, taglib, time, amixerControl,threading, singletonStatus, IOSingleton, json
class player:
    # Here will be the instance stored.
    __instance = None
    mediaPlayer = None
    nowPlaying = None
    stopPoints = []
    textPoints = []
    textPointsText = {}
    stopHere = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if player.__instance == None:
            player()

        return player.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if player.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.mediaPlayer = vlc.MediaPlayer("silent.mp3")
            player.__instance = self

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

    def setFile(self, patch):
        try:
            amixerControl.restoreVolBal()
            if self.mediaPlayer:
                self.mediaPlayer.stop()
                z = singletonStatus.SingletonStatus.getInstance()
                z.run = False
                io = IOSingleton.IOSingleton.getInstance()
                io.send("CanceledStop")
        except: None
        self.mediaPlayer = vlc.MediaPlayer(patch)
        if "mp4" in patch or "MP4"  in patch or "AVI"in patch or"avi"in patch or"mpeg"in patch or"MPEG" in patch or"flv"in patch or"FLV" in patch:
            self.mediaPlayer.set_fullscreen(b_fullscreen=True)
        try:
            tmp = taglib.File(patch)
            del self.stopPoints[:]
            for x in str(tmp.tags["LYRICS"][0]).split():
                self.stopPoints.append(float(x))
                print(x)
            self.stopPoints.sort()


        except:
            None
        try:
            del self.textPoints[:]
            self.textPointsText = json.loads(str(tmp.tags["COMMENT"][0]))
            for i in self.textPointsText:
                self.textPoints.append(float(i))
            self.textPoints.sort()
            print(self.textPoints)
        except:
            self.stopPoints.append(-1)
            self.textPointsText[-1] = None

        try:
            self.nowPlaying = tmp.tags["TITLE"]
        except:
            self.nowPlaying = patch
        try:
            self.WriteToFile(self.nowPlaying)
        except:
            None
        self.mediaPlayer.play()
        print(self.textPoints)
        return self.textPoints, self.textPointsText

    def isPlaying(self):
        if self.mediaPlayer.is_playing():
            return True
        else:
            return False

    def getPosition(self):
        if self.mediaPlayer.is_playing():
            return self.mediaPlayer.get_position()
        else:
            return 0

    def stopNow(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            io = IOSingleton.IOSingleton.getInstance()
            io.send("Stopped")
            z = singletonStatus.SingletonStatus.getInstance()
            z.run = False
        self.mediaPlayer = vlc.MediaPlayer("silent.mp3")

    def getLength(self):
        return self.mediaPlayer.get_length()

    def stopAt(self, point):
        z = singletonStatus.SingletonStatus.getInstance()
        while z.run:
            if point < self.mediaPlayer.get_position()*self.mediaPlayer.get_length()/1000:
                #self.mediaPlayer.pause()
                self.stopNowMute()
                break
            time.sleep(1/75)

    def stopWhenYouCan(self):
        for x in self.stopPoints:
            io = IOSingleton.IOSingleton.getInstance()
            #print(x)
            #print(self.mediaPlayer.get_position()*self.mediaPlayer.get_length())
            if x > self.mediaPlayer.get_position()*self.mediaPlayer.get_length()/1000:
                print("i will stop at: " + str(x))
                io.send("TimeStopON")
                z = singletonStatus.SingletonStatus.getInstance()
                z.run = True
                t = threading.Thread(target=self.stopAt, args={x})
                t.start()
                break

    def stopNowMute(self):
        amixerControl.autoMute()
        self.stopNow()
        amixerControl.restoreVolBal()


