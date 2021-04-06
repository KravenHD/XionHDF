import os
import enigma
import eBaseImpl
import eConsoleImpl
enigma.eTimer = eBaseImpl.eTimer
enigma.eConsoleAppContainer = eConsoleImpl.eConsoleAppContainer
from Components.config import config, ConfigSelection, ConfigSubsection, ConfigSelectionNumber, ConfigText, ConfigNumber
from Tools.Directories import fileExists
import re
from shutil import move, copy, rmtree, copytree
from ChangeSkin import ChangeSkin

skinSearchAndReplace = []
skin_lines = []
datei = "/usr/share/enigma2/XionHDF/skin.xml"
dateiTMP = datei + ".tmp"
FILE = "/usr/share/enigma2/XionHDF/skin.xml"
TMPFILE = FILE + ".tmp"
#############################################################

from config import *

#######################################################################

def debug(what):
        f = open('/tmp/xion_debug.txt', 'a+')
        f.write('[Xion Save Skin with:] ' + str(what) + '\n')
        f.close()

def appendSkinFile(appendFileName, skinPartSearchAndReplace=None):
        """
        add skin file to main skin content

        appendFileName:
         xml skin-part to add

        skinPartSearchAndReplace:
         (optional) a list of search and replace arrays. first element, search, second for replace
        """
        skFile = open(appendFileName, "r")
        file_lines = skFile.readlines()
        skFile.close()

        tmpSearchAndReplace = []

        if skinPartSearchAndReplace is not None:
                tmpSearchAndReplace = skinSearchAndReplace + skinPartSearchAndReplace
        else:
                tmpSearchAndReplace = skinSearchAndReplace

        for skinLine in file_lines:
                for item in tmpSearchAndReplace:
                        skinLine = skinLine.replace(item[0], item[1])
                skin_lines.append(skinLine)

def justSave():
        skin_mode = config.plugins.XionHDF.skin_mode.value
        if os.path.exists("/usr/share/enigma2/XionHDF/buttons"):
                rmtree("/usr/share/enigma2/XionHDF/buttons")
        if skin_mode == 'hd':
                daten = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/data/"
                #os.system("cp /usr/share/enigma2/XionHDF/buttonsets/hd/buttons /usr/share/enigma2/XionHDF")
                copytree('/usr/share/enigma2/XionHDF/buttonsets/hd/buttons', '/usr/share/enigma2/XionHDF/buttons', symlinks=False, ignore=None)
                os.system("cp /usr/share/enigma2/XionHDF/buttonsets/hd/infobar/*.* /usr/share/enigma2/XionHDF")
        else:
                pass

        if skin_mode == 'fullhd':
                daten = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/data/"
                #os.system("cp /usr/share/enigma2/XionHDF/buttonsets/fhd/buttons /usr/share/enigma2/XionHDF")
                copytree('/usr/share/enigma2/XionHDF/buttonsets/fhd/buttons', '/usr/share/enigma2/XionHDF/buttons', symlinks=False, ignore=None)
                os.system("cp /usr/share/enigma2/XionHDF/buttonsets/fhd/infobar/*.* /usr/share/enigma2/XionHDF")
        else:
                pass

#        for x in ["config"].list:
#                if len(x) > 1:
#                                x[1].save()
#                else:
#                                pass

        #global tag search and replace in all skin elements
        global skinSearchAndReplace
        FontStyleHeight_1 = config.plugins.XionHDF.FontStyleHeight_1.value
        skinSearchAndReplace.append(['<font filename="XionHDF/fonts/NotoSans-Regular.ttf" name="Regular" scale="95" />', '<font filename="XionHDF/fonts/NotoSans-Regular.ttf" name="Regular" scale="%s" />' % str(FontStyleHeight_1)])
        FontStyleHeight_2 = config.plugins.XionHDF.FontStyleHeight_2.value
        skinSearchAndReplace.append(['<font filename="XionHDF/fonts/NotoSans-Bold.ttf" name="Regular2" scale="95" />', '<font filename="XionHDF/fonts/NotoSans-Bold.ttf" name="Regular2" scale="%s" />' % str(FontStyleHeight_2)])
        skinSearchAndReplace.append(['name="XionBackground" value="#00', 'name="XionBackground" value="#' + config.plugins.XionHDF.BackgroundColorTrans.value])
        skinSearchAndReplace.append(['name="XionSelection" value="#000050EF', 'name="XionSelection" value="#' + config.plugins.XionHDF.SelectionBackground.value])
        skinSearchAndReplace.append(['name="XionFont1" value="#00ffffff', 'name="XionFont1" value="#' + config.plugins.XionHDF.Font1.value])
        skinSearchAndReplace.append(['name="XionFont2" value="#00ffffff', 'name="XionFont2" value="#' + config.plugins.XionHDF.Font2.value])
        skinSearchAndReplace.append(['name="XionSelFont" value="#00ffffff', 'name="XionSelFont" value="#' + config.plugins.XionHDF.SelectionFont.value])
        skinSearchAndReplace.append(['name="XionButtonText" value="#00ffffff', 'name="XionButtonText" value="#' + config.plugins.XionHDF.ButtonText.value])
        skinSearchAndReplace.append(['name="XionProgress" value="#00ffffff', 'name="XionProgress" value="#' + config.plugins.XionHDF.Progress.value])
        skinSearchAndReplace.append(['name="XionLine" value="#00ffffff', 'name="XionLine" value="#' + config.plugins.XionHDF.Line.value])
        skinSearchAndReplace.append(["movetype=running", config.plugins.XionHDF.RunningText.value])
        skinSearchAndReplace.append(["showOnDemand", config.plugins.XionHDF.ScrollBar.value])

        ### Selectionborder
        if not config.plugins.XionHDF.SelectionBorder.value == "none":
                selectionbordercolor = config.plugins.XionHDF.SelectionBorder.value
                borset = ("borset_" + selectionbordercolor + ".png")
                skinSearchAndReplace.append(["borset.png", borset])

        ### Header
        appendSkinFile(daten + "header_begin.xml")
        if not config.plugins.XionHDF.SelectionBorder.value == "none":
                appendSkinFile(daten + "header_middle.xml")
        appendSkinFile(daten + "header_end.xml")

        ###ChannelSelection
        appendSkinFile(daten + config.plugins.XionHDF.ChannelSelectionStyle.value + ".xml")

        ###Infobar_main
        appendSkinFile(daten + config.plugins.XionHDF.InfobarStyle.value + "_main.xml")

        ###weather-style
        appendSkinFile(daten + config.plugins.XionHDF.WeatherStyle.value + ".xml")

        ###Infobar_middle
        appendSkinFile(daten + config.plugins.XionHDF.InfobarChannelname.value + ".xml")

        ###Infobar_end
        appendSkinFile(daten + config.plugins.XionHDF.SIB.value + ".xml")

        ###Main XML
        appendSkinFile(daten + "main.xml")

        ###Plugins XML
        appendSkinFile(daten + "plugins.xml")

        ###emc-style
        appendSkinFile(daten + config.plugins.XionHDF.EMCStyle.value + ".xml")

        ###movie-style
        appendSkinFile(daten + config.plugins.XionHDF.MovieStyle.value + ".xml")

        ###skin-user
        try:
                appendSkinFile(daten + "skin-user.xml")
        except:
                pass
        ###skin-end
        appendSkinFile(daten + "skin-end.xml")

        xFile = open(dateiTMP, "w")
        for xx in skin_lines:
                xFile.writelines(xx)
        xFile.close()

        Instance = ChangeSkin(1)

        if fileExists(TMPFILE):
           if fileExists(FILE):
              move(TMPFILE, FILE)
              debug('mv : ' + TMPFILE + ' to ' + FILE + "\n")
           else:
              os.rename(TMPFILE, FILE)
              debug('rename : ' + TMPFILE + ' to ' + FILE + "\n")
        return 0
