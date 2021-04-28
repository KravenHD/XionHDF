# XionHDFServiceInfo2 based on standard ServiceInfo

from Poll import Poll
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached

class XionHDFServiceInfo2(Poll, Converter, object):

	xAPID = 0
	xVPID = 1
	xSID = 2
	xONID = 3
	xTSID = 4
	sCAIDs = 5
	yAll = 6
	xAll = 7
	xVTYPE = 8
	xATYPE = 9
	xALLTYPE = 10
	VideoHeight = 11
	VideoWidth = 12
	Framerate = 13
	Provider = 14

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type, self.interesting_events = {
				"xAPID": (self.xAPID, (iPlayableService.evUpdatedInfo,)),
				"xVPID": (self.xVPID, (iPlayableService.evUpdatedInfo,)),
				"xSID": (self.xSID, (iPlayableService.evUpdatedInfo,)),
				"xONID": (self.xONID, (iPlayableService.evUpdatedInfo,)),
				"xTSID": (self.xTSID, (iPlayableService.evUpdatedInfo,)),
				"sCAIDs": (self.sCAIDs, (iPlayableService.evUpdatedInfo,)),
				"yAll": (self.yAll, (iPlayableService.evUpdatedInfo,)),
				"xAll": (self.xAll, (iPlayableService.evUpdatedInfo,)),
				"xVTYPE": (self.xVTYPE, (iPlayableService.evUpdatedInfo,)),
				"xATYPE": (self.xATYPE, (iPlayableService.evUpdatedInfo,)),
				"xALLTYPE": (self.xALLTYPE, (iPlayableService.evUpdatedInfo,)),
				"VideoHeight": (self.VideoHeight, (iPlayableService.evUpdatedInfo,)),
				"VideoWidth": (self.VideoWidth, (iPlayableService.evUpdatedInfo,)),
				"Framerate": (self.Framerate, (iPlayableService.evVideoSizeChanged, iPlayableService.evUpdatedInfo,)),
				"Provider": (self.Provider, (iPlayableService.evUpdatedInfo,)),
			}[type]
		self.poll_interval = 1000
		self.poll_enabled = True

	def getServiceInfoString(self, info, what, convert=lambda x: "%d" % x):
		v = info.getInfo(what)
		if v == -1:
			return "N/A"
		if v == -2:
			return info.getInfoString(what)
		if v == -3:
			t_objs = info.getInfoObject(what)
			if t_objs and (len(t_objs) > 0):
				ret_val = ""
				for t_obj in t_objs:
					ret_val += "%.4X " % t_obj
				return ret_val[:-1]
			else:
				return ""
		return convert(v)

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""
		if self.type == self.xAPID:
			try:
				return "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sAudioPID))
			except:
				return "N/A"
		elif self.type == self.xVTYPE:
			return ("MPEG2", "AVC", "H263", "VC1", "MPEG4-VC", "VC1-SM", "MPEG1", "HEVC", "VP8", "VP9", "XVID", "N/A 11", "N/A 12", "DIVX 3", "DIVX 4", "DIVX 5", "AVS", "N/A 17", "VP6", "N/A 19", "N/A 20", "SPARK", "")[info.getInfo(iServiceInformation.sVideoType)]
		elif self.type == self.xALLTYPE:
			audio = service.audioTracks()
			try:
				return "%s%s" % (("MPEG2/", "AVC/", "H263/", "VC1/", "MPEG4-VC/", "VC1-SM/", "MPEG1/", "HEVC/", "VP8/", "VP9/", "XVID/", "N/A 11/", "N/A 12/", "DIVX 3/", "DIVX 4/", "DIVX 5/", "AVS/", "N/A 17/", "VP6/", "N/A 19/", "N/A 20/", "SPARK/", "")[info.getInfo(iServiceInformation.sVideoType)], str(audio.getTrackInfo(audio.getCurrentTrack()).getDescription()))
			except:
				return ""
		elif self.type == self.xATYPE:
			audio = service.audioTracks()
			try:
				return str(audio.getTrackInfo(audio.getCurrentTrack()).getDescription())
			except:
				return ""
		elif self.type == self.xVPID:
			try:
				return "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sVideoPID))
			except:
				return "N/A"
		elif self.type == self.xSID:
			try:
				return "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sSID))
			except:
				return "N/A"
		elif self.type == self.xTSID:
			try:
				return "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sTSID))
			except:
				return "N/A"
		elif self.type == self.xONID:
			try:
				return "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sONID))
			except:
				return "N/A"
		elif self.type == self.sCAIDs:
			try:
				return self.getServiceInfoString(info, iServiceInformation.sCAIDs)
			except:
				return "N/A"
		elif self.type == self.yAll:
			try:
				return "SID: %0.4X  VPID: %0.4X  APID: %0.4X  TSID: %0.4X  ONID: %0.4X" % (int(self.getServiceInfoString(info, iServiceInformation.sSID)), int(self.getServiceInfoString(info, iServiceInformation.sVideoPID)), int(self.getServiceInfoString(info, iServiceInformation.sAudioPID)), int(self.getServiceInfoString(info, iServiceInformation.sTSID)), int(self.getServiceInfoString(info, iServiceInformation.sONID)))
			except:
				try:
					return "SID: %0.4X  APID: %0.4X  TSID: %0.4X  ONID: %0.4X" % (int(self.getServiceInfoString(info, iServiceInformation.sSID)), int(self.getServiceInfoString(info, iServiceInformation.sAudioPID)), int(self.getServiceInfoString(info, iServiceInformation.sTSID)), int(self.getServiceInfoString(info, iServiceInformation.sONID)))
				except:
					return " "
		elif self.type == self.xAll:
			try:
				return "SID: %0.4X  VPID: %0.4X APID: %0.4X" % (int(self.getServiceInfoString(info, iServiceInformation.sSID)), int(self.getServiceInfoString(info, iServiceInformation.sVideoPID)), int(self.getServiceInfoString(info, iServiceInformation.sAudioPID)))
			except:
				try:
					return "SID: %0.4X  APID: %0.4X" % (int(self.getServiceInfoString(info, iServiceInformation.sSID)), int(self.getServiceInfoString(info, iServiceInformation.sAudioPID)))
				except:
					return " "
		elif self.type == self.VideoHeight:
			yres = info.getInfo(iServiceInformation.sVideoHeight)
			if yres == -1:
				return " "
			mode = ("i", "p", "")[info.getInfo(iServiceInformation.sProgressive)]
			return str(yres) + mode
		elif self.type == self.VideoWidth:
			xres = info.getInfo(iServiceInformation.sVideoWidth)
			if xres == -1:
				return " "
			return str(xres)
		elif self.type == self.Framerate:
			return self.getServiceInfoString(info, iServiceInformation.sFrameRate, lambda x: "%d" % ((x + 500) / 1000))
		elif self.type == self.Provider:
			return self.getServiceInfoString(info, iServiceInformation.sProvider).upper()
		return ""

	text = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_SPECIFIC:
			if what[1] == iPlayableService.evStart or what[1] == iPlayableService.evVideoSizeChanged or what[1] == iPlayableService.evUpdatedInfo:
				Converter.changed(self, what)
		elif what[0] != self.CHANGED_SPECIFIC or what[1] in self.interesting_events:
			Converter.changed(self, what)
		elif what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
