from __future__ import absolute_import
from Components.Converter.Converter import Converter
from os import statvfs
from Components.Element import cached, ElementError
from Components.Converter.Poll import Poll

class XionHDFDiskSpace(Poll, Converter, object):
    free = 0
    size = 1
    path = 2

    def __init__(self, type):
        _type = type
        Converter.__init__(self, _type)
        Poll.__init__(self)
        if _type == "free":
            self.type = self.free
        elif _type == "size":
            self.type = self.size
        elif _type == "path":
            self.type = self.path

        self.poll_interval = 2000
        self.poll_enabled = True


    @cached
    def getText(self):
        service = self.source.service
        if service:
            if self.type == self.free:
                try:
                    stat = statvfs(service.getPath().replace('Latest Recordings', '..'))
                    hdd = stat.f_bfree * stat.f_bsize
                    if hdd > 1099511627776:
                        free = float(hdd / 1099511627776.0)
                        return '%.2f TB' % free
                    elif hdd > 1073741824:
                        free = float(hdd / 1073741824.0)
                        return '%.2f GB' % free
                    elif hdd > 1048576:
                        free = float(hdd / 1048576.0)
                        return '%i MB' % free
                except OSError:
                    return 'N/A'

            elif self.type == self.size:
                try:
                    stat = statvfs(service.getPath().replace('Latest Recordings', '..'))
                    hddsize = stat.f_blocks * stat.f_bsize
                    if hddsize > 1099511627776:
                        locks = float(hddsize / 1099511627776.0)
                        return '(%.2f TB)' % locks
                    elif hddsize > 1073741824:
                        locks = float(hddsize / 1073741824.0)
                        return '(%.2f GB)' % locks
                    elif hddsize > 1048576:
                        locks = float(hddsize / 1048576.0)
                        return '(%i MB)' % locks
                except OSError:
                    return 'N/A'

            elif self.type == self.path:
                return service.getPath().replace('Latest Recordings', '..')

        return ""

    text = property(getText)

    def changed(self, what):
        if what[0] is self.CHANGED_SPECIFIC:
            Converter.changed(self, what)
        elif what[0] is self.CHANGED_POLL:
            self.downstream_elements.changed(what)
