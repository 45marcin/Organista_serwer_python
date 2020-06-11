import taglib

class audioFile:
    title = ""
    artist = ""
    album = ""
    patch = ""
    def __init__(self, Patch):
        tmp = taglib.File(Patch)
        try:self.title = tmp.tags["TITLE"]
        except:
            a = Patch.rfind("/")
            b = Patch.rfind(".")
            self.title = "  " + Patch[a + 1:b] + "  "
        try:self.artist = tmp.tags["ARTIST"]
        except:self.artist = ""
        try:self.album = tmp.tags["ALBUM"]
        except:self.album = ""
        self.patch = Patch


    @staticmethod
    def serialize(title, album, artist, Patch):
        Title = "mgraudioFile:{\"Title\":\"" + title[2:len(title)-2] + "\"";
        Album = "\"Album\":\"" + album[2:len(album)-2] + "\"";
        Artist = "\"Artist\":\"" + artist[2:len(artist)-2] + "\"";
        No = "\"No\":" + str(0);
        path = "\"path\":\"" + Patch + "\"}";
        print(Title + "," + Album + "," + Artist + "," + No + "," + path)
        return Title + "," + Album + "," + Artist + "," + No + "," + path;