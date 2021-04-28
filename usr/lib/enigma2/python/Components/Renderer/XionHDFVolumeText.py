#
#  VOLUME TO TEXT Converter
#
#  Coded by tomele for Kraven Skins
#  Thankfully inspired by fromhell555
#
#  This code is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ 
#  or send a letter to Creative Commons, 559 Nathan 
#  Abbott Way, Stanford, California 94305, USA.
#

from __future__ import absolute_import
from .Renderer import Renderer
from Components.VariableText import VariableText
from enigma import eLabel, eDVBVolumecontrol, eTimer

class XionHDFVolumeText(Renderer, VariableText):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.vol_timer = eTimer()
		self.vol_timer.callback.append(self.poll)
	GUI_WIDGET = eLabel

	def poll(self):
		self.changed(None)

	def onHide(self):
		self.suspended = True
		self.vol_timer.stop()
		
	def onShow(self):
		self.suspended = False
		self.vol_timer.start(200)

	def changed(self, what):
		if not self.suspended:
			self.text = str(eDVBVolumecontrol.getInstance().getVolume())
