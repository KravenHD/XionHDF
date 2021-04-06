#!/usr/bin/python
# -*- coding: utf-8 -*-
#written and © by .:TBX:. 
# on Sat-Soft.net/forum
#      10/2015
import re
from Components.config import config
FILE = "/usr/share/enigma2/XionHDF/skin.xml"
TMPFILE = FILE + ".tmp"

class ChangeSkin():
        
        def __init__(self, session):
                self.session = session
                self.onClose = [ ]                                                  
                self.do_update()   

        
        def do_update(self):
                self.skin_mode = config.plugins.XionHDF.skin_mode.value
                self.debug('SkinMode is set to: ' + self.skin_mode)
                
                with open(TMPFILE, 'r') as xFile:
                     self.lines = xFile.readlines()
                     tmp_skin_resolution = re.search('resolution bpp="32" xres="(.+?)" yres="(.+?)"', str(self.lines)).groups(1)
                
                # HD Skin 1080 x 720
                if self.skin_mode == 'hd':
                   self.x_factor = float(1280) / float(tmp_skin_resolution[0])
                   self.y_factor = float(720) / float(tmp_skin_resolution[1])
                   resolution = '<resolution bpp="32" xres="1280" yres="720" />'
                   self.debug('Resolution is set to: ' + resolution)
                   self.debug('X-Factor is set to: ' + str(self.x_factor))
                   self.debug('Y-Factor is set to: ' + str(self.y_factor))
                # FullHD Skin 1920 x 1080
                elif self.skin_mode == 'fullhd':
                   self.x_factor = float(1920) / float(tmp_skin_resolution[0])
                   self.y_factor = float(1080) / float(tmp_skin_resolution[1])
                   resolution = '<resolution bpp="32" xres="1920" yres="1080" />'
                   self.debug('Resolution is set to: ' + resolution)
                   self.debug('X-Factor is set to: ' + str(self.x_factor))
                   self.debug('Y-Factor is set to: ' + str(self.y_factor))
                # UHD Skin 3840 x 2160
                elif self.skin_mode == 'uhd':
                   self.x_factor = float(3840) / float(tmp_skin_resolution[0])
                   self.y_factor = float(2160) / float(tmp_skin_resolution[1])
                   resolution = '<resolution bpp="32" xres="3840" yres="2160" />'
                   self.debug('Resolution is set to: ' + resolution)
                   self.debug('X-Factor is set to: ' + str(self.x_factor))
                   self.debug('Y-Factor is set to: ' + str(self.y_factor))
                # 4K Skin 4096 x 2160
                elif self.skin_mode == '4khd':
                   self.x_factor = float(4096) / float(tmp_skin_resolution[0])
                   self.y_factor = float(2160) / float(tmp_skin_resolution[1])
                   resolution = '<resolution bpp="32" xres="4096" yres="2160" />'
                   self.debug('Resolution is set to: ' + resolution)
                   self.debug('X-Factor is set to: ' + str(self.x_factor))
                   self.debug('Y-Factor is set to: ' + str(self.y_factor))
                # FullUHD Skin 7680 x 4320
                elif self.skin_mode == 'fulluhd':
                   self.x_factor = float(7680) / float(tmp_skin_resolution[0])
                   self.y_factor = float(4320) / float(tmp_skin_resolution[1])
                   resolution = '<resolution bpp="32" xres="7680" yres="4320" />'
                   self.debug('Resolution is set to: ' + resolution)
                   self.debug('X-Factor is set to: ' + str(self.x_factor))
                   self.debug('Y-Factor is set to: ' + str(self.y_factor))
                # 8K Skin 8192 x 4320
                elif self.skin_mode == '8khd':
                   self.x_factor = float(8192) / float(tmp_skin_resolution[0])
                   self.y_factor = float(4320) / float(tmp_skin_resolution[1])
                   resolution = '<resolution bpp="32" xres="8192" yres="4320" />'
                   self.debug('Resolution is set to: ' + resolution)
                   self.debug('X-Factor is set to: ' + str(self.x_factor))
                   self.debug('Y-Factor is set to: ' + str(self.y_factor))
                else:
                   return
        
                wFile = open(TMPFILE, 'w')
                self.debug('Start Convertion <0=======')
                count = 0
                self.skipper = '0'
                for line in self.lines:
                   old_resolution = ''   
                   new_position_string = ''
                   try:   
                          
                       if '<resolution' in line:
                          self.skipper = '1'
                          old_resolution = re.search('(<(.+?)>)', str(line)).group(0)
                          line = line.replace(old_resolution, resolution)
                    
                       if 'value="' in line and '<parameter' in line:
                          self.skipper = '2'
                          try:
                             old_value = re.search('(value="(.+?),(.+?),(.+?),(.+?)")', str(line)).groups(1)

                             wposition = old_value[1]
                             xposition = old_value[2]
                             yposition = old_value[3]
                             zposition = old_value[4]
                          
                             wposition = self.get_new_value(old_value[1], 'x')
                             xposition = self.get_new_value(old_value[2], 'y')
                             yposition = self.get_new_value(old_value[3], 'x')
                             zposition = self.get_new_value(old_value[4], 'y')
                          
                             new_position_string = 'value="%s,%s,%s,%s"' % (wposition, xposition, yposition, zposition)
                          
                          except AttributeError:
                             
                             try:
                                old_value = re.search('(value="(.+?),(.+?),(.+?)")', str(line)).groups(1)
                             
                                wposition = old_value[1]
                                xposition = old_value[2]
                                yposition = old_value[3]
                             
                                wposition = self.get_new_value(old_value[1], 'x')
                                xposition = self.get_new_value(old_value[2], 'y')
                                yposition = self.get_new_value(old_value[3], 'y')
                          
                                new_position_string = 'value="%s,%s,%s"' % (wposition, xposition, yposition)
                          
                             except AttributeError:
                                old_value = re.search('(value="(.+?),(.+?)")', str(line)).groups(1)
                             
                                xposition = old_value[1]
                                yposition = old_value[2]
                             
                                xposition = self.get_new_value(old_value[1], 'x')
                                yposition = self.get_new_value(old_value[2], 'y')
                          
                                new_position_string = 'value="%s,%s"' % (xposition, yposition)
                          
                          old_position_string = old_value[0]  
                          line = line.replace(old_position_string, new_position_string)
                    
                       if 'position="' in line:
                          self.skipper = '2.1'
                          old_value = re.search('(position="(.+?),(.+?)")', str(line)).groups(1)
                          xposition = old_value[1]
                          yposition = old_value[2]
                       
                          if xposition != 'center':
                             xposition = self.get_new_value(old_value[1], 'x')
                          if yposition != 'center':
                             yposition = self.get_new_value(old_value[2], 'y')
                          
                          old_position_string = old_value[0] 
                          new_position_string = 'position="%s,%s"' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                    
                       if 'shadowOffset="' in line or ' offset="' in line:
                          self.skipper = '3'
                          old_value = re.search('(ffset="(.+?),(.+?)")', str(line)).groups(1)
                          xposition = old_value[1]
                          yposition = old_value[2]
                       
                          if xposition != 'center':
                             xposition = self.get_new_value(old_value[1], 'x')
                          if yposition != 'center':
                             yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'ffset="%s,%s"' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'size="' in line and not '<alias' in line:
                          self.skipper = '4'
                          old_value = re.search('(size="(.+?),(.+?)")', str(line)).groups(1)
                          xposition = old_value[1]
                          yposition = old_value[2]
                       
                          if xposition != 'center':
                             xposition = self.get_new_value(old_value[1], 'x')
                          if yposition != 'center':
                             yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'size="%s,%s"' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                       
                       if 'size="' in line and '<alias' in line:
                          self.skipper = '4.1'
                          old_value = re.search('(size="(.+?)")', str(line)).groups(1)
                          xposition = old_value[1]
                       
                          if xposition != 'center':
                             xposition = self.get_new_value(old_value[1], 'x')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'size="%s"' % (xposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                       
                       if 'height="' in line and '<alias' in line:
                          self.skipper = '4.2'
                          old_value = re.search('(height="(.+?)")', str(line)).groups(1)
                          yposition = old_value[1]
                       
                          if yposition != 'center':
                             yposition = self.get_new_value(old_value[1], 'x')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'height="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'font="' in line and not '<alias' in line:
                          self.skipper = '5'
                          old_value = re.search('(font="(.+?);(.+?)")', str(line)).groups(1)
                          xposition = old_value[1]
                          yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'font="%s;%s"' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'serviceNameFont="' in line:
                          self.skipper = '6'
                          old_value = re.search('(serviceNameFont="(.+?);(..)")', str(line)).groups(1)
                          xposition = old_value[1]
                          yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'serviceNameFont="%s;%s"' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
 
                       if 'setEventNameFont="' in line or ' EventNameFont="' in line:
                          self.skipper = '6.1'
                          old_value = re.search('(EventNameFont="(.+?);(..)")', str(line)).groups(1)
                          xposition = old_value[1]
                          yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'EventNameFont="%s;%s"' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                       
                       if 'setFont="' in line:
                          self.skipper = '6.2'
                          old_value = re.search('(setFont="(.+?);(..)")', str(line)).groups(1)
                          xposition = old_value[1]
                          yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'setFont="%s;%s"' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                       
                       if 'setServiceNameFont="' in line or ' ServiceNameFont' in line:
                          self.skipper = '6.3'
                          old_value = re.search('(ServiceNameFont="(.+?);(..)")', str(line)).groups(1)
                          xposition = old_value[1]
                          yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'ServiceNameFont="%s;%s"' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                       
                       if 'satPosLeft="' in line:
                          self.skipper = '6.4'
                          old_value = re.search('(satPosLeft="(.+?)")', str(line)).groups(1)
                          xposition = self.get_new_value(old_value[1], 'x')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'satPosLeft="%s"' % (xposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                       
                       if 'iconMargin="' in line:
                          self.skipper = '6.5'
                          old_value = re.search('(iconMargin="(.+?)")', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'iconMargin="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                       
                       if 'rowSplit="' in line:
                          self.skipper = '6.6'
                          old_value = re.search('(rowSplit="(.+?)")', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'rowSplit="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                       
                       if 'rowSplit1="' in line:
                          self.skipper = '6.7'
                          old_value = re.search('(rowSplit1="(.+?)")', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'rowSplit1="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                       
                       if 'rowSplit2="' in line:
                          self.skipper = '6.8'
                          old_value = re.search('(rowSplit2="(.+?)")', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'rowSplit2="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                       
                       if 'rowHeight="' in line:
                          self.skipper = '6.9'
                          old_value = re.search('(rowHeight="(.+?)")', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'rowHeight="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'serviceNumberFont="' in line:
                          self.skipper = '7'
                          old_value = re.search('(serviceNumberFont="(.+?);(..)")', str(line)).groups(1)
                          xposition = old_value[1]
                          yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'serviceNumberFont="%s;%s"' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'serviceInfoFont="' in line:
                          self.skipper = '8'
                          old_value = re.search('(serviceInfoFont="(.+?);(..)")', str(line)).groups(1)
                          xposition = old_value[1]
                          yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'serviceInfoFont="%s;%s"' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                    
                       if 'setItemHeight' in line:
                          self.skipper = '9'
                          old_value = re.search('(setItemHeight[(](.+?)[)])', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
                       
                          old_position_string = old_value[0] 
                          new_position_string = 'setItemHeight(%s)' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'itemHeight="' in line:
                          self.skipper = '10'
                          old_value = re.search('(itemHeight="(.+?)")', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'itemHeight="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'serviceItemHeight="' in line:
                          self.skipper = '11'
                          old_value = re.search('(serviceItemHeight="(.+?)")', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'serviceItemHeight="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'borderWidth="' in line:
                          self.skipper = '12'
                          old_value = re.search('(borderWidth="(.+?)")', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'borderWidth="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                         
                       if 'scrollbarWidth="' in line:
                          self.skipper = '13'
                          old_value = re.search('(scrollbarWidth="(.+?)")', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'scrollbarWidth="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'scrollbarSliderBorderWidth="' in line:
                          self.skipper = '14'
                          old_value = re.search('(scrollbarSliderBorderWidth="(.+?)")', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'scrollbarSliderBorderWidth="%s"' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                 
                       if 'itemHeight":' in line:
                          self.skipper = '15'
                          old_value = re.search('(itemHeight":(.*))', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
                     
                          old_position_string = old_value[0] 
                          new_position_string = 'itemHeight": %s' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                    
                       if 'default":' in line:
                          self.skipper = '16'    
                          old_value = re.search('(default": [(](.+?),)', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
                     
                          old_position_string = old_value[0] 
                          new_position_string = 'default": (%s,' % (yposition) 
                                                 
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'state":' in line:
                          self.skipper = '17'    
                          old_value = re.search('(state": [(](.+?),)', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
                     
                          old_position_string = old_value[0] 
                          new_position_string = 'state": (%s,' % (yposition) 
                                                 
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'notselected":' in line: 
                          self.skipper = '18'   
                          old_value = re.search('(notselected": [(](.+?),)', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
                     
                          old_position_string = old_value[0] 
                          new_position_string = 'notselected": (%s,' % (yposition) 
                                                 
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'category":' in line:
                          self.skipper = '19'    
                          old_value = re.search('(category": [(](.+?),)', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
                     
                          old_position_string = old_value[0] 
                          new_position_string = 'category": (%s,' % (yposition) 
                                                 
                          line = line.replace(old_position_string, new_position_string)
                             
                       if 'pos = (' in line or 'pos=(' in line:
                          self.skipper = '20'
                          if 'pos = (' in line:
                             old_value = re.search('(pos = [(](.+?),(.+?)[)])', str(line)).groups(1)
                          if 'pos=(' in line:
                             old_value = re.search('(pos=[(](.+?),(.+?)[)])', str(line)).groups(1)
                          
                          xposition = self.get_new_value(old_value[1], 'x')
                          yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'pos = (%s, %s)' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                    
                       if ', size = (' in line or ', size=(' in line or ',size = (' in line or ',size=(' in line:
                          self.skipper = '21'
                          if 'size = (' in line:
                             old_value = re.search('(size = [(](.+?),(.+?)[)])', str(line)).groups(1)
                          if 'size=(' in line:
                             old_value = re.search('(size=[(](.+?),(.+?)[)])', str(line)).groups(1)
                          
                          xposition = self.get_new_value(old_value[1], 'x')
                          yposition = self.get_new_value(old_value[2], 'y')
                       
                          old_position_string = old_value[0] 
                          new_position_string = 'size = (%s, %s)' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)          
                   
                       if 'gFont("' in line:
                          self.skipper = '22'
                          old_value = re.findall('(gFont[(]"(.+?)",(.+?)[)])', str(line))
                          for entrie in old_value:
                              xposition = entrie[1]
                              yposition = self.get_new_value(entrie[2], 'y')
        
                              old_position_string = entrie[0] 
                              new_position_string = 'gFont("%s", %s)' % (xposition, yposition) 
        
                              line = line.replace(old_position_string, new_position_string)
                              
                       if 'textsize[1]' in line or 'textsize[0]' in line:
                          self.skipper = '23'
                          try:
                            old_value = re.search('(textsize.* [+] (\d+)[,) ])', str(line)).groups(1)
                            value = old_value[1]
                            xposition = self.get_new_value(value, 'x')

                            old_position_string = '%s' % (value) 
                            new_position_string = '%s' % (xposition) 
        
                            line = line.replace(old_position_string, new_position_string)
                            
                          except:
                            line = line
                       
                       if 'offset = ' in line:
                          self.skipper = '24'
                          old_value = re.search('(offset = (.*))', str(line)).groups(1)
                          yposition = self.get_new_value(old_value[1], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'offset = %s' % (yposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if 'wsizex = ' in line:
                          self.skipper = '25'
                          old_value = re.search('(wsizex = (.*))', str(line)).groups(1)
                          value = old_value[1]
                       
                          if not 'text' in value:
                             xposition = self.get_new_value(value, 'x')
        
                             old_position_string = old_value[0] 
                             new_position_string = 'wsizex = %s' % (xposition) 
        
                             line = line.replace(old_position_string, new_position_string)
                             
                       if '&gt; wsizex):' in line:
                          self.skipper = '26'
                          old_value = re.search('(if [(](.+?) &gt; wsizex[)]:)', str(line)).groups(1)
                          xposition = self.get_new_value(old_value[1], 'x')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'if (%s &gt; wsizex):' % (xposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                          
                       if '(wsizex - ' in line:
                          self.skipper = '27'
                          old_value = re.search('([(]wsizex [-] (\d+),(\d+)[)])', str(line)).groups(1)
                          xposition = self.get_new_value(old_value[1], 'x')
                          yposition = self.get_new_value(old_value[2], 'y')
        
                          old_position_string = old_value[0] 
                          new_position_string = '(wsizex - %s, %s)' % (xposition, yposition) 
        
                          line = line.replace(old_position_string, new_position_string)  
                          
                       if '].instance.move(ePoint(' in line:
                          self.skipper = '28'
                          old_value = re.search('(ePoint[(](.+?),)', str(line)).groups(1)
                          xposition = self.get_new_value(old_value[1], 'x')
        
                          old_position_string = old_value[0] 
                          new_position_string = 'ePoint(%s,' % (xposition) 
        
                          line = line.replace(old_position_string, new_position_string)
                            
                       if '(wsizex,' in line: 
                          self.skipper = '29'
                          if not 'wsizey)' in line:
                             old_value = re.search('([(]wsizex.* (\d+)[)])', str(line)).groups(1)
                             yposition = self.get_new_value(old_value[1], 'y')
        
                             old_position_string = old_value[0] 
                             new_position_string = '(wsizex, %s)' % (yposition) 
        
                             line = line.replace(old_position_string, new_position_string)
                       
                       # Cool Stuff 
                       if ' Cool' in line:
                          old_value = re.findall('(Cool(.+?)="(.+?)")', str(line))
                          for entrie in old_value:
                              wrong = '0'
                              if '"' in str(entrie[1]):
                                 new_position_string = str(entrie[0])
                                 #self.debug('coolinfoguide: ' + str(entrie[1]))
                                 wrong = '1'
                              if ';' in str(entrie[2]) and wrong != '1':
                                 value = entrie[2].split(';')
                                 xposition = str(value[0])
                                 yposition = self.get_new_value(str(value[1]), 'y')
                                 new_position_string = 'Cool%s="%s;%s"' % (str(entrie[1]), xposition, yposition)
                              if ',' in str(entrie[2]) and wrong != '1':
                                 value = entrie[2].split(',')
                                 xposition = self.get_new_value(str(value[0]), 'x')
                                 yposition = self.get_new_value(str(value[1]), 'y')
                                 new_position_string = 'Cool%s="%s,%s"' % (str(entrie[1]), xposition, yposition)
                              if not ',' in str(entrie[2]) and not ';' in str(entrie[2]) and wrong != '1':
                                 try:
                                    yposition = self.get_new_value(str(entrie[2]), 'y')
                                    new_position_string = 'Cool%s="%s"' % (str(entrie[1]), yposition)
                                 except:
                                    new_position_string = str(entrie[0])
                                 
                              old_position_string = str(entrie[0])
                              line = line.replace(old_position_string, new_position_string)
                                
                       # Cool Stuff End                         
                       if self.skin_mode > 'hd':
                          if ' name="config" ' in line and not ' font="' in line:
                             self.skipper = '42'
                             try:
                               font_height = self.get_new_value('22', 'y')
                               old_position_string = ' name="config" '
                               new_position_string = ' name="config" font="Regular;%s" ' % str(font_height)
        
                               line = line.replace(old_position_string, new_position_string)
                            
                             except:
                               line = line
                          
                          if ' name="config" ' in line and not ' itemHeight="' in line:
                             self.skipper = '43'
                             try:
                               item_height = self.get_new_value('30', 'y')
                               old_position_string = ' name="config" '
                               new_position_string = ' name="config" itemHeight="%s" ' % str(item_height)
        
                               line = line.replace(old_position_string, new_position_string)
                            
                             except:
                               line = line
                            
                       wFile.write(line)
                       count += 1
                   except:
                       wFile.write('<!-- Skipper ' + str(self.skipper) + '--><!-- /* ERROR LINE -->' + line)   
                       self.debug('<!-- Skipper ' + str(self.skipper) + '--><!-- /* ERROR LINE -->' + line) 
                       count += 1
                
                wFile.close()
                self.debug('End Convertion <0=======')
                self.debug(str(count) + ' are Lines Changed')
                
        def get_new_value(self, value, factor):
                if factor == 'x':
                   value = str(int(round(float(value)* float(self.x_factor))))
                else:
                   value = str(int(round(float(value)* float(self.y_factor))))
                
                return value
        
        def debug(self, what):        
                   f = open('/tmp/kraven_debug.txt', 'a+')
                   f.write('[ChangeSkin]' + str(what) + '\n')
                   f.close()
