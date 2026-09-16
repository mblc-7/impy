import ctypes as __CTYPES

ptr = __CTYPES.POINTER
struct = __CTYPES.Structure
et = __CTYPES.byref
sizeof = __CTYPES.sizeof
WinError = __CTYPES.WinError
def L(value: str, size: int | None = None) -> __CTYPES.c_wchar_p:
    return __CTYPES.cast(
        __CTYPES.create_unicode_buffer(value, size),
        __CTYPES.c_wchar_p
    )

__KERNEL32 = __CTYPES.windll.kernel32
__SHLWAPI = __CTYPES.windll.shlwapi

INFINITY = 0xFFFFFFFF

INT = __CTYPES.c_int
WORD = __CTYPES.c_ushort
DWORD = __CTYPES.c_ulong
LPDWORD = ptr(DWORD)
LPWSTR = __CTYPES.c_wchar_p
LPCWSTR = __CTYPES.c_wchar_p
BOOL = __CTYPES.c_int
LPVOID = __CTYPES.c_void_p
BYTE = __CTYPES.c_byte
LPBYTE = ptr(BYTE)
HANDLE = __CTYPES.c_void_p
LONG = __CTYPES.c_long
LONG_PTR = __CTYPES.c_longlong
ULONG_PTR = __CTYPES.c_ulonglong

class _SECURITY_ATTRIBUTES(struct):
    _fields_ = [
        ("nLength", DWORD),
        ("lpSecurityDescriptor", LPVOID),
        ("bInheritHandle", BOOL)
    ]
SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES
LPSECURITY_ATTRIBUTES = ptr(SECURITY_ATTRIBUTES)

class _STARTUPINFOW(struct):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPWSTR),
        ("lpDesktop", LPWSTR),
        ("lpTitle", LPWSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", HANDLE)
    ]
STARTUPINFOW = _STARTUPINFOW
LPSTARTUPINFOW = ptr(STARTUPINFOW)

class _PROCESS_INFORMATION(struct):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD)
    ]
PROCESS_INFORMATION = _PROCESS_INFORMATION
LPPROCESS_INFORMATION = ptr(PROCESS_INFORMATION)

__KERNEL32.CreateProcessW.argtypes = [
    LPCWSTR,
    LPWSTR,
    LPSECURITY_ATTRIBUTES,
    LPSECURITY_ATTRIBUTES,
    BOOL,
    DWORD,
    LPVOID,
    LPCWSTR,
    LPSTARTUPINFOW,
    LPPROCESS_INFORMATION
]
__KERNEL32.CreateProcessW.restype = BOOL
def CreateProcessW(
        lpApplicationName: LPCWSTR,
        lpCommandLine: LPWSTR,
        lpProcessAttributes: LPSECURITY_ATTRIBUTES, # type: ignore
        lpThreadAttributes: LPSECURITY_ATTRIBUTES, # type: ignore
        bInheritHandles: BOOL,
        dwCreationFlags: DWORD,
        lpEnvironment: LPVOID,
        lpCurrentDirectory: LPCWSTR,
        lpStartupInfo: LPSTARTUPINFOW, # type: ignore
        lpProcessInformation: LPPROCESS_INFORMATION # type: ignore
) -> BOOL:
    return __KERNEL32.CreateProcessW(
        lpApplicationName,
        lpCommandLine,
        lpProcessAttributes,
        lpThreadAttributes,
        bInheritHandles,
        dwCreationFlags,
        lpEnvironment,
        lpCurrentDirectory,
        lpStartupInfo,
        lpProcessInformation
    )

__KERNEL32.WaitForSingleObject.argtypes = [
    HANDLE,
    DWORD
]
__KERNEL32.WaitForSingleObject.restype = DWORD
def WaitForSingleObject(
        hHandle: HANDLE,
        dwMilliseconds: DWORD
) -> DWORD:
    return __KERNEL32.WaitForSingleObject(
        hHandle,
        dwMilliseconds
    )

__KERNEL32.CreateDirectoryW.argtypes = [
    LPCWSTR,
    LPSECURITY_ATTRIBUTES
]
__KERNEL32.CreateDirectoryW.restype = BOOL
def CreateDirectoryW(
        lpPathName: LPCWSTR,
        lpSecurityAttributes: LPSECURITY_ATTRIBUTES # type: ignore
) -> BOOL:
    return __KERNEL32.CreateDirectoryW(
        lpPathName,
        lpSecurityAttributes
    )

__KERNEL32.DeleteFileW.argtypes = [
    LPCWSTR
]
__KERNEL32.DeleteFileW.restype = BOOL
def DeleteFileW(
        lpFileName: LPCWSTR
) -> BOOL:
    return __KERNEL32.DeleteFileW(
        lpFileName
    )

__KERNEL32.CloseHandle.argtypes = [
    HANDLE
]
__KERNEL32.CloseHandle.restype = BOOL
def CloseHandle(
        hObject: HANDLE
) -> BOOL:
    return __KERNEL32.CloseHandle(
        hObject
    )

__KERNEL32.GetExitCodeProcess.argtypes = [
    HANDLE,
    LPDWORD
]
__KERNEL32.GetExitCodeProcess.restype = BOOL
def GetExitCodeProcess(
        hProcess: HANDLE,
        lpExitCode: LPDWORD # type: ignore
) -> BOOL:
    return __KERNEL32.GetExitCodeProcess(
        hProcess,
        lpExitCode
    )

__SHLWAPI.PathFileExistsW.argtypes = [
    LPCWSTR
]
__SHLWAPI.PathFileExistsW.restype = BOOL
def PathFileExistsW(
        pszPath: LPCWSTR
) -> BOOL:
    return __SHLWAPI.PathFileExistsW(
        pszPath
    )