from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        self.h_process       = None
        self.pid             = None
        self.debugger_active = False



    def load(self, path_to_exe):
        # dwCreationFlags defines how to create processes
        # --> If you want to see GUI of calc.exe, creation_flags = CREATE_NEW_CONSOLE
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

            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            print("[!] Error: 0x{0:08x}".format((kernel32.GetLastError())))



    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process



    def attach(self, pid):
        self.h_process = self.open_process(pid)

        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid             = int(pid)
        else:
            print("[*] Unable to attach to the process.")
            print("[!] Error: 0x{0:08x}".format((kernel32.GetLastError())))



    def run(self):
        while self.debugger_active == True:
            debug_event     = DEBUG_EVENT()
            continue_status = DBG_CONTINUE 

            if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
                input("Press a key to continue...")
                self.debugger_active = False
                kernel32.ContinueDebugEvent(
                    debug_event.dwProcessId,
                    debug_event.dwThreadId,
                    continue_status)


    def detach(self):

        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] Finished debugging. Exiting...")
            return True
        else:
            print("There was an error")
            print("[!] Error: 0x{0:08x}".format((kernel32.GetLastError())))
            return False

    
    def open_thread(self, thread_id):

        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)

        if h_thread != 0:
            return h_thread
        else:
            print("[*] Could not obtain a valid thread handle.")
            print("[!] Error: 0x{0:08x}".format((kernel32.GetLastError())))


    def enumerate_threads(self):

        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)

        if snapshot != None:
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))

            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))
                
            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            print("[*] Failed to take a snapshot.")
            print("[!] Error: 0x{0:08x}".format((kernel32.GetLastError())))
            return False
        
    
    def get_thread_context(self, thread_id=None, h_thread=None):

        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        if h_thread == None:
            h_thread = self.open_thread(thread_id)
        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            print("[*] Failed to get thread context.")
            print("[!] Error: 0x{0:08x}".format((kernel32.GetLastError())))
            return False