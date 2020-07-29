from __future__ import absolute_import
import os
import re
from Components.config import config, ConfigSelection, ConfigSubsection, ConfigSelectionNumber, ConfigText, ConfigNumber
from Tools.Directories import fileExists
from boxbranding import getBoxType

################# ColorList #########################################

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

################# SelectionBorderList ################################

SelectionBorderList = [("none", _("Off"))]
SelectionBorderList = ColorList + SelectionBorderList

################# bmeminfo ###########################################

if fileExists('/proc/bmeminfo'):
   entrie = os.popen('cat /proc/bmeminfo').read()
   mem = entrie.split(':', 1)[1].split('k')[0]
   bmem = int(mem)/1024
else:
   mem_info = []
   entrie = os.popen('cat /proc/cmdline').read()

   if getBoxType() in ('vusolo4k', 'mutant51', 'mutant52', 'ax51', 'zgemmah7', 'zgemmah9t', 'zgemmah9s', 'e4hdultra'):
        mem = re.findall('_cma=(.*?)M', entrie)
   else:
        mem = re.findall('bmem=(.*?)M', entrie)

   for info in mem:
      mem_info.append((info))

   if len(mem_info) > 1:
      bmem = int(mem_info[0]) + int(mem_info[1])
   else:
      if getBoxType() in ('sf8008','sf4008','dinobot4k','anadol4k','zgemmah9t','zgemmah9s','gbquad4k','gbue4k','e4hdultra','axashis4kcombo','axashis4kcomboplus'):
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

################################################################

config.plugins = ConfigSubsection()
config.plugins.XionHDF = ConfigSubsection()

config.plugins.XionHDF.BackgroundColorTrans = ConfigSelection(default="1c", choices = [
                                ("00", _("Off")),
                                ("1c", _("Lower")),
                                ("2d", _("Low")),
                                ("4a", _("Middle")),
                                ("6c", _("Medium")),
                                ("8c", _("High"))
                                ])
config.plugins.XionHDF.ButtonText = ConfigSelection(default="00ffffff", choices = ColorList)
config.plugins.XionHDF.ChannelSelectionStyle = ConfigSelection(default="channelselection-twocolumns", choices = [
                                ("channelselection-twocolumns", _("Two columns")),
                                ("channelselection-threecolumns", _("Three columns")),
                                ("channelselection-xpicon", _("X-Picon")),
                                ("channelselection-minitv", _("MiniTV"))
                                ])
config.plugins.XionHDF.EMCStyle = ConfigSelection(default="emc-nocover", choices = [
                                ("emc-nocover", _("No cover")),
                                ("emc-smallcover", _("Small cover")),
                                ("emc-bigcover", _("Big cover")),
                                ("emc-verybigcover", _("Very big cover")),
                                ("emc-listbigcover", _("List big cover")),
                                ("emc-minitv", _("MiniTV"))
                                ])
config.plugins.XionHDF.Font1 = ConfigSelection(default="00ffffff", choices = ColorList)
config.plugins.XionHDF.Font2 = ConfigSelection(default="00ffffff", choices = ColorList)
config.plugins.XionHDF.FontStyleHeight_1 = ConfigSelectionNumber(default = 95, stepwidth = 1, min = 0, max = 120, wraparound = True)
config.plugins.XionHDF.FontStyleHeight_2 = ConfigSelectionNumber(default = 95, stepwidth = 1, min = 0, max = 120, wraparound = True)
config.plugins.XionHDF.InfobarChannelname = ConfigSelection(default="infobar-style-xpicon_middle1", choices = [
                                ("infobar-style-xpicon_middle1", _("Small")),
                                ("infobar-style-xpicon_middle2", _("Big")),
                                ("infobar-style-xpicon_middleP", _("Poster")),
                                ("infobar-style-xpicon_middle3", _("Off"))
                                ])
config.plugins.XionHDF.InfobarStyle = ConfigSelection(default="infobar-style-xpicon", choices = [
                                ("infobar-style-xpicon", _("X-Picon"))
                                ])
config.plugins.XionHDF.Line = ConfigSelection(default="00ffffff", choices = ColorList)
config.plugins.XionHDF.MovieStyle = ConfigSelection(default="movieselectionnocover", choices = [
                                ("movieselectionnocover", _("No cover")),
                                ("movieselectionsmallcover", _("Small cover")),
                                ("movieselectionbigcover", _("Big cover")),
                                ("movieselectionlistbigcover", _("List big cover")),
                                ("movieselectionminitv", _("MiniTV"))
                                ])
config.plugins.XionHDF.Progress = ConfigSelection(default="00C3461B", choices = ColorList)
config.plugins.XionHDF.ScrollBar = ConfigSelection(default="showNever", choices = [
                                ("showOnDemand", _("On")),
                                ("showNever", _("Off"))
                                ])
config.plugins.XionHDF.SelectionBackground = ConfigSelection(default="00C3461B", choices = ColorList)
config.plugins.XionHDF.SelectionBorder = ConfigSelection(default="none", choices = SelectionBorderList)
config.plugins.XionHDF.SelectionFont = ConfigSelection(default="00ffffff", choices = ColorList)
config.plugins.XionHDF.SIB = ConfigSelection(default="infobar-style-xpicon_end1", choices = [
                                ("infobar-style-xpicon_end1", _("Only current program")),
                                ("infobar-style-xpicon_end2", _("Top/Bottom")),
                                ("infobar-style-xpicon_end3", _("Left/Right"))
                                ])
config.plugins.XionHDF.refreshInterval = ConfigSelectionNumber(min = 10, max = 240, stepwidth = 5, default = 60, wraparound = True)
config.plugins.XionHDF.skin_mode = ConfigSelection(default="hd", choices = SkinModeList)
config.plugins.XionHDF.RunningText = ConfigSelection(default="movetype=running", choices = [
                                ("movetype=running", _("On")),
                                ("movetype=none", _("Off"))
                                ])
config.plugins.XionHDF.System = ConfigSelection(default="openhdf", choices = [
                                ("openhdf", _(" "))
                                ])
config.plugins.XionHDF.weather_city = ConfigText(default = "")
config.plugins.XionHDF.weather_foundcity = ConfigText(default = "")
config.plugins.XionHDF.weather_realtek_latlon = ConfigText(default = "")
config.plugins.XionHDF.WeatherStyle = ConfigSelection(default="weather-off", choices = [
                                ("weather-off", _("Off")),
                                ("weather-info", _("Infos in place of weather")),
                                ("weather-big", _("Big")),
                                ("weather-slim", _("Slim")),
                                ("weather-small", _("Small"))
                                ])

