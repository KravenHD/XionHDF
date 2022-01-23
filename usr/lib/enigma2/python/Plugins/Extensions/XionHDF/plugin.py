#######################################################################
#
# XionHDF by Team Kraven
#
# Thankfully inspired by:
# MyMetrix
# Coded by iMaxxx (c) 2013
#
# This plugin is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#######################################################################

import os
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger, ConfigSelectionNumber
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system
from shutil import move, copy, rmtree, copytree, copyfile
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
import gettext
import time
import subprocess
import re
import requests
import json
from boxbranding import getBoxType, getImageArch
from enigma import ePicLoad, getDesktop, eConsoleAppContainer
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from ChangeSkin import *
FILE = "/usr/share/enigma2/XionHDF/skin.xml"
TMPFILE = FILE + ".tmp"
#############################################################

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("XionHDF", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/XionHDF/locale/"))

def _(txt):
    t = gettext.dgettext("XionHDF", txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t

def translateBlock(block):
    for x in TranslationHelper:
        if block.__contains__(x[0]):
            block = block.replace(x[0], x[1])
    return block

#############################################################

config.plugins.XionHDF = ConfigSubsection()

config.plugins.XionHDF.weather_city = ConfigText(default="", visible_width=250, fixed_size=False)

config.plugins.XionHDF.refreshInterval = ConfigSelectionNumber(min=10, max=240, stepwidth=5, default=60, wraparound=True)
config.plugins.XionHDF.weather_realtek_latlon = ConfigText(default="")
config.plugins.XionHDF.weather_foundcity = ConfigText(default="")

config.plugins.XionHDF.System = ConfigSelection(default="openhdf", choices=[
                                ("openhdf", _(" "))
                                ])

config.plugins.XionHDF.BackgroundColorTrans = ConfigSelection(default="1c", choices=[
                                ("00", _("Off")),
                                ("1c", _("Lower")),
                                ("2d", _("Low")),
                                ("4a", _("Middle")),
                                ("6c", _("Medium")),
                                ("8c", _("High"))
                                ])
ColorList = []
ColorList.append(("00F0A30A", _("Amber")))
ColorList.append(("00B27708", _("Amber dark")))
ColorList.append(("001B1775", _("Blue")))
ColorList.append(("000E0C3F", _("Blue dark")))
ColorList.append(("007D5929", _("Brown")))
ColorList.append(("003F2D15", _("Brown dark")))
ColorList.append(("000050EF", _("Cobalt")))
ColorList.append(("00001F59", _("Cobalt dark")))
ColorList.append(("001BA1E2", _("Cyan")))
ColorList.append(("000F5B7F", _("Cyan dark")))
ColorList.append(("00FFEA04", _("Yellow")))
ColorList.append(("00999999", _("Grey")))
ColorList.append(("003F3F3F", _("Grey dark")))
ColorList.append(("0070AD11", _("Green")))
ColorList.append(("00213305", _("Green dark")))
ColorList.append(("001DFF00", _("Neon green")))
ColorList.append(("00FFFF00", _("Neon yellow")))
ColorList.append(("006D8764", _("Olive")))
ColorList.append(("00313D2D", _("Olive dark")))
ColorList.append(("00C3461B", _("Orange")))
ColorList.append(("00892E13", _("Orange dark")))
ColorList.append(("00F472D0", _("Pink")))
ColorList.append(("00723562", _("Pink dark")))
ColorList.append(("00E51400", _("Red")))
ColorList.append(("00330400", _("Red dark")))
ColorList.append(("00000000", _("Black")))
ColorList.append(("00647687", _("Steel")))
ColorList.append(("00262C33", _("Steel dark")))
ColorList.append(("006C0AAB", _("Violet")))
ColorList.append(("001F0333", _("Violet dark")))
ColorList.append(("00ffffff", _("White")))

config.plugins.XionHDF.SelectionBackground = ConfigSelection(default="00C3461B", choices=ColorList)

config.plugins.XionHDF.Font1 = ConfigSelection(default="00ffffff", choices=ColorList)

config.plugins.XionHDF.Font2 = ConfigSelection(default="00ffffff", choices=ColorList)

config.plugins.XionHDF.SelectionFont = ConfigSelection(default="00ffffff", choices=ColorList)

config.plugins.XionHDF.ButtonText = ConfigSelection(default="00ffffff", choices=ColorList)

config.plugins.XionHDF.Progress = ConfigSelection(default="00C3461B", choices=ColorList)

config.plugins.XionHDF.Line = ConfigSelection(default="00ffffff", choices=ColorList)

SelectionBorderList = [("none", _("Off"))]
SelectionBorderList = ColorList + SelectionBorderList
config.plugins.XionHDF.SelectionBorder = ConfigSelection(default="none", choices=SelectionBorderList)

config.plugins.XionHDF.EMCStyle = ConfigSelection(default="emc-nocover", choices=[
                                ("emc-nocover", _("No cover")),
                                ("emc-smallcover", _("Small cover")),
                                ("emc-bigcover", _("Big cover")),
                                ("emc-verybigcover", _("Very big cover")),
                                ("emc-listbigcover", _("List big cover")),
                                ("emc-minitv", _("MiniTV"))
                                ])

config.plugins.XionHDF.MovieStyle = ConfigSelection(default="movieselectionnocover", choices=[
                                ("movieselectionnocover", _("No cover")),
                                ("movieselectionsmallcover", _("Small cover")),
                                ("movieselectionbigcover", _("Big cover")),
                                ("movieselectionlistbigcover", _("List big cover")),
                                ("movieselectionminitv", _("MiniTV"))
                                ])

config.plugins.XionHDF.InfobarStyle = ConfigSelection(default="infobar-style-xpicon", choices=[
                                ("infobar-style-xpicon", _("X-Picon"))
                                ])

config.plugins.XionHDF.SIB = ConfigSelection(default="infobar-style-xpicon_end1", choices=[
                                ("infobar-style-xpicon_end1", _("Only current program")),
                                ("infobar-style-xpicon_end2", _("Top/Bottom")),
                                ("infobar-style-xpicon_end3", _("Left/Right"))
                                ])

config.plugins.XionHDF.ChannelSelectionStyle = ConfigSelection(default="channelselection-twocolumns", choices=[
                                ("channelselection-twocolumns", _("Two columns")),
                                ("channelselection-threecolumns", _("Three columns")),
                                ("channelselection-xpicon", _("X-Picon")),
                                ("channelselection-minitv", _("MiniTV"))
                                ])

config.plugins.XionHDF.InfobarChannelname = ConfigSelection(default="infobar-style-xpicon_middle1", choices=[
                                ("infobar-style-xpicon_middle1", _("Small")),
                                ("infobar-style-xpicon_middle2", _("Big")),
                                ("infobar-style-xpicon_middleP", _("Poster")),
                                ("infobar-style-xpicon_middle3", _("Off"))
                                ])

config.plugins.XionHDF.RunningText = ConfigSelection(default="movetype=running", choices=[
                                ("movetype=running", _("On")),
                                ("movetype=none", _("Off"))
                                ])

config.plugins.XionHDF.WeatherStyle = ConfigSelection(default="weather-off", choices=[
                                ("weather-off", _("Off")),
                                ("weather-info", _("Infos in place of weather")),
                                ("weather-big", _("Big")),
                                ("weather-slim", _("Slim")),
                                ("weather-small", _("Small"))
                                ])

config.plugins.XionHDF.ScrollBar = ConfigSelection(default="showNever", choices=[
                                ("showOnDemand", _("On")),
                                ("showNever", _("Off"))
                                ])

config.plugins.XionHDF.FontStyleHeight_1 = ConfigSelectionNumber(default=95, stepwidth=1, min=0, max=120, wraparound=True)
config.plugins.XionHDF.FontStyleHeight_2 = ConfigSelectionNumber(default=95, stepwidth=1, min=0, max=120, wraparound=True)

################# bmeminfo ###########################################
if fileExists('/proc/bmeminfo'):
    entrie = os.popen('cat /proc/bmeminfo').read()
    mem = entrie.split(':', 1)[1].split('k')[0]
    bmem = int(mem) / 1024
else:
    mem_info = []
    entrie = os.popen('cat /proc/cmdline').read()

    if getBoxType() in ('vusolo4k', 'zgemmah7', 'zgemmah9t', 'zgemmah9s', 'e4hdultra'):
        mem = re.findall('_cma=(.*?)M', entrie)
    else:
        mem = re.findall('bmem=(.*?)M', entrie)

    for info in mem:
        mem_info.append((info))

    if len(mem_info) > 1:
        bmem = int(mem_info[0]) + int(mem_info[1])
    else:
        if getImageArch() == 'cortexa15hf-neon-vfpv4' or getBoxType() in ('zgemmah9s', 'e4hdultra'):
            bmem = 250
        else:
            bmem = int(mem_info[0])

SkinModeList = []
SkinModeList.append(("hd", _("HD Skin 1280 x 720")))
if bmem > 180:
    SkinModeList.append(("fullhd", _("FullHD Skin 1920 x 1080")))
#if bmem > 440:
#   if getBoxType() == 'vusolo4k':
#      SkinModeList.append(("uhd", _("UHD Skin 3840 x 2160")))
        #SkinModeList.append(("4khd", _("4K Skin 4096 x 2160")))
#if bmem > 880:
    #SkinModeList.append(("fulluhd", _("FullUHD Skin 7680 x 4320")))
    #SkinModeList.append(("8khd", _("8K Skin 8192 x 4320")))
#SkinModeList.append(("userdef", _("User Selection")))

config.plugins.XionHDF.skin_mode = ConfigSelection(default="hd", choices=SkinModeList)
#######################################################################

class XionHDF(ConfigListScreen, Screen):
    skin = """
<screen name="XionHDF-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#00000000">
<eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
<eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
<eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text="Reboot" transparent="1" />
<widget name="config" position="70,75" size="708,572" itemHeight="27" font="Regular;23" transparent="1" enableWrapAround="1" scrollbarMode="showOnDemand" zPosition="1" backgroundColor="#00000000" />
<eLabel position="70,12" size="708,46" text="XionHDF - Konfigurationstool" font="Regular; 34" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
<eLabel position="847,200" size="368,2" backgroundColor="#00ffffff" />
<eLabel position="847,409" size="368,2" backgroundColor="#00ffffff" />
<eLabel position="845,200" size="2,211" backgroundColor="#00ffffff" />
<eLabel position="1215,200" size="2,211" backgroundColor="#00ffffff" />
<eLabel backgroundColor="#00000000" position="0,0" size="1280,720" transparent="0" zPosition="-9" />
<ePixmap pixmap="XionHDF/buttonsets/hd/buttons/key_red1.png" position="22,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
<ePixmap pixmap="XionHDF/buttonsets/hd/buttons/key_green1.png" position="222,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
<ePixmap pixmap="XionHDF/buttonsets/hd/buttons/key_yellow1.png" position="422,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
<ePixmap pixmap="XionHDF/buttonsets/hd/buttons/key_blue1.png" position="622,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
<widget source="global.CurrentTime" render="Label" position="1154,16" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
<convert type="ClockToText">Default</convert>
</widget>
<eLabel position="830,80" size="402,46" text="XionHDF" font="Regular; 36" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
<eLabel position="845,130" size="372,46" text="Version: 1.4" font="Regular; 30" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
<ePixmap backgroundColor="#00000000" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/openhdf.png" position="847,202" size="368,207" zPosition="-9" />
<widget name="helperimage" position="847,202" size="368,207" zPosition="1" backgroundColor="#00000000" />
<widget source="help" render="Label" position="847,450" size="368,168" font="Regular2;20" backgroundColor="#00000000" foregroundColor="#00ffffff" halign="center" valign="top" transparent="1" />
<eLabel backgroundColor="#00ffffff" position="0,64" size="1280,2" zPosition="2" />
<eLabel backgroundColor="#00ffffff" position="0,656" size="1280,2" zPosition="2" />
</screen>
"""

    def __init__(self, session, args=None, picPath=None):
        self.skin_lines = []
        Screen.__init__(self, session)
        self.session = session
        self.datei = "/usr/share/enigma2/XionHDF/skin.xml"
        self.dateiTMP = self.datei + ".tmp"
        self.daten = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/data/"
        self.komponente = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/comp/"
        self.picPath = picPath
        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self["helperimage"] = Pixmap()
        self["help"] = StaticText()

        ConfigListScreen.__init__(
                        self,
                        self.mylist(),
                        session=session,
                        on_change=self.__selectionChanged
                        )

        self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "InputActions", "ColorActions"], {"left": self.keyLeft, "down": self.keyDown, "up": self.keyUp, "right": self.keyRight, "red": self.exit, "yellow": self.reboot, "blue": self.showInfo, "green": self.save, "cancel": self.exit, "ok": self.keyOK}, -1)
        self.onLayoutFinish.append(self.UpdatePicture)

    def mylist(self):
        list = []
        #list.append(getConfigListEntry(_("_____________________________ Styles __________________________________"), config.plugins.XionHDF.System, _(" ")))
        list.append(getConfigListEntry(_("Skinmode"), config.plugins.XionHDF.skin_mode, _("This option set the resolution of skin.")))
        list.append(getConfigListEntry(_("Running text"), config.plugins.XionHDF.RunningText, _("This option activates the running text for some parts of skin.")))
        list.append(getConfigListEntry(_("Scrollbars"), config.plugins.XionHDF.ScrollBar, _("This option activates the scrollbars for some parts of skin.")))
        list.append(getConfigListEntry(_("Background transparency"), config.plugins.XionHDF.BackgroundColorTrans, _("This option activate/deactive/change the background transparency of skin.")))
        list.append(getConfigListEntry(_("ChannelSelection"), config.plugins.XionHDF.ChannelSelectionStyle, _("This option changes the view of channellist.")))
        list.append(getConfigListEntry(_("Infobar channelname"), config.plugins.XionHDF.InfobarChannelname, _("This option activates the channelname within the infobar.\nFor using Poster, you need a drive as HDD to save the pictures.")))
        list.append(getConfigListEntry(_("Second Infobar"), config.plugins.XionHDF.SIB, _("This option changes the view of second infobar.")))
        list.append(getConfigListEntry(_("EnhancedMovieCenter"), config.plugins.XionHDF.EMCStyle, _("This option changes the view of cover inside from EnhancedMovieCenter.")))
        list.append(getConfigListEntry(_("MovieSelection"), config.plugins.XionHDF.MovieStyle, _("This option changes the view of cover inside from MovieSelection.")))
        #list.append(getConfigListEntry(_("_____________________________ Weather _________________________________"), ))
        list.append(getConfigListEntry(_("Weather"), config.plugins.XionHDF.WeatherStyle, _("This option activate/deactive/change the weather on top inside the infobar.")))
        list.append(getConfigListEntry(_("Weather ID"), config.plugins.XionHDF.weather_city, _("Here you can insert your city, district, zip code or alltogether.\nLeave blank to automatically detect your location via the IP adress.\nPress OK to insert your location manually.")))
        list.append(getConfigListEntry(_("Refresh interval (in minutes)"), config.plugins.XionHDF.refreshInterval, _("Here you can change how often the weather is refreshed in the background.")))
        #list.append(getConfigListEntry(_("_____________________________ Colors __________________________________"), ))
        list.append(getConfigListEntry(_("Line"), config.plugins.XionHDF.Line, _("Please select the color of lines inside the skin.")))
        list.append(getConfigListEntry(_("Listselection"), config.plugins.XionHDF.SelectionBackground, _("Please select the color of listselection inside the skin.")))
        list.append(getConfigListEntry(_("Listselection border"), config.plugins.XionHDF.SelectionBorder, _("Please select the bordercolor of selection bars or deactivate borders completely.")))
        list.append(getConfigListEntry(_("Progress-/Volumebar"), config.plugins.XionHDF.Progress, _("Please select the color of progress- and volumebar inside the skin.")))
        list.append(getConfigListEntry(_("Primary font"), config.plugins.XionHDF.Font1, _("Please select the color of primary font inside the skin.")))
        list.append(getConfigListEntry(_("Secondary font"), config.plugins.XionHDF.Font2, _("Please select the color of secundary font inside the skin.")))
        list.append(getConfigListEntry(_("Listselection font"), config.plugins.XionHDF.SelectionFont, _("Please select the color of listselection font inside the skin.")))
        list.append(getConfigListEntry(_("Button text"), config.plugins.XionHDF.ButtonText, _("Please select the color of button text inside the skin.")))
        list.append(getConfigListEntry(_("Font normal height in %"), config.plugins.XionHDF.FontStyleHeight_1, _("This option changes the height of normal font.")))
        list.append(getConfigListEntry(_("Font bold height in %"), config.plugins.XionHDF.FontStyleHeight_2, _("This option changes the height of bold font.")))
        return list

    def __selectionChanged(self):
        returnValue = self["config"].getCurrent()
        self.debug(str(returnValue))
        if str(returnValue) == 'Weather ID' or str(returnValue) == 'Wetter ID':
            self["config"].setList(self.mylist())

    def updateHelp(self):
        cur = self["config"].getCurrent()
        if cur:
            self["help"].text = cur[2]

    def GetPicturePath(self):
        try:
            returnValue = self["config"].getCurrent()[1].value
            if returnValue == "hd":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/hd.jpg"
            elif returnValue == "fullhd":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/fullhd.jpg"
            elif returnValue == "openhdf":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/openhdf.png"
            elif returnValue == "00F0A30A":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/amber.jpg"
            elif returnValue == "00B27708":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/amber_dark.jpg"
            elif returnValue == "001B1775":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/blue.jpg"
            elif returnValue == "000E0C3F":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/blue_dark.jpg"
            elif returnValue == "007D5929":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/brown.jpg"
            elif returnValue == "003F2D15":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/brown_dark.jpg"
            elif returnValue == "000050EF":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/cobalt.jpg"
            elif returnValue == "00001F59":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/cobalt_dark.jpg"
            elif returnValue == "001BA1E2":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/cyan.jpg"
            elif returnValue == "000F5B7F":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/cyan_dark.jpg"
            elif returnValue == "00FFEA04":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/yellow.jpg"
            elif returnValue == "00999999":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/grey.jpg"
            elif returnValue == "003F3F3F":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/grey_dark.jpg"
            elif returnValue == "0070AD11":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/green.jpg"
            elif returnValue == "00213305":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/green_dark.jpg"
            elif returnValue == "001DFF00":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/neon_green.jpg"
            elif returnValue == "00FFFF00":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/neon_yellow.jpg"
            elif returnValue == "006D8764":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/olive.jpg"
            elif returnValue == "00313D2D":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/olive_dark.jpg"
            elif returnValue == "00C3461B":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/orange.jpg"
            elif returnValue == "00892E13":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/orange_dark.jpg"
            elif returnValue == "00F472D0":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/pink.jpg"
            elif returnValue == "00723562":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/pink_dark.jpg"
            elif returnValue == "00E51400":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/red.jpg"
            elif returnValue == "00330400":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/red_dark.jpg"
            elif returnValue == "00000000":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/black.jpg"
            elif returnValue == "00647687":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/steel.jpg"
            elif returnValue == "00262C33":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/steel_dark.jpg"
            elif returnValue == "006C0AAB":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/violet.jpg"
            elif returnValue == "001F0333":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/violet_dark.jpg"
            elif returnValue == "00ffffff":
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/white.jpg"
            else:
                path = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/" + returnValue + ".jpg"
            if fileExists(path):
                return path
            else:
                return "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/fb.jpg"
        except:
            return "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/fb.jpg"

    def UpdatePicture(self):
        self.PicLoad.PictureData.get().append(self.DecodePicture)
        self.onLayoutFinish.append(self.ShowPicture)

    def ShowPicture(self):
        self.PicLoad.setPara([self["helperimage"].instance.size().width(), self["helperimage"].instance.size().height(), self.Scale[0], self.Scale[1], 0, 1, "#002C2C39"])
        self.PicLoad.startDecode(self.GetPicturePath())

    def DecodePicture(self, PicInfo=""):
        ptr = self.PicLoad.getData()
        self["helperimage"].instance.setPixmap(ptr)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.ShowPicture()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.ShowPicture()

    def keyDown(self):
        self["config"].instance.moveSelection(self["config"].instance.moveDown)
        self.ShowPicture()
        self.updateHelp()

    def keyUp(self):
        self["config"].instance.moveSelection(self["config"].instance.moveUp)
        self.ShowPicture()
        self.updateHelp()

    def keyOK(self):
        if isinstance(self["config"].getCurrent()[1], ConfigText):
            from Screens.VirtualKeyBoard import VirtualKeyBoard
            text = self["config"].getCurrent()[1].value
            title = _("Enter the city name of your location:")
            self.session.openWithCallback(self.keyVirtualKeyBoardCallBack, VirtualKeyBoard, title=title, text=text)

    def keyVirtualKeyBoardCallBack(self, callback):
        try:
            if callback:
                self["config"].getCurrent()[1].value = callback
            else:
                pass
        except:
            pass

    def reboot(self):
        restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
        restartbox.setTitle(_("Restart GUI"))

    def showInfo(self):
        self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

    def getDataByKey(self, list, key):
        for item in list:
            if item["key"] == key:
                return item
        return list[0]

    def getFontStyleData(self, key):
        return self.getDataByKey(channelselFontStyles, key)

    def getFontSizeData(self, key):
        return self.getDataByKey(channelInfoFontSizes, key)

    def save(self):
        self.skin_mode = config.plugins.XionHDF.skin_mode.value
        if os.path.exists("/usr/share/enigma2/XionHDF/buttons"):
            rmtree("/usr/share/enigma2/XionHDF/buttons")
        if self.skin_mode == 'hd':
            self.daten = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/data/"
            copytree('/usr/share/enigma2/XionHDF/buttonsets/hd/buttons', '/usr/share/enigma2/XionHDF/buttons', symlinks=False, ignore=None)
            os.system("cp /usr/share/enigma2/XionHDF/buttonsets/hd/infobar/*.* /usr/share/enigma2/XionHDF")
            os.system("cp /usr/share/enigma2/XionHDF/extensions/hd/*.* /usr/share/enigma2/XionHDF/extensions")
            os.system("cp /usr/share/enigma2/XionHDF/icons/hd/*.* /usr/share/enigma2/XionHDF/icons")
        else:
            pass

        if self.skin_mode == 'fullhd':
            self.daten = "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/data/"
            copytree('/usr/share/enigma2/XionHDF/buttonsets/fhd/buttons', '/usr/share/enigma2/XionHDF/buttons', symlinks=False, ignore=None)
            os.system("cp /usr/share/enigma2/XionHDF/buttonsets/fhd/infobar/*.* /usr/share/enigma2/XionHDF")
            os.system("cp /usr/share/enigma2/XionHDF/extensions/fhd/*.* /usr/share/enigma2/XionHDF/extensions")
            os.system("cp /usr/share/enigma2/XionHDF/icons/fhd/*.* /usr/share/enigma2/XionHDF/icons")
        else:
            pass

        for x in self["config"].list:
            if len(x) > 1:
                x[1].save()
            else:
                pass

        try:
            #global tag search and replace in all skin elements
            self.skinSearchAndReplace = []
            self.FontStyleHeight_1 = config.plugins.XionHDF.FontStyleHeight_1.value
            self.skinSearchAndReplace.append(['<font filename="XionHDF/fonts/NotoSans-Regular.ttf" name="Regular" scale="95" />', '<font filename="XionHDF/fonts/NotoSans-Regular.ttf" name="Regular" scale="%s" />' % str(self.FontStyleHeight_1)])
            self.FontStyleHeight_2 = config.plugins.XionHDF.FontStyleHeight_2.value
            self.skinSearchAndReplace.append(['<font filename="XionHDF/fonts/NotoSans-Bold.ttf" name="Regular2" scale="95" />', '<font filename="XionHDF/fonts/NotoSans-Bold.ttf" name="Regular2" scale="%s" />' % str(self.FontStyleHeight_2)])
            self.skinSearchAndReplace.append(['name="XionBackground" value="#00', 'name="XionBackground" value="#' + config.plugins.XionHDF.BackgroundColorTrans.value])
            self.skinSearchAndReplace.append(['name="XionSelection" value="#000050EF', 'name="XionSelection" value="#' + config.plugins.XionHDF.SelectionBackground.value])
            self.skinSearchAndReplace.append(['name="XionFont1" value="#00ffffff', 'name="XionFont1" value="#' + config.plugins.XionHDF.Font1.value])
            self.skinSearchAndReplace.append(['name="XionFont2" value="#00ffffff', 'name="XionFont2" value="#' + config.plugins.XionHDF.Font2.value])
            self.skinSearchAndReplace.append(['name="XionSelFont" value="#00ffffff', 'name="XionSelFont" value="#' + config.plugins.XionHDF.SelectionFont.value])
            self.skinSearchAndReplace.append(['name="XionButtonText" value="#00ffffff', 'name="XionButtonText" value="#' + config.plugins.XionHDF.ButtonText.value])
            self.skinSearchAndReplace.append(['name="XionProgress" value="#00ffffff', 'name="XionProgress" value="#' + config.plugins.XionHDF.Progress.value])
            self.skinSearchAndReplace.append(['name="XionLine" value="#00ffffff', 'name="XionLine" value="#' + config.plugins.XionHDF.Line.value])
            self.skinSearchAndReplace.append(["movetype=running", config.plugins.XionHDF.RunningText.value])
            self.skinSearchAndReplace.append(["showOnDemand", config.plugins.XionHDF.ScrollBar.value])

            ### Selectionborder
            if not config.plugins.XionHDF.SelectionBorder.value == "none":
                self.selectionbordercolor = config.plugins.XionHDF.SelectionBorder.value
                self.borset = ("borset_" + self.selectionbordercolor + ".png")
                self.skinSearchAndReplace.append(["borset.png", self.borset])

            ### Header
            self.appendSkinFile(self.daten + "header_begin.xml")
            if not config.plugins.XionHDF.SelectionBorder.value == "none":
                self.appendSkinFile(self.daten + "header_middle.xml")
            self.appendSkinFile(self.daten + "header_end.xml")

            ###ChannelSelection
            self.appendSkinFile(self.daten + config.plugins.XionHDF.ChannelSelectionStyle.value + ".xml")

            ###Infobar_main
            self.appendSkinFile(self.daten + config.plugins.XionHDF.InfobarStyle.value + "_main.xml")

            ###weather-style
            self.appendSkinFile(self.daten + config.plugins.XionHDF.WeatherStyle.value + ".xml")

            ###Infobar_middle
            self.appendSkinFile(self.daten + config.plugins.XionHDF.InfobarChannelname.value + ".xml")

            ###Infobar_end
            self.appendSkinFile(self.daten + config.plugins.XionHDF.SIB.value + ".xml")

            ###Main XML
            self.appendSkinFile(self.daten + "main.xml")

            ###Plugins XML
            self.appendSkinFile(self.daten + "plugins.xml")

            ###emc-style
            self.appendSkinFile(self.daten + config.plugins.XionHDF.EMCStyle.value + ".xml")

            ###movie-style
            self.appendSkinFile(self.daten + config.plugins.XionHDF.MovieStyle.value + ".xml")

            ###skin-user
            try:
                self.appendSkinFile(self.daten + "skin-user.xml")
            except:
                pass
            ###skin-end
            self.appendSkinFile(self.daten + "skin-end.xml")

            xFile = open(self.dateiTMP, "w")
            for xx in self.skin_lines:
                xFile.writelines(xx)
            xFile.close()

            #move(self.dateiTMP, self.datei)

            #system('rm -rf ' + self.dateiTMP)
            Instance = ChangeSkin(self.session)

            if fileExists(TMPFILE):
                if fileExists(FILE):
                    move(TMPFILE, FILE)
                    self.debug('mv : ' + TMPFILE + ' to ' + FILE + "\n")
                else:
                    rename(TMPFILE, FILE)
                    self.debug('rename : ' + TMPFILE + ' to ' + FILE + "\n")
        except:
            self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)

        ### Get weather data to make sure the helper config values are not empty
        self.get_weather_data()
        self.restart()

    def restart(self):
        configfile.save()
        restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _("GUI needs a restart to apply a new skin.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
        restartbox.setTitle(_("Restart GUI"))

    def appendSkinFile(self, appendFileName, skinPartSearchAndReplace=None):
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
            tmpSearchAndReplace = self.skinSearchAndReplace + skinPartSearchAndReplace
        else:
            tmpSearchAndReplace = self.skinSearchAndReplace

        for skinLine in file_lines:
            for item in tmpSearchAndReplace:
                skinLine = skinLine.replace(item[0], item[1])
            self.skin_lines.append(skinLine)


    def restartGUI(self, answer):
        if answer is True:
            config.skin.primary_skin.setValue("XionHDF/skin.xml")
            config.skin.save()
            configfile.save()
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def exit(self):
        for x in self["config"].list:
            if len(x) > 1:
                x[1].cancel()
            else:
                pass
        self.close()

    def debug(self, what):
        f = open('/tmp/xion_debug.txt', 'a+')
        f.write('[PluginScreen]' + str(what) + '\n')
        f.close()

    def get_weather_data(self):
        self.city = ''
        self.lat = ''
        self.lon = ''
        self.accu_id = ''

        if config.plugins.XionHDF.weather_city.value == '':
            self.get_latlon_by_ip()
        else:
            self.get_latlon_by_name()

        config.plugins.XionHDF.weather_foundcity.value = self.city
        config.plugins.XionHDF.weather_foundcity.save()
        config.plugins.XionHDF.weather_realtek_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), lang[:2])
        #print config.plugins.XionHDF.weather_realtek_latlon.value
        config.plugins.XionHDF.weather_realtek_latlon.save()

    def get_latlon_by_ip(self):
        #print "try to found weather via IP"
        try:
            res = requests.get('http://ip-api.com/json/?lang=de&fields=status,city,lat,lon,country', timeout=3)
            data = res.json()
            if data['status'] == 'success':
                self.country = data['country']
                self.city1 = data['city']
                self.city = str(self.city1) + ' / ' + str(self.country)
                self.lat = data['lat']
                self.lon = data['lon']
                self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
            else:
                self.preview_text = _('No data for IP')
                self.session.open(MessageBox, _("Error retrieving weather data!"), MessageBox.TYPE_ERROR)
        except:
            self.preview_text = _('No data for IP')
            self.session.open(MessageBox, _("Error retrieving weather data!"), MessageBox.TYPE_ERROR)

#############################################################
# location detect via bing maps #

    def get_latlon_by_name(self):
        #print "try to found weather via Name"
        try:
            name = config.plugins.XionHDF.weather_city.value
            res = requests.request('get', 'http://dev.virtualearth.net/REST/v1/Locations/' + name + '?&key=AiU2Jrx506GVhCwH5kw6h6KLiYGbgwWDtYUFvDxYNYQ5yAcb81_RxlIMmFOLB8Rr', timeout=3)
            data = res.json()
            self.city1 = data['resourceSets'][0]['resources'][0]['address']['locality']
            self.city2 = data['resourceSets'][0]['resources'][0]['address']['countryRegion']
            self.lat = data['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates'][0]
            self.lon = data['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates'][1]
            self.city = str(self.city1) + ' / ' + str(self.city2)
        except:
            #self.session.open(MessageBox, _("Error retrieving weather data,\nfallback to IP!"), MessageBox.TYPE_ERROR)
            self.get_latlon_by_ip()

#############################################################
# location detect via mapquestapi #

#       def get_latlon_by_name(self):
#               #print "try to found weather via Name"
#               try:
#                       name = config.plugins.XionHDF.weather_city.value
#                       res = requests.request('get', 'http://www.mapquestapi.com/geocoding/v1/address?key=46e6mCww60Y4X2m8pttGoNTrdsPqedKW&location=' + name, timeout=3)
#                       data = res.json()
#                       self.city = data['results'][0]['locations'][0]['adminArea4']
#                       self.lat = data['results'][0]['locations'][0]['latLng']['lat']
#                       self.lon = data['results'][0]['locations'][0]['latLng']['lng']
#               except:
#                       self.session.open(MessageBox, _("Error retrieving weather data,\nfallback to IP!"), MessageBox.TYPE_ERROR)
#                       self.get_latlon_by_ip()

#############################################################

def main(session, **kwargs):
    session.open(XionHDF, "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/Xioncolors.jpg")

def Plugins(**kwargs):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        return [PluginDescriptor(name="XionHDF", description=_("Configuration tool for XionHDF"), where=PluginDescriptor.WHERE_PLUGINMENU, icon='pluginfhd.png', fnc=main)]
    else:
        return [PluginDescriptor(name="XionHDF", description=_("Configuration tool for XionHDF"), where=PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main)]
