from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        pass

    def load(self, path_to_exe):
        # dwCreationFlags defines how to create processes
        # --> If you want to see GUI of calc.exe, creation_flags = DEBUG_NEW_CONSOLE
        creation_flags = CREATE_NEW_CONSOLE

        # Instantiate a structure
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        # With the following two options, the launched process will be displayed as a separate window
        # This is also an example of how the settings in the STARTUPINFO structure affect the debugging target
        startupinfo.cb = sizeof(startupinfo)

        if kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print("[*] We have successfully launched the process!")
            print("[*] PID: {}".format(process_information.dwProcessId))
        else:
            print("[!] Error: {0:8}".format(hex(kernel32.GetLastError())))