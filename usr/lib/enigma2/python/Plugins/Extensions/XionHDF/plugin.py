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

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger, ConfigSelectionNumber
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system
from shutil import move
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
import gettext
from enigma import ePicLoad, getDesktop, eConsoleAppContainer
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS

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
config.plugins.XionHDF.weather_city = ConfigNumber(default="638242")
config.plugins.XionHDF.refreshInterval = ConfigNumber(default="60")
				
config.plugins.XionHDF.System = ConfigSelection(default="openhdf", choices = [
				("openhdf", _(" "))
				])
				
config.plugins.XionHDF.BackgroundColorTrans = ConfigSelection(default="1c", choices = [
				("00", _("off")),
				("1c", _("lower")),
				("2d", _("low")),
				("4a", _("middle")),
				("6c", _("medium")),
				("8c", _("high"))
				])
				
config.plugins.XionHDF.SelectionBackground = ConfigSelection(default="00C3461B", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00FFEA04", _("yellow")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("001DFF00", _("neon green")),
				("00FFFF00", _("neon yellow")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
config.plugins.XionHDF.Font1 = ConfigSelection(default="00ffffff", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00FFEA04", _("yellow")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("001DFF00", _("neon green")),
				("00FFFF00", _("neon yellow")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
config.plugins.XionHDF.Font2 = ConfigSelection(default="00ffffff", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00FFEA04", _("yellow")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("001DFF00", _("neon green")),
				("00FFFF00", _("neon yellow")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
config.plugins.XionHDF.SelectionFont = ConfigSelection(default="00ffffff", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00FFEA04", _("yellow")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("001DFF00", _("neon green")),
				("00FFFF00", _("neon yellow")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
config.plugins.XionHDF.ButtonText = ConfigSelection(default="00ffffff", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00FFEA04", _("yellow")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("001DFF00", _("neon green")),
				("00FFFF00", _("neon yellow")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
config.plugins.XionHDF.Progress = ConfigSelection(default="00C3461B", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00FFEA04", _("yellow")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("001DFF00", _("neon green")),
				("00FFFF00", _("neon yellow")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
config.plugins.XionHDF.Line = ConfigSelection(default="00ffffff", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00FFEA04", _("yellow")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("001DFF00", _("neon green")),
				("00FFFF00", _("neon yellow")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
config.plugins.XionHDF.EMCStyle = ConfigSelection(default="emc-nocover", choices = [
				("emc-nocover", _("no Cover")),
				("emc-smallcover", _("small Cover")),
				("emc-bigcover", _("big Cover")),
				("emc-verybigcover", _("very big Cover")),
				("emc-minitv", _("MiniTV"))
				])
				
config.plugins.XionHDF.MovieStyle = ConfigSelection(default="movieselectionnocover", choices = [
				("movieselectionnocover", _("no Cover")),
				("movieselectionsmallcover", _("small Cover")),
				("movieselectionbigcover", _("big Cover")),
				("movieselectionminitv", _("MiniTV"))
				])
				
config.plugins.XionHDF.InfobarStyle = ConfigSelection(default="infobar-style-xpicon", choices = [
				("infobar-style-xpicon", _("X-Picon"))
				])
				
config.plugins.XionHDF.SIB = ConfigSelection(default="infobar-style-xpicon_end1", choices = [
				("infobar-style-xpicon_end1", _("full")),
				("infobar-style-xpicon_end2", _("top/bottom")),
				("infobar-style-xpicon_end3", _("left/right"))
				])
				
config.plugins.XionHDF.ChannelSelectionStyle = ConfigSelection(default="channelselection-twocolumns", choices = [
				("channelselection-twocolumns", _("two Columns")),
				("channelselection-threecolumns", _("three Columns")),
				("channelselection-xpicon", _("X-Picon")),
				("channelselection-minitv", _("MiniTV"))
				])
				
config.plugins.XionHDF.RunningText = ConfigSelection(default="movetype=running", choices = [
				("movetype=running", _("on")),
				("movetype=none", _("off"))
				])
				
config.plugins.XionHDF.WeatherStyle = ConfigSelection(default="weather-off", choices = [
				("weather-off", _("off")),
				("weather-info", _("infos in place of weather")),
				("weather-big", _("big")),
				("weather-slim", _("slim")),
				("weather-small", _("small"))
				])
				

#config.plugins.XionHDF.SIBFontSize = ConfigSelectionNumber(min = 1, max = 40, stepwidth = 1, default = 18, wraparound = True)
				
#######################################################################

class XionHDF(ConfigListScreen, Screen):
	skin = """
<screen name="XionHDF-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#00000000">
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" text="Cancel" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" text="Save" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" text="Reboot" transparent="1" />
  <widget name="config" position="70,90" size="708,532" itemHeight="28" font="Regular;24" transparent="1" enableWrapAround="1" scrollbarMode="showOnDemand" zPosition="1" backgroundColor="#00000000" />
  <eLabel position="70,12" size="708,46" text="XionHDF - Konfigurationstool" font="Regular; 34" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
  <eLabel position="847,200" size="368,2" backgroundColor="#00ffffff" />
  <eLabel position="847,409" size="368,2" backgroundColor="#00ffffff" />
  <eLabel position="845,200" size="2,211" backgroundColor="#00ffffff" />
  <eLabel position="1215,200" size="2,211" backgroundColor="#00ffffff" />
  <eLabel backgroundColor="#00000000" position="0,0" size="1280,720" transparent="0" zPosition="-9" />
  <ePixmap pixmap="XionHDF/buttons/key_red1.png" position="22,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="XionHDF/buttons/key_green1.png" position="222,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="XionHDF/buttons/key_yellow1.png" position="422,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="XionHDF/buttons/key_blue1.png" position="622,670" size="32,32" backgroundColor="#00000000" alphatest="blend" />
  <widget source="global.CurrentTime" render="Label" position="1154,16" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
    <convert type="ClockToText">Default</convert>
  </widget>
  <eLabel position="830,80" size="402,46" text="XionHDF" font="Regular; 36" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
  <eLabel position="845,130" size="372,46" text="Version: 0.7" font="Regular; 30" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
  <ePixmap backgroundColor="#00000000" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/openhdf.png" position="847,202" size="368,207" zPosition="-9" />
  <widget name="helperimage" position="847,202" size="368,207" zPosition="1" backgroundColor="#00000000" />
  <widget source="help" render="Label" position="847,450" size="368,168" font="Regular2;20" backgroundColor="#00000000" foregroundColor="#00ffffff" halign="center" valign="top" transparent="1" />
  <eLabel backgroundColor="#00ffffff" position="0,64" size="1280,2" zPosition="2" />
  <eLabel backgroundColor="#00ffffff" position="0,656" size="1280,2" zPosition="2" />
</screen>
"""

	def __init__(self, session, args = None, picPath = None):
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
		
		list = []
		ConfigListScreen.__init__(self, list)
		
		self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions"], {"left": self.keyLeft,"down": self.keyDown,"up": self.keyUp,"right": self.keyRight,"red": self.exit,"yellow": self.reboot, "blue": self.showInfo, "green": self.save,"cancel": self.exit}, -1)
		self.UpdatePicture()
		self.onLayoutFinish.append(self.mylist)

	def mylist(self):
		list = []
		list.append(getConfigListEntry(_("_____________________________ System __________________________________"), config.plugins.XionHDF.System, _(" ")))
		list.append(getConfigListEntry(_("Running Text"), config.plugins.XionHDF.RunningText, _("This option activates the running text for some parts of skin.")))
		list.append(getConfigListEntry(_("Background Transparency"), config.plugins.XionHDF.BackgroundColorTrans, _("This option activate/deactive/change the background transparency of skin.")))
		list.append(getConfigListEntry(_("_____________________________ Weather _________________________________"), ))
		list.append(getConfigListEntry(_("Weather"), config.plugins.XionHDF.WeatherStyle, _("This option activate/deactive/change the weather on top inside the infobar.")))
		list.append(getConfigListEntry(_("Weather ID"), config.plugins.XionHDF.weather_city, _("Here you can insert your personal WeatherID. Please visit the website metrixweather.open-store.net to find your location.")))
#		list.append(getConfigListEntry(_("Refresh interval (in minutes)"), config.plugins.XionHDF.refreshInterval, _("Here you can change how often the weather is refreshed in the background.")))
		list.append(getConfigListEntry(_("_____________________________ Colors __________________________________"), ))
		list.append(getConfigListEntry(_("Line"), config.plugins.XionHDF.Line, _("Please select the color of lines inside the skin.")))
		list.append(getConfigListEntry(_("Listselection"), config.plugins.XionHDF.SelectionBackground, _("Please select the color of listselection inside the skin.")))
		list.append(getConfigListEntry(_("Progress-/Volumebar"), config.plugins.XionHDF.Progress, _("Please select the color of progress- and volumebar inside the skin.")))
		list.append(getConfigListEntry(_("primary Font"), config.plugins.XionHDF.Font1, _("Please select the color of primary font inside the skin.")))
		list.append(getConfigListEntry(_("secondary Font"), config.plugins.XionHDF.Font2, _("Please select the color of secundary font inside the skin.")))
		list.append(getConfigListEntry(_("Listselection Font"), config.plugins.XionHDF.SelectionFont, _("Please select the color of listselection font inside the skin.")))
		list.append(getConfigListEntry(_("Button Text"), config.plugins.XionHDF.ButtonText, _("Please select the color of button text inside the skin.")))
		list.append(getConfigListEntry(_("_____________________________ Styles __________________________________"), ))
		list.append(getConfigListEntry(_("Second Infobar"), config.plugins.XionHDF.SIB, _("This option changes the view of second infobar.")))
#		list.append(getConfigListEntry(_("Fontsize Second Infobar"), config.plugins.XionHDF.SIBFontSize, _("This option changes the size of font within the secondinfobar.")))
		list.append(getConfigListEntry(_("ChannelSelection"), config.plugins.XionHDF.ChannelSelectionStyle, _("This option changes the view of channellist.")))
		list.append(getConfigListEntry(_("EnhancedMovieCenter"), config.plugins.XionHDF.EMCStyle, _("This option changes the view of cover inside from EnhancedMovieCenter.")))
		list.append(getConfigListEntry(_("MovieSelection"), config.plugins.XionHDF.MovieStyle, _("This option changes the view of cover inside from MovieSelection.")))
		
		self["config"].list = list
		self["config"].l.setList(list)
		
		self.ShowPicture()
		self.updateHelp()

	def updateHelp(self):
		cur = self["config"].getCurrent()
		if cur:
			self["help"].text = cur[2]

	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			if returnValue == "openhdf":
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
				return "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/black.jpg"
		except:
			return "/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/fb.jpg"

	def UpdatePicture(self):
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)
	
	def ShowPicture(self):
		self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#002C2C39"])
		self.PicLoad.startDecode(self.GetPicturePath())

	def DecodePicture(self, PicInfo = ""):
		ptr = self.PicLoad.getData()
		self["helperimage"].instance.setPixmap(ptr)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.mylist()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.mylist()

	def keyDown(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.mylist()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.mylist()

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
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
		for x in self["config"].list:
			if len(x) > 1:
					x[1].save()
			else:
					pass

		try:
			#global tag search and replace in all skin elements
			self.skinSearchAndReplace = []
			self.skinSearchAndReplace.append(['name="XionBackground" value="#00', 'name="XionBackground" value="#' + config.plugins.XionHDF.BackgroundColorTrans.value])
			self.skinSearchAndReplace.append(['name="XionSelection" value="#000050EF', 'name="XionSelection" value="#' + config.plugins.XionHDF.SelectionBackground.value])
			self.skinSearchAndReplace.append(['name="XionFont1" value="#00ffffff', 'name="XionFont1" value="#' + config.plugins.XionHDF.Font1.value])
			self.skinSearchAndReplace.append(['name="XionFont2" value="#00ffffff', 'name="XionFont2" value="#' + config.plugins.XionHDF.Font2.value])
			self.skinSearchAndReplace.append(['name="XionSelFont" value="#00ffffff', 'name="XionSelFont" value="#' + config.plugins.XionHDF.SelectionFont.value])
			self.skinSearchAndReplace.append(['name="XionButtonText" value="#00ffffff', 'name="XionButtonText" value="#' + config.plugins.XionHDF.ButtonText.value])
			self.skinSearchAndReplace.append(['name="XionProgress" value="#00ffffff', 'name="XionProgress" value="#' + config.plugins.XionHDF.Progress.value])
			self.skinSearchAndReplace.append(['name="XionLine" value="#00ffffff', 'name="XionLine" value="#' + config.plugins.XionHDF.Line.value])
			self.skinSearchAndReplace.append(["movetype=running", config.plugins.XionHDF.RunningText.value])
			
			
			### Header
			self.appendSkinFile(self.daten + "header.xml")

			###ChannelSelection
			self.appendSkinFile(self.daten + config.plugins.XionHDF.ChannelSelectionStyle.value + ".xml")

			###Infobar_main
			self.appendSkinFile(self.daten + config.plugins.XionHDF.InfobarStyle.value + "_main.xml")

#			###SecondInfobar_main EPG fontsize
#			self.appendSkinFile(self.daten + config.plugins.XionHDF.SIBFontSize.value + "_main.xml")

			###weather-style
			self.appendSkinFile(self.daten + config.plugins.XionHDF.WeatherStyle.value + ".xml")

			###Infobar_middle
			self.appendSkinFile(self.daten + config.plugins.XionHDF.InfobarStyle.value + "_middle.xml")

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

			move(self.dateiTMP, self.datei)

			#system('rm -rf ' + self.dateiTMP)
		except:
			self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)

		self.restart()

	def restart(self):
		configfile.save()
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skin.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
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

#############################################################

def main(session, **kwargs):
	session.open(XionHDF,"/usr/lib/enigma2/python/Plugins/Extensions/XionHDF/images/Xioncolors.jpg")

def Plugins(**kwargs):
	screenwidth = getDesktop(0).size().width()
	if screenwidth and screenwidth == 1920:
		return [PluginDescriptor(name="XionHDF", description=_("Configuration tool for XionHDF"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='pluginfhd.png', fnc=main)]
	else:
		return [PluginDescriptor(name="XionHDF", description=_("Configuration tool for XionHDF"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main)]