import sqlite3, math, os.path

def createDatabesSettingsTables():
    conn = sqlite3.connect('/home/organista/settings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS  Settings (volume real, balance real)''')
    c.execute('insert  into  Settings VALUES (0, 0)')
    conn.commit()
    conn.close()


def saveVolume(vol):
    conn = sqlite3.connect('/home/organista/settings.db')
    c = conn.cursor()
    c.execute('UPDATE Settings SET volume = ?', [str(vol)])
    conn.commit()
    conn.close()


def saveBalance(bal):
    conn = sqlite3.connect('/home/organista/settings.db')
    c = conn.cursor()
    c.execute('UPDATE Settings SET balance = ?', [str(bal)])
    conn.commit()
    conn.close()


def readVolume():
    conn = sqlite3.connect('/home/organista/settings.db')
    c = conn.cursor()
    for row in c.execute("select volume from Settings"):
        return int(row[0])
    conn.close()


def readBalance():
    conn = sqlite3.connect('/home/organista/settings.db')
    c = conn.cursor()
    for row in c.execute("select balance from Settings"):
        return int(row[0])
    conn.close()


def initialize():
    if not (os.path.exists("/home/organista/settings.db")):
        createDatabesSettingsTables()