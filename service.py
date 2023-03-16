import atexit
import socket
import sys
import time

import win32serviceutil

import servicemanager
import win32event
import win32service

from main import work, pprint


class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = 'YummyRecommendsService'
    _svc_display_name_ = 'YummyAnime Recommends service'
    _svc_description_ = 'Update yummyanime recommendations'
    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        """
        Constructor of the winservice
        """
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.i = 0
        self.isrunning = False
    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        """
        Override to add logic before the start
        eg. running condition
        """
        self.isrunning = True
        atexit.register(lambda: pprint('Finished!'))

    def stop(self):
        """
        Override to add logic before the stop
        eg. invalidating running condition
        """
        pprint('Service had stopped!')
        self.isrunning = False
    def main(self):
        """
        Main class to be ovverridden to add logic
        """
        # find related items ( Your name )
        while self.isrunning:
            if self.i % 10000 == 0:
                work()
            self.i += 1
            time.sleep(5)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SMWinservice)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(SMWinservice)

# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
#     SMWinservice.parse_command_line()


