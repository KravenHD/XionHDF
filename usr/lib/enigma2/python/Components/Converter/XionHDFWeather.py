# -*- coding: utf-8 -*-
#
#  YAHOO Weather Info
#
#  Coded by tomele for Kraven Skins
#  Thankfully inspired by iMaxxx (c) 2013
#
#  This plugin is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative
#  Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially 
#  distributed other than under the conditions noted above.
#

from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Components.Language import language
from twisted.web.client import getPage
from xml.dom.minidom import parseString
from enigma import eTimer
from Components.config import config
from time import strftime
from Poll import Poll
from copy import deepcopy
import gettext, os, time


lang = language.getLanguage()
os.environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("XionHDF", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/XionHDF/locale/"))

def _(txt):
	t = gettext.dgettext("XionHDF", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

weather_data = None
weather_data_old = None
look_again = False
load_data = False
look_count = 0

class XionHDFWeather(Poll, Converter, object):

	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.type = type
		self.poll_interval = 10000
		self.poll_enabled = True
		global weather_data
		global weather_data_old
		global load_data
		if weather_data is None:
			load_data = True
			weather_data = WeatherData()
		if weather_data_old is None:
			load_data = False
			weather_data_old = WeatherData()

	@cached
	def getText(self):
		WeatherInfo = weather_data_old.WeatherInfo

		# due to yahoo changing the forecast scheme hours after the actual day has changed
		# read actual day name and tomorrow forecast day name

		self.aday = _(strftime("%a", time.localtime())).upper()
		self.fday = WeatherInfo["forecastTomorrowDay"].upper()
		
		# if actual day equals tomorrow forecast day, shift forecasts left one day

		if self.fday == self.aday:
			
			WeatherInfo["forecastTodayCode"] = WeatherInfo["forecastTomorrowCode"] 
			WeatherInfo["forecastTodayDay"] = WeatherInfo["forecastTomorrowDay"] 
			WeatherInfo["forecastTodayDate"] = WeatherInfo["forecastTomorrowDate"] 
			WeatherInfo["forecastTodayTempMax"] = WeatherInfo["forecastTomorrowTempMax"] 
			WeatherInfo["forecastTodayTempMin"] = WeatherInfo["forecastTomorrowTempMin"] 
			WeatherInfo["forecastTodayTempMinMax"] = WeatherInfo["forecastTomorrowTempMinMax"]
			WeatherInfo["forecastTodayText"] = WeatherInfo["forecastTomorrowText"] 
			WeatherInfo["forecastTodayPicon"] = WeatherInfo["forecastTomorrowPicon"] 

			WeatherInfo["forecastTomorrowCode"] = WeatherInfo["forecastTomorrow1Code"] 
			WeatherInfo["forecastTomorrowDay"] = WeatherInfo["forecastTomorrow1Day"] 
			WeatherInfo["forecastTomorrowDate"] = WeatherInfo["forecastTomorrow1Date"] 
			WeatherInfo["forecastTomorrowTempMax"] = WeatherInfo["forecastTomorrow1TempMax"] 
			WeatherInfo["forecastTomorrowTempMin"] = WeatherInfo["forecastTomorrow1TempMin"] 
			WeatherInfo["forecastTomorrowTempMinMax"] = WeatherInfo["forecastTomorrow1TempMinMax"]
			WeatherInfo["forecastTomorrowText"] = WeatherInfo["forecastTomorrow1Text"] 
			WeatherInfo["forecastTomorrowPicon"] = WeatherInfo["forecastTomorrow1Picon"] 
		
			WeatherInfo["forecastTomorrow1Code"] = WeatherInfo["forecastTomorrow2Code"] 
			WeatherInfo["forecastTomorrow1Day"] = WeatherInfo["forecastTomorrow2Day"] 
			WeatherInfo["forecastTomorrow1Date"] = WeatherInfo["forecastTomorrow2Date"] 
			WeatherInfo["forecastTomorrow1TempMax"] = WeatherInfo["forecastTomorrow2TempMax"] 
			WeatherInfo["forecastTomorrow1TempMin"] = WeatherInfo["forecastTomorrow2TempMin"] 
			WeatherInfo["forecastTomorrow1TempMinMax"] = WeatherInfo["forecastTomorrow2TempMinMax"]
			WeatherInfo["forecastTomorrow1Text"] = WeatherInfo["forecastTomorrow2Text"] 
			WeatherInfo["forecastTomorrow1Picon"] = WeatherInfo["forecastTomorrow2Picon"] 
		
			WeatherInfo["forecastTomorrow2Code"] = WeatherInfo["forecastTomorrow3Code"] 
			WeatherInfo["forecastTomorrow2Day"] = WeatherInfo["forecastTomorrow3Day"] 
			WeatherInfo["forecastTomorrow2Date"] = WeatherInfo["forecastTomorrow3Date"] 
			WeatherInfo["forecastTomorrow2TempMax"] = WeatherInfo["forecastTomorrow3TempMax"] 
			WeatherInfo["forecastTomorrow2TempMin"] = WeatherInfo["forecastTomorrow3TempMin"] 
			WeatherInfo["forecastTomorrow2TempMinMax"] = WeatherInfo["forecastTomorrow3TempMinMax"]
			WeatherInfo["forecastTomorrow2Text"] = WeatherInfo["forecastTomorrow3Text"] 
			WeatherInfo["forecastTomorrow2Picon"] = WeatherInfo["forecastTomorrow3Picon"] 
		
			WeatherInfo["forecastTomorrow3Code"] = "("
			WeatherInfo["forecastTomorrow3Date"] = ""
			WeatherInfo["forecastTomorrow3TempMax"] = ""
			WeatherInfo["forecastTomorrow3TempMin"] = ""
			WeatherInfo["forecastTomorrow3TempMinMax"] = ""
			WeatherInfo["forecastTomorrow3Text"] = ""
			WeatherInfo["forecastTomorrow3Picon"] = "3200"

			if WeatherInfo["forecastTomorrow3Day"] == "MO":
				WeatherInfo["forecastTomorrow3Day"] = "DI"
			elif WeatherInfo["forecastTomorrow3Day"] == "DI":
 				WeatherInfo["forecastTomorrow3Day"] = "MI"
			elif WeatherInfo["forecastTomorrow3Day"] == "MI":
 				WeatherInfo["forecastTomorrow3Day"] = "DO"
			elif WeatherInfo["forecastTomorrow3Day"] == "DO":
 				WeatherInfo["forecastTomorrow3Day"] = "FR"
			elif WeatherInfo["forecastTomorrow3Day"] == "FR":
 				WeatherInfo["forecastTomorrow3Day"] = "SA"
			elif WeatherInfo["forecastTomorrow3Day"] == "SA":
 				WeatherInfo["forecastTomorrow3Day"] = "SO"
			elif WeatherInfo["forecastTomorrow3Day"] == "SO":
 				WeatherInfo["forecastTomorrow3Day"] = "MO"

		# end of yahoo forecast fix
				
		if self.type == "currentLocation":
			return WeatherInfo[self.type]
		elif self.type == "currentDirection":
			return WeatherInfo[self.type]
		elif self.type == "currentWind":
			return WeatherInfo[self.type]
		elif self.type == "feels2":
			return WeatherInfo[self.type] + "°C"
		elif self.type == "feels":
			return WeatherInfo[self.type]
		elif self.type == "klima":
			return WeatherInfo[self.type]
		elif self.type == "currentWeatherTemp":
			return WeatherInfo[self.type] + "°C"
		elif self.type == "currentWeatherText":
			if WeatherInfo["currentWeatherPicon"] == '0':
				return _('Tornado')
			elif WeatherInfo["currentWeatherPicon"] == '1':
				return _('Tropical\n storm')
			elif WeatherInfo["currentWeatherPicon"] == '2':
				return _('Hurricane')
			elif WeatherInfo["currentWeatherPicon"] == '3':
				return _('Severe\n thunderstorms')
			elif WeatherInfo["currentWeatherPicon"] == '4':
				return _('Thunderstorms')
			elif WeatherInfo["currentWeatherPicon"] == '5':
				return _('Mixed rain\n and snow')
			elif WeatherInfo["currentWeatherPicon"] == '6':
				return _('Mixed rain\n and sleet')
			elif WeatherInfo["currentWeatherPicon"] == '7':
				return _('Mixed snow\n and sleet')
			elif WeatherInfo["currentWeatherPicon"] == '8':
				return _('Freezing\n drizzle')
			elif WeatherInfo["currentWeatherPicon"] == '9':
				return _('Drizzle')
			elif WeatherInfo["currentWeatherPicon"] == '10':
				return _('Freezing\n rain')
			elif WeatherInfo["currentWeatherPicon"] == '11':
				return _('Showers')
			elif WeatherInfo["currentWeatherPicon"] == '12':
				return _('Rain')
			elif WeatherInfo["currentWeatherPicon"] == '13':
				return _('Snow\n flurries')
			elif WeatherInfo["currentWeatherPicon"] == '14':
				return _('Light\n snow showers')
			elif WeatherInfo["currentWeatherPicon"] == '15':
				return _('Blowing\n snow')
			elif WeatherInfo["currentWeatherPicon"] == '16':
				return _('Snow')
			elif WeatherInfo["currentWeatherPicon"] == '17':
				return _('Hail')
			elif WeatherInfo["currentWeatherPicon"] == '18':
				return _('Sleet')
			elif WeatherInfo["currentWeatherPicon"] == '19':
				return _('Dust')
			elif WeatherInfo["currentWeatherPicon"] == '20':
				return _('Foggy')
			elif WeatherInfo["currentWeatherPicon"] == '21':
				return _('Haze')
			elif WeatherInfo["currentWeatherPicon"] == '22':
				return _('Smoky')
			elif WeatherInfo["currentWeatherPicon"] == '23':
				return _('Blustery')
			elif WeatherInfo["currentWeatherPicon"] == '24':
				return _('Windy')
			elif WeatherInfo["currentWeatherPicon"] == '25':
				return _('Cold')
			elif WeatherInfo["currentWeatherPicon"] == '26':
				return _('Cloudy')
			elif WeatherInfo["currentWeatherPicon"] == '27':
				return _('Mostly\n cloudy')
			elif WeatherInfo["currentWeatherPicon"] == '28':
				return _('Mostly\n cloudy')
			elif WeatherInfo["currentWeatherPicon"] == '29':
				return _('Partly\n cloudy')
			elif WeatherInfo["currentWeatherPicon"] == '30':
				return _('Partly\n cloudy')
			elif WeatherInfo["currentWeatherPicon"] == '31':
				return _('Clear')
			elif WeatherInfo["currentWeatherPicon"] == '32':
				return _('Sunny')
			elif WeatherInfo["currentWeatherPicon"] == '33':
				return _('Fair')
			elif WeatherInfo["currentWeatherPicon"] == '34':
				return _('Fair')
			elif WeatherInfo["currentWeatherPicon"] == '35':
				return _('Mixed rain\n and hail')
			elif WeatherInfo["currentWeatherPicon"] == '36':
				return _('Hot')
			elif WeatherInfo["currentWeatherPicon"] == '37':
				return _('Isolated\n thunderstorms')
			elif WeatherInfo["currentWeatherPicon"] == '38':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["currentWeatherPicon"] == '39':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["currentWeatherPicon"] == '40':
				return _('Scattered\n showers')
			elif WeatherInfo["currentWeatherPicon"] == '41':
				return _('Heavy snow')
			elif WeatherInfo["currentWeatherPicon"] == '42':
				return _('Scattered\n snow showers')
			elif WeatherInfo["currentWeatherPicon"] == '43':
				return _('Heavy snow')
			elif WeatherInfo["currentWeatherPicon"] == '44':
				return _('Partly\n cloudy')
			elif WeatherInfo["currentWeatherPicon"] == '45':
				return _('Thundershowers')
			elif WeatherInfo["currentWeatherPicon"] == '46':
				return _('Snow showers')
			elif WeatherInfo["currentWeatherPicon"] == '47':
				return _('Isolated\n thundershowers')
			elif WeatherInfo["currentWeatherPicon"] == '3200':
				return _('Not\n available')
			else:
				return "N/A"
		elif self.type == "currentWeatherPicon":
			return WeatherInfo[self.type]
		elif self.type == "currentWeatherCode":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayCode":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayDay":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayDate":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayTempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayTempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayTempMinMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTodayText":
			if WeatherInfo["forecastTodayPicon"] == '0':
				return _('Tornado')
			elif WeatherInfo["forecastTodayPicon"] == '1':
				return _('Tropical\n storm')
			elif WeatherInfo["forecastTodayPicon"] == '2':
				return _('Hurricane')
			elif WeatherInfo["forecastTodayPicon"] == '3':
				return _('Severe\n thunderstorms')
			elif WeatherInfo["forecastTodayPicon"] == '4':
				return _('Thunderstorms')
			elif WeatherInfo["forecastTodayPicon"] == '5':
				return _('Mixed rain\n and snow')
			elif WeatherInfo["forecastTodayPicon"] == '6':
				return _('Mixed rain\n and sleet')
			elif WeatherInfo["forecastTodayPicon"] == '7':
				return _('Mixed snow\n and sleet')
			elif WeatherInfo["forecastTodayPicon"] == '8':
				return _('Freezing\n drizzle')
			elif WeatherInfo["forecastTodayPicon"] == '9':
				return _('Drizzle')
			elif WeatherInfo["forecastTodayPicon"] == '10':
				return _('Freezing\n rain')
			elif WeatherInfo["forecastTodayPicon"] == '11':
				return _('Showers')
			elif WeatherInfo["forecastTodayPicon"] == '12':
				return _('Rain')
			elif WeatherInfo["forecastTodayPicon"] == '13':
				return _('Snow\n flurries')
			elif WeatherInfo["forecastTodayPicon"] == '14':
				return _('Light\n snow showers')
			elif WeatherInfo["forecastTodayPicon"] == '15':
				return _('Blowing\n snow')
			elif WeatherInfo["forecastTodayPicon"] == '16':
				return _('Snow')
			elif WeatherInfo["forecastTodayPicon"] == '17':
				return _('Hail')
			elif WeatherInfo["forecastTodayPicon"] == '18':
				return _('Sleet')
			elif WeatherInfo["forecastTodayPicon"] == '19':
				return _('Dust')
			elif WeatherInfo["forecastTodayPicon"] == '20':
				return _('Foggy')
			elif WeatherInfo["forecastTodayPicon"] == '21':
				return _('Haze')
			elif WeatherInfo["forecastTodayPicon"] == '22':
				return _('Smoky')
			elif WeatherInfo["forecastTodayPicon"] == '23':
				return _('Blustery')
			elif WeatherInfo["forecastTodayPicon"] == '24':
				return _('Windy')
			elif WeatherInfo["forecastTodayPicon"] == '25':
				return _('Cold')
			elif WeatherInfo["forecastTodayPicon"] == '26':
				return _('Cloudy')
			elif WeatherInfo["forecastTodayPicon"] == '27':
				return _('Mostly\n cloudy')
			elif WeatherInfo["forecastTodayPicon"] == '28':
				return _('Mostly\n cloudy')
			elif WeatherInfo["forecastTodayPicon"] == '29':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTodayPicon"] == '30':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTodayPicon"] == '31':
				return _('Clear')
			elif WeatherInfo["forecastTodayPicon"] == '32':
				return _('Sunny')
			elif WeatherInfo["forecastTodayPicon"] == '33':
				return _('Fair')
			elif WeatherInfo["forecastTodayPicon"] == '34':
				return _('Fair')
			elif WeatherInfo["forecastTodayPicon"] == '35':
				return _('Mixed rain\n and hail')
			elif WeatherInfo["forecastTodayPicon"] == '36':
				return _('Hot')
			elif WeatherInfo["forecastTodayPicon"] == '37':
				return _('Isolated\n thunderstorms')
			elif WeatherInfo["forecastTodayPicon"] == '38':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["forecastTodayPicon"] == '39':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["forecastTodayPicon"] == '40':
				return _('Scattered\n showers')
			elif WeatherInfo["forecastTodayPicon"] == '41':
				return _('Heavy snow')
			elif WeatherInfo["forecastTodayPicon"] == '42':
				return _('Scattered\n snow showers')
			elif WeatherInfo["forecastTodayPicon"] == '43':
				return _('Heavy snow')
			elif WeatherInfo["forecastTodayPicon"] == '44':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTodayPicon"] == '45':
				return _('Thundershowers')
			elif WeatherInfo["forecastTodayPicon"] == '46':
				return _('Snow showers')
			elif WeatherInfo["forecastTodayPicon"] == '47':
				return _('Isolated\n thundershowers')
			elif WeatherInfo["forecastTodayPicon"] == '3200':
				return _('Not\n available')
			else:
				return "N/A"
		elif self.type == "forecastTodayPicon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowCode":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowDay":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowDate":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowTempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowTempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowTempMinMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrowText":
			if WeatherInfo["forecastTomorrowPicon"] == '0':
				return _('Tornado')
			elif WeatherInfo["forecastTomorrowPicon"] == '1':
				return _('Tropical\n storm')
			elif WeatherInfo["forecastTomorrowPicon"] == '2':
				return _('Hurricane')
			elif WeatherInfo["forecastTomorrowPicon"] == '3':
				return _('Severe\n thunderstorms')
			elif WeatherInfo["forecastTomorrowPicon"] == '4':
				return _('Thunderstorms')
			elif WeatherInfo["forecastTomorrowPicon"] == '5':
				return _('Mixed rain\n and snow')
			elif WeatherInfo["forecastTomorrowPicon"] == '6':
				return _('Mixed rain\n and sleet')
			elif WeatherInfo["forecastTomorrowPicon"] == '7':
				return _('Mixed snow\n and sleet')
			elif WeatherInfo["forecastTomorrowPicon"] == '8':
				return _('Freezing\n drizzle')
			elif WeatherInfo["forecastTomorrowPicon"] == '9':
				return _('Drizzle')
			elif WeatherInfo["forecastTomorrowPicon"] == '10':
				return _('Freezing\n rain')
			elif WeatherInfo["forecastTomorrowPicon"] == '11':
				return _('Showers')
			elif WeatherInfo["forecastTomorrowPicon"] == '12':
				return _('Rain')
			elif WeatherInfo["forecastTomorrowPicon"] == '13':
				return _('Snow\n flurries')
			elif WeatherInfo["forecastTomorrowPicon"] == '14':
				return _('Light\n snow showers')
			elif WeatherInfo["forecastTomorrowPicon"] == '15':
				return _('Blowing\n snow')
			elif WeatherInfo["forecastTomorrowPicon"] == '16':
				return _('Snow')
			elif WeatherInfo["forecastTomorrowPicon"] == '17':
				return _('Hail')
			elif WeatherInfo["forecastTomorrowPicon"] == '18':
				return _('Sleet')
			elif WeatherInfo["forecastTomorrowPicon"] == '19':
				return _('Dust')
			elif WeatherInfo["forecastTomorrowPicon"] == '20':
				return _('Foggy')
			elif WeatherInfo["forecastTomorrowPicon"] == '21':
				return _('Haze')
			elif WeatherInfo["forecastTomorrowPicon"] == '22':
				return _('Smoky')
			elif WeatherInfo["forecastTomorrowPicon"] == '23':
				return _('Blustery')
			elif WeatherInfo["forecastTomorrowPicon"] == '24':
				return _('Windy')
			elif WeatherInfo["forecastTomorrowPicon"] == '25':
				return _('Cold')
			elif WeatherInfo["forecastTomorrowPicon"] == '26':
				return _('Cloudy')
			elif WeatherInfo["forecastTomorrowPicon"] == '27':
				return _('Mostly\n cloudy')
			elif WeatherInfo["forecastTomorrowPicon"] == '28':
				return _('Mostly\n cloudy')
			elif WeatherInfo["forecastTomorrowPicon"] == '29':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrowPicon"] == '30':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrowPicon"] == '31':
				return _('Clear')
			elif WeatherInfo["forecastTomorrowPicon"] == '32':
				return _('Sunny')
			elif WeatherInfo["forecastTomorrowPicon"] == '33':
				return _('Fair')
			elif WeatherInfo["forecastTomorrowPicon"] == '34':
				return _('Fair')
			elif WeatherInfo["forecastTomorrowPicon"] == '35':
				return _('Mixed rain\n and hail')
			elif WeatherInfo["forecastTomorrowPicon"] == '36':
				return _('Hot')
			elif WeatherInfo["forecastTomorrowPicon"] == '37':
				return _('Isolated\n thunderstorms')
			elif WeatherInfo["forecastTomorrowPicon"] == '38':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["forecastTomorrowPicon"] == '39':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["forecastTomorrowPicon"] == '40':
				return _('Scattered\n showers')
			elif WeatherInfo["forecastTomorrowPicon"] == '41':
				return _('Heavy snow')
			elif WeatherInfo["forecastTomorrowPicon"] == '42':
				return _('Scattered\n snow showers')
			elif WeatherInfo["forecastTomorrowPicon"] == '43':
				return _('Heavy snow')
			elif WeatherInfo["forecastTomorrowPicon"] == '44':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrowPicon"] == '45':
				return _('Thundershowers')
			elif WeatherInfo["forecastTomorrowPicon"] == '46':
				return _('Snow showers')
			elif WeatherInfo["forecastTomorrowPicon"] == '47':
				return _('Isolated\n thundershowers')
			elif WeatherInfo["forecastTomorrowPicon"] == '3200':
				return _('Not\n available')
			else:
				return "N/A"
		elif self.type == "forecastTomorrowPicon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1TempMinMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow1Text":
			if WeatherInfo["forecastTomorrow1Picon"] == '0':
				return _('Tornado')
			elif WeatherInfo["forecastTomorrow1Picon"] == '1':
				return _('Tropical\n storm')
			elif WeatherInfo["forecastTomorrow1Picon"] == '2':
				return _('Hurricane')
			elif WeatherInfo["forecastTomorrow1Picon"] == '3':
				return _('Severe\n thunderstorms')
			elif WeatherInfo["forecastTomorrow1Picon"] == '4':
				return _('Thunderstorms')
			elif WeatherInfo["forecastTomorrow1Picon"] == '5':
				return _('Mixed rain\n and snow')
			elif WeatherInfo["forecastTomorrow1Picon"] == '6':
				return _('Mixed rain\n and sleet')
			elif WeatherInfo["forecastTomorrow1Picon"] == '7':
				return _('Mixed snow\n and sleet')
			elif WeatherInfo["forecastTomorrow1Picon"] == '8':
				return _('Freezing\n drizzle')
			elif WeatherInfo["forecastTomorrow1Picon"] == '9':
				return _('Drizzle')
			elif WeatherInfo["forecastTomorrow1Picon"] == '10':
				return _('Freezing\n rain')
			elif WeatherInfo["forecastTomorrow1Picon"] == '11':
				return _('Showers')
			elif WeatherInfo["forecastTomorrow1Picon"] == '12':
				return _('Rain')
			elif WeatherInfo["forecastTomorrow1Picon"] == '13':
				return _('Snow\n flurries')
			elif WeatherInfo["forecastTomorrow1Picon"] == '14':
				return _('Light\n snow showers')
			elif WeatherInfo["forecastTomorrow1Picon"] == '15':
				return _('Blowing\n snow')
			elif WeatherInfo["forecastTomorrow1Picon"] == '16':
				return _('Snow')
			elif WeatherInfo["forecastTomorrow1Picon"] == '17':
				return _('Hail')
			elif WeatherInfo["forecastTomorrow1Picon"] == '18':
				return _('Sleet')
			elif WeatherInfo["forecastTomorrow1Picon"] == '19':
				return _('Dust')
			elif WeatherInfo["forecastTomorrow1Picon"] == '20':
				return _('Foggy')
			elif WeatherInfo["forecastTomorrow1Picon"] == '21':
				return _('Haze')
			elif WeatherInfo["forecastTomorrow1Picon"] == '22':
				return _('Smoky')
			elif WeatherInfo["forecastTomorrow1Picon"] == '23':
				return _('Blustery')
			elif WeatherInfo["forecastTomorrow1Picon"] == '24':
				return _('Windy')
			elif WeatherInfo["forecastTomorrow1Picon"] == '25':
				return _('Cold')
			elif WeatherInfo["forecastTomorrow1Picon"] == '26':
				return _('Cloudy')
			elif WeatherInfo["forecastTomorrow1Picon"] == '27':
				return _('Mostly\n cloudy')
			elif WeatherInfo["forecastTomorrow1Picon"] == '28':
				return _('Mostly\n cloudy')
			elif WeatherInfo["forecastTomorrow1Picon"] == '29':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrow1Picon"] == '30':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrow1Picon"] == '31':
				return _('Clear')
			elif WeatherInfo["forecastTomorrow1Picon"] == '32':
				return _('Sunny')
			elif WeatherInfo["forecastTomorrow1Picon"] == '33':
				return _('Fair')
			elif WeatherInfo["forecastTomorrow1Picon"] == '34':
				return _('Fair')
			elif WeatherInfo["forecastTomorrow1Picon"] == '35':
				return _('Mixed rain\n and hail')
			elif WeatherInfo["forecastTomorrow1Picon"] == '36':
				return _('Hot')
			elif WeatherInfo["forecastTomorrow1Picon"] == '37':
				return _('Isolated\n thunderstorms')
			elif WeatherInfo["forecastTomorrow1Picon"] == '38':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["forecastTomorrow1Picon"] == '39':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["forecastTomorrow1Picon"] == '40':
				return _('Scattered\n showers')
			elif WeatherInfo["forecastTomorrow1Picon"] == '41':
				return _('Heavy snow')
			elif WeatherInfo["forecastTomorrow1Picon"] == '42':
				return _('Scattered\n snow showers')
			elif WeatherInfo["forecastTomorrow1Picon"] == '43':
				return _('Heavy snow')
			elif WeatherInfo["forecastTomorrow1Picon"] == '44':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrow1Picon"] == '45':
				return _('Thundershowers')
			elif WeatherInfo["forecastTomorrow1Picon"] == '46':
				return _('Snow showers')
			elif WeatherInfo["forecastTomorrow1Picon"] == '47':
				return _('Isolated\n thundershowers')
			elif WeatherInfo["forecastTomorrow1Picon"] == '3200':
				return _('Not\n available')
			else:
				return "N/A"
		elif self.type == "forecastTomorrow1Picon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2TempMinMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow2Text":
			if WeatherInfo["forecastTomorrow2Picon"] == '0':
				return _('Tornado')
			elif WeatherInfo["forecastTomorrow2Picon"] == '1':
				return _('Tropical\n storm')
			elif WeatherInfo["forecastTomorrow2Picon"] == '2':
				return _('Hurricane')
			elif WeatherInfo["forecastTomorrow2Picon"] == '3':
				return _('Severe\n thunderstorms')
			elif WeatherInfo["forecastTomorrow2Picon"] == '4':
				return _('Thunderstorms')
			elif WeatherInfo["forecastTomorrow2Picon"] == '5':
				return _('Mixed rain\n and snow')
			elif WeatherInfo["forecastTomorrow2Picon"] == '6':
				return _('Mixed rain\n and sleet')
			elif WeatherInfo["forecastTomorrow2Picon"] == '7':
				return _('Mixed snow\n and sleet')
			elif WeatherInfo["forecastTomorrow2Picon"] == '8':
				return _('Freezing\n drizzle')
			elif WeatherInfo["forecastTomorrow2Picon"] == '9':
				return _('Drizzle')
			elif WeatherInfo["forecastTomorrow2Picon"] == '10':
				return _('Freezing\n rain')
			elif WeatherInfo["forecastTomorrow2Picon"] == '11':
				return _('Showers')
			elif WeatherInfo["forecastTomorrow2Picon"] == '12':
				return _('Rain')
			elif WeatherInfo["forecastTomorrow2Picon"] == '13':
				return _('Snow\n flurries')
			elif WeatherInfo["forecastTomorrow2Picon"] == '14':
				return _('Light\n snow showers')
			elif WeatherInfo["forecastTomorrow2Picon"] == '15':
				return _('Blowing\n snow')
			elif WeatherInfo["forecastTomorrow2Picon"] == '16':
				return _('Snow')
			elif WeatherInfo["forecastTomorrow2Picon"] == '17':
				return _('Hail')
			elif WeatherInfo["forecastTomorrow2Picon"] == '18':
				return _('Sleet')
			elif WeatherInfo["forecastTomorrow2Picon"] == '19':
				return _('Dust')
			elif WeatherInfo["forecastTomorrow2Picon"] == '20':
				return _('Foggy')
			elif WeatherInfo["forecastTomorrow2Picon"] == '21':
				return _('Haze')
			elif WeatherInfo["forecastTomorrow2Picon"] == '22':
				return _('Smoky')
			elif WeatherInfo["forecastTomorrow2Picon"] == '23':
				return _('Blustery')
			elif WeatherInfo["forecastTomorrow2Picon"] == '24':
				return _('Windy')
			elif WeatherInfo["forecastTomorrow2Picon"] == '25':
				return _('Cold')
			elif WeatherInfo["forecastTomorrow2Picon"] == '26':
				return _('Cloudy')
			elif WeatherInfo["forecastTomorrow2Picon"] == '27':
				return _('Mostly\n cloudy')
			elif WeatherInfo["forecastTomorrow2Picon"] == '28':
				return _('Mostly\n cloudy')
			elif WeatherInfo["forecastTomorrow2Picon"] == '29':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrow2Picon"] == '30':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrow2Picon"] == '31':
				return _('Clear')
			elif WeatherInfo["forecastTomorrow2Picon"] == '32':
				return _('Sunny')
			elif WeatherInfo["forecastTomorrow2Picon"] == '33':
				return _('Fair')
			elif WeatherInfo["forecastTomorrow2Picon"] == '34':
				return _('Fair')
			elif WeatherInfo["forecastTomorrow2Picon"] == '35':
				return _('Mixed rain\n and hail')
			elif WeatherInfo["forecastTomorrow2Picon"] == '36':
				return _('Hot')
			elif WeatherInfo["forecastTomorrow2Picon"] == '37':
				return _('Isolated\n thunderstorms')
			elif WeatherInfo["forecastTomorrow2Picon"] == '38':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["forecastTomorrow2Picon"] == '39':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["forecastTomorrow2Picon"] == '40':
				return _('Scattered\n showers')
			elif WeatherInfo["forecastTomorrow2Picon"] == '41':
				return _('Heavy snow')
			elif WeatherInfo["forecastTomorrow2Picon"] == '42':
				return _('Scattered\n snow showers')
			elif WeatherInfo["forecastTomorrow2Picon"] == '43':
				return _('Heavy snow')
			elif WeatherInfo["forecastTomorrow2Picon"] == '44':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrow2Picon"] == '45':
				return _('Thundershowers')
			elif WeatherInfo["forecastTomorrow2Picon"] == '46':
				return _('Snow showers')
			elif WeatherInfo["forecastTomorrow2Picon"] == '47':
				return _('Isolated\n thundershowers')
			elif WeatherInfo["forecastTomorrow2Picon"] == '3200':
				return _('Not\n available')
			else:
				return "N/A"
		elif self.type == "forecastTomorrow2Picon":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3Code":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3Day":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3Date":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3TempMin":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3TempMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3TempMinMax":
			return WeatherInfo[self.type]
		elif self.type == "forecastTomorrow3Text":
			if WeatherInfo["forecastTomorrow3Picon"] == '0':
				return _('Tornado')
			elif WeatherInfo["forecastTomorrow3Picon"] == '1':
				return _('Tropical\n storm')
			elif WeatherInfo["forecastTomorrow3Picon"] == '2':
				return _('Hurricane')
			elif WeatherInfo["forecastTomorrow3Picon"] == '3':
				return _('Severe\n thunderstorms')
			elif WeatherInfo["forecastTomorrow3Picon"] == '4':
				return _('Thunderstorms')
			elif WeatherInfo["forecastTomorrow3Picon"] == '5':
				return _('Mixed rain\n and snow')
			elif WeatherInfo["forecastTomorrow3Picon"] == '6':
				return _('Mixed rain\n and sleet')
			elif WeatherInfo["forecastTomorrow3Picon"] == '7':
				return _('Mixed snow\n and sleet')
			elif WeatherInfo["forecastTomorrow3Picon"] == '8':
				return _('Freezing\n drizzle')
			elif WeatherInfo["forecastTomorrow3Picon"] == '9':
				return _('Drizzle')
			elif WeatherInfo["forecastTomorrow3Picon"] == '10':
				return _('Freezing\n rain')
			elif WeatherInfo["forecastTomorrow3Picon"] == '11':
				return _('Showers')
			elif WeatherInfo["forecastTomorrow3Picon"] == '12':
				return _('Rain')
			elif WeatherInfo["forecastTomorrow3Picon"] == '13':
				return _('Snow\n flurries')
			elif WeatherInfo["forecastTomorrow3Picon"] == '14':
				return _('Light\n snow showers')
			elif WeatherInfo["forecastTomorrow3Picon"] == '15':
				return _('Blowing\n snow')
			elif WeatherInfo["forecastTomorrow3Picon"] == '16':
				return _('Snow')
			elif WeatherInfo["forecastTomorrow3Picon"] == '17':
				return _('Hail')
			elif WeatherInfo["forecastTomorrow3Picon"] == '18':
				return _('Sleet')
			elif WeatherInfo["forecastTomorrow3Picon"] == '19':
				return _('Dust')
			elif WeatherInfo["forecastTomorrow3Picon"] == '20':
				return _('Foggy')
			elif WeatherInfo["forecastTomorrow3Picon"] == '21':
				return _('Haze')
			elif WeatherInfo["forecastTomorrow3Picon"] == '22':
				return _('Smoky')
			elif WeatherInfo["forecastTomorrow3Picon"] == '23':
				return _('Blustery')
			elif WeatherInfo["forecastTomorrow3Picon"] == '24':
				return _('Windy')
			elif WeatherInfo["forecastTomorrow3Picon"] == '25':
				return _('Cold')
			elif WeatherInfo["forecastTomorrow3Picon"] == '26':
				return _('Cloudy')
			elif WeatherInfo["forecastTomorrow3Picon"] == '27':
				return _('Mostly\n cloudy')
			elif WeatherInfo["forecastTomorrow3Picon"] == '28':
				return _('Mostly\n cloudy')
			elif WeatherInfo["forecastTomorrow3Picon"] == '29':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrow3Picon"] == '30':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrow3Picon"] == '31':
				return _('Clear')
			elif WeatherInfo["forecastTomorrow3Picon"] == '32':
				return _('Sunny')
			elif WeatherInfo["forecastTomorrow3Picon"] == '33':
				return _('Fair')
			elif WeatherInfo["forecastTomorrow3Picon"] == '34':
				return _('Fair')
			elif WeatherInfo["forecastTomorrow3Picon"] == '35':
				return _('Mixed rain\n and hail')
			elif WeatherInfo["forecastTomorrow3Picon"] == '36':
				return _('Hot')
			elif WeatherInfo["forecastTomorrow3Picon"] == '37':
				return _('Isolated\n thunderstorms')
			elif WeatherInfo["forecastTomorrow3Picon"] == '38':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["forecastTomorrow3Picon"] == '39':
				return _('Scattered\n thunderstorms')
			elif WeatherInfo["forecastTomorrow3Picon"] == '40':
				return _('Scattered\n showers')
			elif WeatherInfo["forecastTomorrow3Picon"] == '41':
				return _('Heavy snow')
			elif WeatherInfo["forecastTomorrow3Picon"] == '42':
				return _('Scattered\n snow showers')
			elif WeatherInfo["forecastTomorrow3Picon"] == '43':
				return _('Heavy snow')
			elif WeatherInfo["forecastTomorrow3Picon"] == '44':
				return _('Partly\n cloudy')
			elif WeatherInfo["forecastTomorrow3Picon"] == '45':
				return _('Thundershowers')
			elif WeatherInfo["forecastTomorrow3Picon"] == '46':
				return _('Snow showers')
			elif WeatherInfo["forecastTomorrow3Picon"] == '47':
				return _('Isolated\n thundershowers')
			elif WeatherInfo["forecastTomorrow3Picon"] == '3200':
				return _('Not\n available')
			else:
				return "N/A"
		elif self.type == "forecastTomorrow3Picon":
			return WeatherInfo[self.type]
		elif self.type == "title":
			return "°" + " | " + WeatherInfo[self.type]
		elif self.type == "CF":
			return "°"
		else:
			return ""

	text = property(getText)

class WeatherData:
	def __init__(self):
		self.WeatherInfo = WeatherInfo = { 
			"currentLocation": "N/A",
			"currentDirection": "N/A",
			"currentWind": "N/A",
			"feels2": "N/A",
			"feels": "N/A",
			"klima": "N/A",
			"currentWeatherCode": "(",
			"currentWeatherText": "N/A",
			"currentWeatherPicon": "N/A",
			"currentWeatherTemp": "=",
			"forecastTodayCode": "(",
			"forecastTodayText": "N/A",
			"forecastTodayPicon": "N/A",
			"forecastTodayDay": "N/A",
			"forecastTodayDate": "N/A",
			"forecastTodayDateEn": "N/A",
			"forecastTodayTempMin": "0",
			"forecastTodayTempMax": "0",
			"forecastTodayTempMinMax": "0",
			"forecastTomorrowCode": "(",
			"forecastTomorrowText": "N/A",
			"forecastTomorrowPicon": "N/A",
			"forecastTomorrowDay": "N/A",
			"forecastTomorrowDate": "N/A",
			"forecastTomorrowDateEn": "N/A",
			"forecastTomorrowTempMin": "0",
			"forecastTomorrowTempMax": "0",
			"forecastTomorrowTempMinMax": "0",
			"forecastTomorrow1Code": "(",
			"forecastTomorrow1Text": "N/A",
			"forecastTomorrow1Picon": "N/A",
			"forecastTomorrow1Day": "N/A",
			"forecastTomorrow1Date": "N/A",
			"forecastTomorrow1TempMin": "0",
			"forecastTomorrow1TempMax": "0",
			"forecastTomorrow1TempMinMax": "0",
			"forecastTomorrow2Code": "(",
			"forecastTomorrow2Text": "N/A",
			"forecastTomorrow2Picon": "N/A",
			"forecastTomorrow2Day": "N/A",
			"forecastTomorrow2Date": "N/A",
			"forecastTomorrow2TempMin": "0",
			"forecastTomorrow2TempMax": "0",
			"forecastTomorrow2TempMinMax": "0",
			"forecastTomorrow3Code": "(",
			"forecastTomorrow3Text": "N/A",
			"forecastTomorrow3Picon": "N/A",
			"forecastTomorrow3Day": "N/A",
			"forecastTomorrow3Date": "N/A",
			"forecastTomorrow3TempMin": "0",
			"forecastTomorrow3TempMax": "0",
			"forecastTomorrow3TempMinMax": "0",
		}
		if config.plugins.XionHDF.refreshInterval.value > 0 and load_data:
			self.timer = eTimer()
			self.timer.callback.append(self.GetWeather)
			self.GetWeather()

	def downloadError(self, error = None):
		print "[WeatherUpdate] error fetching weather data"

	def GetWeather(self):
		global look_again
		global look_count
		global weather_data_old
		
		url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%3D%22"+str(config.plugins.XionHDF.weather_city.value)+"%22&format=xml"
		timeout = int(config.plugins.XionHDF.refreshInterval.value) * 1000.0 * 60.0
		retry_timeout = 15555
		
		if timeout > 0:
			if weather_data is None:
				look_count = 1
				print "XionWeather lookup 1 for ID " + str(config.plugins.XionHDF.weather_city.value)
				getPage(url,method = 'GET').addCallback(self.GotWeatherData).addErrback(self.downloadError)
				self.timer.start(retry_timeout, True)
				look_again = True
			else:
				adate = strftime("%-d. %b", time.localtime()).replace('Dez','Dec').replace('Mai','May').replace('Okt','Oct').replace('Mrz','Mar')
				ddate = weather_data.WeatherInfo["forecastTodayDateEn"]
				mdate = weather_data.WeatherInfo["forecastTomorrowDateEn"]
				looking = look_again
				if adate not in (ddate,mdate):
					look_count +=1
					print "XionWeather: Weather data for "+str(ddate)+" is not for current day: "+str(adate)
					print "XionWeather: Weather lookup "+str(look_count)+" for ID " + str(config.plugins.XionHDF.weather_city.value)
					getPage(url,method = 'GET').addCallback(self.GotWeatherData).addErrback(self.downloadError)
					self.timer.start(retry_timeout, True)
					look_again = True
				elif looking:
					look_count = 0
					print "XionWeather: Weather data is correct, next lookup in "+str(config.plugins.XionHDF.refreshInterval.value)+" minutes"
					weather_data_old = deepcopy(weather_data)
					self.timer.start(int(timeout), True)
					look_again = False
				else:
					look_count +=1
					print "XionWeather: Weather lookup "+str(look_count)+" for ID "+str(config.plugins.XionHDF.weather_city.value)
					getPage(url,method = 'GET').addCallback(self.GotWeatherData).addErrback(self.downloadError)
					self.timer.start(retry_timeout, True)
					look_again = True

	def GotWeatherData(self, data = None):
		if data is not None:
			dom = parseString(data)
			title = self.getText(dom.getElementsByTagName('title')[0].childNodes)
			self.WeatherInfo["currentLocation"] = str(title).split(',')[0].replace("Yahoo! Weather - ","")
			weather = dom.getElementsByTagName('yweather:wind')[0]
			self.WeatherInfo["currentDirection"] = _(str(weather.getAttributeNode('direction').nodeValue))
			if not self.WeatherInfo["currentDirection"] is 'N/A':
				direct = int(self.WeatherInfo["currentDirection"])
				if direct >= 0 and direct <= 20:
					wdirect = _('N')
				elif direct >= 21 and direct <= 35:
					wdirect = _('N-NE')
				elif direct >= 36 and direct <= 55:
					wdirect = _('NE')
				elif direct >= 56 and direct <= 70:
					wdirect = _('E-NE')
				elif direct >= 71 and direct <= 110:
					wdirect = _('E')
				elif direct >= 111 and direct <= 125:
					wdirect = _('E-SE')
				elif direct >= 126 and direct <= 145:
					wdirect = _('SE')
				elif direct >= 146 and direct <= 160:
					wdirect = _('S-SE')
				elif direct >= 161 and direct <= 200:
					wdirect = _('S')
				elif direct >= 201 and direct <= 215:
					wdirect = _('S-SW')
				elif direct >= 216 and direct <= 235:
					wdirect = _('SW')
				elif direct >= 236 and direct <= 250:
					wdirect = _('W-SW')
				elif direct >= 251 and direct <= 290:
					wdirect = _('W')
				elif direct >= 291 and direct <= 305:
					wdirect = _('W-NW')
				elif direct >= 306 and direct <= 325:
					wdirect = _('NW')
				elif direct >= 326 and direct <= 340:
					wdirect = _('N-NW')
				elif direct >= 341 and direct <= 360:
					wdirect = _('N')
				else:
					wdirect = "N/A"
			else:
				wdirect = "N/A"
			
			self.WeatherInfo["currentWind"] = _(str(weather.getAttributeNode('speed').nodeValue)) + " km/h" + _(" from ") + wdirect
			self.WeatherInfo["feels2"] = self.getTemp(weather.getAttributeNode('chill').nodeValue)

			weather = dom.getElementsByTagName('yweather:atmosphere')[0]
			self.WeatherInfo["klima"] = _(str(weather.getAttributeNode('humidity').nodeValue)) + _('% humidity')

			weather = dom.getElementsByTagName('yweather:condition')[0]
			self.WeatherInfo["currentWeatherCode"] = self.ConvertCondition(weather.getAttributeNode('code').nodeValue)
			self.WeatherInfo["currentWeatherTemp"] = self.getTemp(weather.getAttributeNode('temp').nodeValue)
			self.WeatherInfo["currentWeatherText"] = _(str(weather.getAttributeNode('text').nodeValue))
			self.WeatherInfo["currentWeatherPicon"] = _(str(weather.getAttributeNode('code').nodeValue))

			self.WeatherInfo["feels"] = self.WeatherInfo["currentWeatherTemp"] + "°C" + _(", feels ") + self.WeatherInfo["feels2"] + "°C"

			weather = dom.getElementsByTagName('yweather:forecast')[0]
			self.WeatherInfo["forecastTodayCode"] = self.ConvertCondition(weather.getAttributeNode('code').nodeValue)
			self.WeatherInfo["forecastTodayDay"] = _(weather.getAttributeNode('day').nodeValue)
			self.WeatherInfo["forecastTodayDate"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTodayDateEn"] = self.getWeatherDateEn(weather)
			self.WeatherInfo["forecastTodayTempMax"] = self.getTemp(weather.getAttributeNode('high').nodeValue) + "°C"
			self.WeatherInfo["forecastTodayTempMin"] = self.getTemp(weather.getAttributeNode('low').nodeValue) + "°C"
			self.WeatherInfo["forecastTodayTempMinMax"] = self.getTemp(weather.getAttributeNode('low').nodeValue) + "°/" + self.getTemp(weather.getAttributeNode('high').nodeValue) + "°"
			self.WeatherInfo["forecastTodayText"] = _(str(weather.getAttributeNode('text').nodeValue))
			self.WeatherInfo["forecastTodayPicon"] = _(str(weather.getAttributeNode('code').nodeValue))

			weather = dom.getElementsByTagName('yweather:forecast')[1]
			self.WeatherInfo["forecastTomorrowCode"] = self.ConvertCondition(weather.getAttributeNode('code').nodeValue)
			self.WeatherInfo["forecastTomorrowDay"] = _(weather.getAttributeNode('day').nodeValue)
			self.WeatherInfo["forecastTomorrowDate"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrowDateEn"] = self.getWeatherDateEn(weather)
			self.WeatherInfo["forecastTomorrowTempMax"] = self.getTemp(weather.getAttributeNode('high').nodeValue) + "°C"
			self.WeatherInfo["forecastTomorrowTempMin"] = self.getTemp(weather.getAttributeNode('low').nodeValue) + "°C"
			self.WeatherInfo["forecastTomorrowTempMinMax"] = self.getTemp(weather.getAttributeNode('low').nodeValue) + "°/" + self.getTemp(weather.getAttributeNode('high').nodeValue) + "°"
			self.WeatherInfo["forecastTomorrowText"] = _(str(weather.getAttributeNode('text').nodeValue))
			self.WeatherInfo["forecastTomorrowPicon"] = _(str(weather.getAttributeNode('code').nodeValue))

			weather = dom.getElementsByTagName('yweather:forecast')[2]
			self.WeatherInfo["forecastTomorrow1Code"] = self.ConvertCondition(weather.getAttributeNode('code').nodeValue)
			self.WeatherInfo["forecastTomorrow1Day"] = _(weather.getAttributeNode('day').nodeValue)
			self.WeatherInfo["forecastTomorrow1Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow1TempMax"] = self.getTemp(weather.getAttributeNode('high').nodeValue) + "°C"
			self.WeatherInfo["forecastTomorrow1TempMin"] = self.getTemp(weather.getAttributeNode('low').nodeValue) + "°C"
			self.WeatherInfo["forecastTomorrow1TempMinMax"] = self.getTemp(weather.getAttributeNode('low').nodeValue) + "°/" + self.getTemp(weather.getAttributeNode('high').nodeValue) + "°"
			self.WeatherInfo["forecastTomorrow1Text"] = _(str(weather.getAttributeNode('text').nodeValue))
			self.WeatherInfo["forecastTomorrow1Picon"] = _(str(weather.getAttributeNode('code').nodeValue))

			weather = dom.getElementsByTagName('yweather:forecast')[3]
			self.WeatherInfo["forecastTomorrow2Code"] = self.ConvertCondition(weather.getAttributeNode('code').nodeValue)
			self.WeatherInfo["forecastTomorrow2Day"] = _(weather.getAttributeNode('day').nodeValue)
			self.WeatherInfo["forecastTomorrow2Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow2TempMax"] = self.getTemp(weather.getAttributeNode('high').nodeValue) + "°C"
			self.WeatherInfo["forecastTomorrow2TempMin"] = self.getTemp(weather.getAttributeNode('low').nodeValue) + "°C"
			self.WeatherInfo["forecastTomorrow2TempMinMax"] = self.getTemp(weather.getAttributeNode('low').nodeValue) + "°/" + self.getTemp(weather.getAttributeNode('high').nodeValue) + "°"
			self.WeatherInfo["forecastTomorrow2Text"] = _(str(weather.getAttributeNode('text').nodeValue))
			self.WeatherInfo["forecastTomorrow2Picon"] = _(str(weather.getAttributeNode('code').nodeValue))

			weather = dom.getElementsByTagName('yweather:forecast')[4]
			self.WeatherInfo["forecastTomorrow3Code"] = self.ConvertCondition(weather.getAttributeNode('code').nodeValue)
			self.WeatherInfo["forecastTomorrow3Day"] = _(weather.getAttributeNode('day').nodeValue)
			self.WeatherInfo["forecastTomorrow3Date"] = self.getWeatherDate(weather)
			self.WeatherInfo["forecastTomorrow3TempMax"] = self.getTemp(weather.getAttributeNode('high').nodeValue) + "°C"
			self.WeatherInfo["forecastTomorrow3TempMin"] = self.getTemp(weather.getAttributeNode('low').nodeValue) + "°C"
			self.WeatherInfo["forecastTomorrow3TempMinMax"] = self.getTemp(weather.getAttributeNode('low').nodeValue) + "°/" + self.getTemp(weather.getAttributeNode('high').nodeValue) + "°"
			self.WeatherInfo["forecastTomorrow3Text"] =_(str(weather.getAttributeNode('text').nodeValue))
			self.WeatherInfo["forecastTomorrow3Picon"] = _(str(weather.getAttributeNode('code').nodeValue))
			
	def getText(self,nodelist):
	    rc = []
	    for node in nodelist:
	        if node.nodeType == node.TEXT_NODE:
	            rc.append(node.data)
	    return ''.join(rc)

	def ConvertCondition(self, c):
		c = int(c)
		condition = "("
		if c == 0 or c == 1 or c == 2:
			condition = "S"
		elif c == 3 or c == 4:
			condition = "Z"
		elif c == 5  or c == 6 or c == 7 or c == 18:
			condition = "U"
		elif c == 8 or c == 10 or c == 25:
			condition = "G"
		elif c == 9:
			condition = "Q"
		elif c == 11 or c == 12 or c == 40:
			condition = "R"
		elif c == 13 or c == 14 or c == 15 or c == 16 or c == 41 or c == 46 or c == 42 or c == 43:
			condition = "W"
		elif c == 17 or c == 35:
			condition = "X"
		elif c == 19:
			condition = "F"
		elif c == 20 or c == 21 or c == 22:
			condition = "L"
		elif c == 23 or c == 24:
			condition = "S"
		elif c == 26 or c == 44:
			condition = "N"
		elif c == 27 or c == 29:
			condition = "I"
		elif c == 28 or c == 30:
			condition = "H"
		elif c == 31 or c == 33:
			condition = "C"
		elif c == 32 or c == 34:
			condition = "B"
		elif c == 36:
			condition = "B"
		elif c == 37 or c == 38 or c == 39 or c == 45 or c == 47:
			condition = "0"
		else:
			condition = ")"
		return str(condition)

	def getTemp(self, temp):
		celsius = (float(temp) - 32 ) * 5 / 9
		return str(int(round(float(celsius),0)))

	def getWeatherDate(self, weather):
		cur_weather = str(weather.getAttributeNode('date').nodeValue).split(" ")
		str_weather = cur_weather[0]
		if len(cur_weather) >= 2:
			str_weather += ". " + _(cur_weather[1])
		return str_weather

	def getWeatherDateEn(self, weather):
		cur_weather = str(weather.getAttributeNode('date').nodeValue).split(" ")
		str_weather = cur_weather[0]
		if len(cur_weather) >= 2:
			str_weather += ". " + cur_weather[1]
		return str_weather
