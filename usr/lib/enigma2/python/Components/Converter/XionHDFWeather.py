# -*- coding: utf-8 -*-
#
#  XionHDFWeather Converter
#
#  Coded by oerlgrey
#  Based on openHDF image source code
#
#  This code is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ 
#  or send a letter to Creative Commons, 559 Nathan 
#  Abbott Way, Stanford, California 94305, USA.
#
#  If you think this license infringes any rights,
#  please contact me at ochzoetna@gmail.com

from __future__ import absolute_import
from __future__ import print_function
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from enigma import eTimer
import requests, os, gettext, json
from six import PY3
from time import strftime, strptime, gmtime
from datetime import datetime
from math import floor
from Components.Converter.Poll import Poll
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Components.Language import language

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

if not PY3:
	from HTMLParser import HTMLParser
	_unescape = HTMLParser().unescape
else:
	from html import unescape as _unescape

WEATHER_DATA = None
WEATHER_LOAD = True
WeekDays = [_("Mon"), _("Tue"), _("Wed"), _("Thu"), _("Fri"), _("Sat"), _("Sun")]

def Code_utf8(value):
	value = "" if value is None else _unescape(value)
	if not PY3:
		value = value.replace('\xc2\x86', '').replace('\xc2\x87', '').decode("utf-8", "ignore").encode("utf-8") or ""
		return decode(value, 'UTF-8')
	else:
		value.replace('\x86', '').replace('\x87', '')
		return value

def getDirection(angle):
	def normalize_angle(angle):
		cycles = angle / 360.
		normalized_cycles = cycles - floor(cycles)
		return normalized_cycles * 360.
	direction_names = [_("N"), _("N-NE"), _("NE"), _("E-NE"), _("E"), _("E-SE"), _("SE"), _("S-SE"), _("S"), _("S-SW"), _("SW"), _("W-SW"), _("W"), _("W-NW"), _("NW"), _("N-NW")]
	directions_num = len(direction_names)
	directions_step = 360. / directions_num
	index = int(round(normalize_angle(angle) / directions_step))
	index %= directions_num
	return direction_names[index]

class XionHDFWeather(Poll, Converter, object):
	def __init__(self, type):
		_type = type
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.poll_interval = 60000
		self.poll_enabled = True
		_type = _type.split(',')
		self.day_value = _type[0]
		self.type = _type[1]
		self.timer = eTimer()
		self.timer.callback.append(self.reset)
		self.timer.callback.append(self.get_Data)
		self.data = None
		self.zerolist = [0] * 24
		self.nalist = ["na"] * 24
		self.get_Data()

	@cached
	def getText(self):
		global WEATHER_DATA

		self.data = WEATHER_DATA
		day = self.day_value.split('_')[1]
		if self.type == "DayTemp":
			return self.getDayTemp()
		elif self.type == "FeelTemp":
			return self.getFeelTemp()
		elif self.type == 'MinTemp':
			return self.getMinTemp(int(day))
		elif self.type == 'MaxTemp':
			return self.getMaxTemp(int(day))
		elif self.type == 'MinMaxTemp':
			return self.getMinMax()
		elif self.type == "Humidity":
			return self.getHumidity()
		elif self.type == "Wind":
			return self.getWind()
		elif self.type == "City":
			return str(config.plugins.XionHDF.weather_foundcity.value)
		elif self.type == "MeteoFont":
			return self.getMeteoFont(int(day))
		elif self.type == "Description":
			return self.getMeteoText(int(day))
		elif self.type == 'WetterDate':
			return self.getShortday(int(day))
		else:
			return ""

	text = property(getText)

	def reset(self):
		global WEATHER_LOAD

		WEATHER_LOAD = True
		self.timer.stop()

	def get_Data(self):
		global WEATHER_DATA
		global WEATHER_LOAD

		if WEATHER_LOAD:
			try:
				print("[XionHDF]: download from URL")
				timezones = {"-06": "America/Anchorage", "-05": "America/Los_Angeles", "-04": "America/Denver", "-03": "America/Chicago", "-02": "America/New_York", "-01": "America/Sao_Paulo", "+00": "Europe/London", "+01": "Europe/Berlin", "+02": "Europe/Moscow", "+03": "Africa/Cairo", "+04": "Asia/Bangkok", "+05": "Asia/Singapore", "+06": "Asia/Tokyo", "+07": "Australia/Sydney", "+08": "Pacific/Auckland"}
				currzone = timezones.get(strftime("%z", gmtime())[:3], "Europe/Berlin")
				url = 'https://api.open-meteo.com/v1/forecast?longitude=%s&latitude=%s&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,weathercode,windspeed_10m,winddirection_10m,precipitation_probability&daily=sunrise,sunset,weathercode,precipitation_probability_max,temperature_2m_max,temperature_2m_min&timezone=%s&windspeed_unit=kmh&temperature_unit=celsius' % (str(config.plugins.XionHDF.weather_longitude.value), str(config.plugins.XionHDF.weather_latitude.value), currzone)
				res = requests.get(url, timeout=3)
				self.data = res.json()
				WEATHER_DATA = self.data
				WEATHER_LOAD = False
			except:
				pass
			timeout = max(15, int(config.plugins.XionHDF.refreshInterval.value)) * 1000.0 * 60.0
			self.timer.start(int(timeout), True)
		else:
			self.data = WEATHER_DATA

	def getDayTemp(self):
		try:
			if self.data.get("hourly", None) is not None and self.data.get("daily", None) is not None:
				isotime = datetime.now().strftime("%FT%H:00")
				current = self.data.get("hourly", {})
				for idx, time in enumerate(current.get("time", [])):
					if isotime in time:
						value = "%.0f" % current.get("temperature_2m", self.zerolist)[idx]
						return str(value) + "°C"
		except:
			return ""

	def getFeelTemp(self):
		try:
			if self.data.get("hourly", None) is not None and self.data.get("daily", None) is not None:
				isotime = datetime.now().strftime("%FT%H:00")
				current = self.data.get("hourly", {})
				for idx, time in enumerate(current.get("time", [])):
					if isotime in time:
						cur_temp = "%.0f" % current.get("temperature_2m", self.zerolist)[idx]
						feel_temp = "%.0f" % current.get("apparent_temperature", self.zerolist)[idx]
						return str(cur_temp) + '°C' + _(", feels ") + str(feel_temp) + '°C'
		except:
			return ""

	def getHumidity(self):
		try:
			if self.data.get("hourly", None) is not None and self.data.get("daily", None) is not None:
				isotime = datetime.now().strftime("%FT%H:00")
				current = self.data.get("hourly", {})
				for idx, time in enumerate(current.get("time", [])):
					if isotime in time:
						value = "%.0f%%" % current.get("relativehumidity_2m", self.zerolist)[idx]
						return value.replace('%', '') + _('% humidity')
		except:
			return ""

	def getWind(self):
		try:
			if self.data.get("hourly", None) is not None and self.data.get("daily", None) is not None:
				isotime = datetime.now().strftime("%FT%H:00")
				current = self.data.get("hourly", {})
				for idx, time in enumerate(current.get("time", [])):
					if isotime in time:
						value = "%.0f km/h %s" % (current.get("windspeed_10m", self.zerolist)[idx], getDirection(current.get("winddirection_10m", self.nalist)[idx]))
						return str(value)
		except:
			return ""

	def getMinTemp(self, day):
		try:
			if self.data.get("hourly", None) is not None and self.data.get("daily", None) is not None:
				forecast = self.data["daily"]
				if day in range(6):
					value = "%.0f" % forecast.get("temperature_2m_min", self.zerolist)[day]
					return str(value) + '°C'
		except:
			return ""

	def getMaxTemp(self, day):
		try:
			if self.data.get("hourly", None) is not None and self.data.get("daily", None) is not None:
				forecast = self.data["daily"]
				if day in range(6):
					value = "%.0f" % forecast.get("temperature_2m_max", self.zerolist)[day]
					return str(value) + '°C'
		except:
			return ""

	def getMinMax(self, day):
		try:
			if self.data.get("hourly", None) is not None and self.data.get("daily", None) is not None:
				forecast = self.data["daily"]
				if day in range(6):
					min = "%.0f" % forecast.get("temperature_2m_min", self.zerolist)[day]
					max = "%.0f" % forecast.get("temperature_2m_max", self.zerolist)[day]
					return str(min) + "° / " + str(max) + "°"
		except:
			return ""

	def getShortday(self, day):
		try:
			if self.data.get("hourly", None) is not None and self.data.get("daily", None) is not None:
				global WeekDays
				forecast = self.data["daily"]
				if day in range(6):
					value = Code_utf8(WeekDays[strptime(forecast.get("time", self.zerolist)[day], "%Y-%m-%d").tm_wday])
					return str(value)
		except:
			return ""

	def getMeteoText(self, day):
		try:
			if self.data.get("hourly", None) is not None and self.data.get("daily", None) is not None:
				if day == 0:
					isotime = datetime.now().strftime("%FT%H:00")
					current = self.data.get("hourly", {})
					for idx, time in enumerate(current.get("time", [])):
						if isotime in time:
							value = int(current.get("weathercode", self.nalist)[idx])
							text = self.setDescription(value)
							return str(text)
				else:
					forecast = self.data["daily"]
					if day in range(6):
						value = int(forecast.get("weathercode", self.zerolist)[day])
						text = self.setDescription(value)
						return str(text)
		except:
			return ""

	def getMeteoFont(self, day):
		try:
			if self.data.get("hourly", None) is not None and self.data.get("daily", None) is not None:
				if day == 0:
					isotime = datetime.now().strftime("%FT%H:00")
					current = self.data.get("hourly", {})
					for idx, time in enumerate(current.get("time", [])):
						if isotime in time:
							value = int(current.get("weathercode", self.nalist)[idx])
							font = self.setMeteoFont(value)
							return str(font)
				else:
					forecast = self.data["daily"]
					if day in range(6):
						value = int(forecast.get("weathercode", self.zerolist)[day])
						font = self.setMeteoFont(value)
						return str(font)
		except:
			return ""

	def setMeteoFont(self, value):
		if value == 0:
			return "B" # sun
		elif value in (1, 2):
			return "H" # sun + cloud
		elif value == 3:
			return "Y" # clouds
		elif value in (45, 48):
			return "M" # fog
		elif value in (95, 96, 99):
			return "P" # thunderstorm
		elif value in (51, 61, 80):
			return "Q" # slight rain
		elif value in (53, 55, 63, 65, 81, 82):
			return "R" # rain
		elif value in (71, 85):
			return "U" # slight snow
		elif value in (73, 75, 86):
			return "W" # snow
		elif value in (56, 57, 66, 67, 77):
			return "X" # sleet
		else:
			return "(" # compass

	def setDescription(self, value):
		if value == 0:
			return _("clear sky")
		elif value == 1:
			return _("mainly clear")
		elif value == 2:
			return _("partly cloudy")
		elif value == 3:
			return _("overcast")
		elif value == 45:
			return _("foggy")
		elif value == 48:
			return _("rime fog")
		elif value == 51:
			return _("light drizzle")
		elif value == 53:
			return _("moderate drizzle")
		elif value == 55:
			return _("dense drizzle")
		elif value == 56:
			return _("light freezing drizzle")
		elif value == 57:
			return _("dense freezing drizzle")
		elif value == 61:
			return _("slight rain")
		elif value == 63:
			return _("moderate rain")
		elif value == 65:
			return _("heavy rain")
		elif value == 66:
			return _("light freezing rain")
		elif value == 67:
			return _("heavy freezing rain")
		elif value == 71:
			return _("slight snow fall")
		elif value == 73:
			return _("moderate snow fall")
		elif value == 75:
			return _("heavy snow fall")
		elif value == 77:
			return _("snow grains")
		elif value == 80:
			return _("slight rain showers")
		elif value == 81:
			return _("moderate rain showers")
		elif value == 82:
			return _("violent rain showers")
		elif value == 85:
			return _("slight snow showers")
		elif value == 86:
			return _("heavy snow showers")
		elif value == 95:
			return _("slight thunderstorm")
		elif value == 96:
			return _("thunderstorm with slight hail")
		elif value == 99:
			return _("thunderstorm with heavy hail")
		else:
			return ""
