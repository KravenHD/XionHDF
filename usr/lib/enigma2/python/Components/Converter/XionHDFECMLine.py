#
#  ECM LINE Converter
#
#  Coded by tomele for Kraven Skins
#
#  This code is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 4.0 International 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/4.0/ 
#

from enigma import iServiceInformation, iPlayableService
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from Poll import Poll

import os, gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Components.Language import language

lang = language.getLanguage()
os.environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("XionHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/XionHD/locale/"))

def _(txt):
	t = gettext.dgettext("XionHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

class XionHDFECMLine(Poll, Converter, object):

	VERYSHORT = 0
	SHORT = 1
	LONG = 2
	INVISIBLE = 3
	
	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)

		if type == "VeryShort":
			self.type = self.VERYSHORT
		elif type == "Short":
			self.type = self.SHORT
		elif type == "Long":
			self.type = self.LONG
		else:
			self.type = self.INVISIBLE

		self.poll_interval = 1000
		self.poll_enabled = True

	@cached
	def getText(self):

		ecmline = ''

		if self.IsCrypted():
			
			try:
				f = open('/tmp/ecm.info', 'r')
				flines = f.readlines()
				f.close()
			except:
				pass
			else:
				camInfo = {}
				for line in flines:
					r = line.split(':', 1)
					if len(r) > 1 :
						camInfo[r[0].strip('\n\r\t ')] = r[1].strip('\n\r\t ')
	
				caid = camInfo.get('caid','')
				
				caid = caid.lstrip('0x')
				caid = caid.upper()
				caid = caid.zfill(4)
				
				if ((caid>='0100') and (caid<='01FF')):
					system = 'System: SECA'
				elif ((caid>='0500') and (caid<='05FF')):
					system = 'System: VIACCESS'
				elif ((caid>='0600') and (caid<='06FF')):
					system = 'System: IRDETO'
				elif ((caid>='0900') and (caid<='09FF')):
					system = 'System: NDS'
				elif ((caid>='0B00') and (caid<='0BFF')):
					system = 'System: CONAX'
				elif ((caid>='0D00') and (caid<='0DFF')):
					system = 'System: CWORKS'
				elif ((caid>='0E00') and (caid<='0EFF')):
					system = 'System: POWERVU'
				elif ((caid>='1700') and (caid<='17FF')):
					system = 'System: BETA'
				elif ((caid>='1800') and (caid<='18FF')):
					system = 'System: NAGRA'
				else:
					system = _('not available')
	
				caid = 'CAID: ' + caid
				
				prov = camInfo.get('prov','')
				prov = prov.lstrip("0x")
				prov = prov.upper()
				prov = prov.zfill(6)
				prov = 'Provider: ' + prov
				
				ecmtime = camInfo.get('ecm time','')
				if ecmtime:
					if "msec" in ecmtime:
						ecmtime = 'ECM: ' + ecmtime				
					else:
						ecmtime = 'ECM: ' + ecmtime	+ ' s'			
	
				hops = 'Hops: ' + str(camInfo.get('hops',''))
				address = 'Server: ' + str(camInfo.get('address',''))
				reader = 'Reader: ' + str(camInfo.get('reader',''))
				source = 'Source: ' + str(camInfo.get('source',''))
				
				using = str(camInfo.get('using',''))
	
				active = ''
				
				if  source == 'emu':
					active = 'EMU'
					ecmline = active + ' - ' + caid
				
				elif using == 'emu':
					active = 'EMU'
					if self.type == self.VERYSHORT:
						ecmline = caid + ', ' + ecmtime
					else:
						ecmline = active + ' - ' + caid + ' - ' + ecmtime
					
				elif 'system' in camInfo :
					active = 'CCCAM'
					if self.type == self.VERYSHORT:
						ecmline = caid + ', ' + ecmtime
					elif self.type == self.SHORT:
						ecmline = caid + ' - ' + address + ' - ' + ecmtime
					else:
						ecmline = active + ' - ' + caid + ' - ' + system + ' - ' + address + ' - ' + hops + ' - ' + ecmtime					
	
				elif 'reader' in camInfo :
					active = 'OSCAM'
					if self.type == self.VERYSHORT:
						ecmline = caid + ', ' + ecmtime
					elif self.type == self.SHORT:
						ecmline = caid + ' - ' + reader + ' - ' + ecmtime
					else:
						ecmline = active + ' - ' + caid + ' - ' + system + ' - ' + reader + ' - ' + hops + ' - ' + ecmtime
	
				elif 'prov' in camInfo :
					active = 'MGCAMD'
					if self.type == self.VERYSHORT:
						ecmline = caid + ', ' + ecmtime
					elif self.type == self.SHORT:
						ecmline = caid + ' - ' + prov + ' - ' + ecmtime
					else:
						ecmline = active + ' - ' + caid + ' - ' + system + ' - ' + prov + ' - ' + source + ' - ' + ecmtime
	
				else:
					active = 'Unknown'
					ecmline = _('not available')

		else:
			if self.type == self.INVISIBLE:
				ecmline = ''
			else:
				ecmline = _('free to air')		
					
		return ecmline

	text = property(getText)

	@cached
	def IsCrypted(self):
		crypted = 0
		service = self.source.service
		if service:
			info = service and service.info()
			if info:
				crypted = info.getInfo(iServiceInformation.sIsCrypted)
		return crypted
			
	def changed(self, what):
		if (what[0] == self.CHANGED_SPECIFIC and what[1] == iPlayableService.evUpdatedInfo) or what[0] == self.CHANGED_POLL:
			Converter.changed(self, what)

