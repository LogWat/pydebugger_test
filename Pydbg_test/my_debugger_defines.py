from ctypes import *

# Define and clarify the correspondence between MS types and ctypes
WORD    = c_ushort
DWORD   = c_ulong
LPBYPTE = POINTER(c_ubyte)
LPTSTR  = POINTER(c_char)
HANDLE  = c_void_p

# Constant
DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010

# structure for CreateProcessA()
class STARTUPINFO(Structure):
    _fields_ = [
        ("cb",              DWORD),
        ("lpReserved",      LPTSTR),
        ("lpDesktop",       LPTSTR),
        ("lpTitle",         LPTSTR),
        ("dwX",             DWORD),
        ("dwY",             DWORD),
        ("dwXSize",         DWORD),
        ("dwYSize",         DWORD),
        ("dwXCountChars",   DWORD),
        ("dwYCountChars",   DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags",         DWORD),
        ("wShowSindow",     WORD),
        ("cbReserved2",     WORD),
        ("lpReserved2",     LPBYPTE),
        ("hStdInput",       HANDLE),
        ("hStdOutput",      HANDLE),
        ("hStdError",       HANDLE),
        ]

class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess",    HANDLE),
        ("hThread",     HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId",  DWORD),]
