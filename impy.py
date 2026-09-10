cincl = ["Python 3.14.7", "Inno Setup 7.1.0", "LLVM 23.1.1", "GCC 16.1.0", "Firefox 155.0"]

from winreg import OpenKey, SetValueEx, CloseKey, QueryValueEx, REG_EXPAND_SZ, KEY_READ, KEY_WRITE, HKEY_CURRENT_USER
from locale import getdefaultlocale
from sys import exit, getwindowsversion, argv, stdout
from platform import machine
from json import dump, load, JSONDecodeError

stdout.reconfigure(line_buffering = True)
loc = getdefaultlocale()[0]
loc = "en_US" if loc not in ["en_US", "zh_CN", "zh_TW"] else loc

try:
    with open("locmap.json", "r", encoding = "utf-8") as lm:
        locmap = load(lm)

except (JSONDecodeError, UnicodeDecodeError):
    print("\033[0;31mDecoding failed: locmap.json\033[0m")
    exit(1)

except FileNotFoundError:
    print("\033[0;31mFile not found: locmap.json\033[0m")
    exit(1)

except PermissionError:
    print("\033[0;31mPermission error: locmap.json\033[0m")
    exit(1)

except:
    print("\033[0;31mUnknown error: locmap.json\033[0m")
    exit(1)

def trans(id: str) -> str:
    return locmap[id][loc]

def trgb(content, red, green, blue) -> str:
    return f"\033[38;2;{red};{green};{blue}m{content}\033[0m"

if machine().lower() not in ["amd64", "arm64"]:
    print(f"\033[0;33m{trans("unsarch")}{machine()}\033[0m")

v = getwindowsversion()
match (v.major, v.minor, v.build):
    case (5, 1, _):
        print(f"\033[0;33m{trans("unsupport")} Windows XP\033[0m")
    case (5, 2, _):
        print(f"\033[0;33m{trans("unsupport")} Windows XP\033[0m")
    case (6, 0, _):
        print(f"\033[0;33m{trans("unsupport")} Windows Vista\033[0m")
    case (6, 1, _):
        print(f"\033[0;33m{trans("unsupport")} Windows 7\033[0m")
    case (6, 2, _):
        print(f"\033[0;33m{trans("unsupport")} Windows 8\033[0m")
    case (6, 3, _):
        print(f"\033[0;33m{trans("unsupport")} Windows 8.1\033[0m")
    case (6, 4, _):
        print(f"\033[0;33m{trans("unsupport")} Windows 10\033[0m")
    case (10, 0, _):
        pass
    case _:
        print(f"\033[0;31m{trans("winverinvalid")}\033[0m")
        exit(1)

from winapi import (CreateProcessW, STARTUPINFOW, PROCESS_INFORMATION, L, et,
                      DWORD, WinError, WaitForSingleObject, INFINITY, GetExitCodeProcess,
                      CloseHandle, DeleteFileW)
from niquests import get, exceptions
from pathlib import Path

args = argv[1:]
localprograms = Path.home() / "AppData" / "Local" / "Programs"
homeurl = "https://mblc-7.github.io/impy"
homepath = localprograms / "ImPy"
homepath.mkdir(exist_ok = True)
setups = homepath / "pythons"
setups.mkdir(exist_ok = True)
impt = "26.1.4"

impyascii = f"""         {trgb("----:----==+", 0, 128, 128)}         
        {trgb("==  -----===++", 0, 128, 128)}        
        {trgb("====---====+++", 0, 128, 128)}        
               {trgb("===++++", 0, 128, 128)}        
 {trgb(" *****+++++===++++++*", 0, 128, 128)} {trgb("======", 255, 215, 0)} 
{trgb("*********++++++++++***", 0, 128, 128)} {trgb("=======", 255, 215, 0)}
{trgb("************++++******", 0, 128, 128)} {trgb("=======", 255, 215, 0)}
{trgb("*********", 0, 128, 128)}            {trgb("======+++", 255, 215, 0)}
{trgb("*******", 0, 128, 128)} {trgb("+=============++++++++", 255, 215, 0)}
{trgb("*******", 0, 128, 128)} {trgb("++++++++++++++++++++++", 255, 215, 0)}
 {trgb("******", 0, 128, 128)} {trgb("++++++++++++++++++++", 255, 215, 0)}  
        {trgb("+++++++", 255, 215, 0)}               
        {trgb("++++++++++++++", 255, 215, 0)}        
        {trgb("++++++++++  ++", 255, 215, 0)}        
         {trgb("++++++++++++", 255, 215, 0)}         
"""

header = {
    "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:155.0) Gecko/20100101 Firefox/155.0 ImPy/{impt}",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

def writemanage(
        version: str,
        pypath: str,
        arch: str = "x64",
        adds: bool = True,
        isdef: bool = False
    ):
    pypath = str(pypath)
    creator = {
        version: {
            "arch": arch,
            "path": pypath,
            "default": isdef
        }
    }
    whereisjson: Path = homepath / "manage.json"
    if whereisjson.exists():
        with open(whereisjson, "r", encoding = "utf-8") as f:
            orig: dict = load(f)

        if adds:
            orig |= creator
        else:
            orig.pop(version, None)
        with open(whereisjson, "w", encoding = "utf-8") as g:
            dump(orig, g, indent = 4)
    else:
        if adds:
            with open(whereisjson, "w", encoding = "utf-8") as f:
                dump(creator, f, indent = 4)
        else:
            with open(whereisjson, "w", encoding = "utf-8") as f:
                dump({}, f, indent = 4)

def getjson(jsonnm: str = "versions.json"):
    where = homepath / jsonnm
    wjson = f"{homeurl}/{jsonnm}"
    if where.exists():
        with open(where, "r", encoding = "utf-8") as f:
            old = load(f)
        
        try:
            d: dict = get(wjson).json()
            if d["meta"] > old["meta"]:
                print(f"{trans("collectin")}{jsonnm} ({d["meta"]})...")
                ret = download(wjson, where, None)

                if isinstance(ret, int):
                    print(f"{trans("uselocal")}{where} ({old["meta"]})")
        except (exceptions.ConnectionError, exceptions.Timeout):
            print(f"{trans("uselocal")}{where} ({old["meta"]})")
    else:
        d = get(wjson).json()
        print(f"{trans("collectin")}{where} ({d["meta"]})")
        
        ret = download(wjson, where, None)

        if isinstance(ret, int):
            if ret == 404:
                print(f"\033[0;31m{trans("noverfd")}\033[0m")
            elif ret == -1:
                print(f"\033[0;31m{trans("noie")}\033[0m")
            elif ret == -2:
                print(f"\033[0;31m{trans("timeout")}\033[0m")
            elif ret == -3:
                print(f"\033[0;31m{trans("unkerr")}\033[0m")
            else:
                print(f"\033[0;31m{trans("dlfail")} ({trans("stat")}{ret})\033[0m")
            exit(1)

    with open(where, "r", encoding = "utf-8") as f:
        old = load(f)
    return old

def download(
        url: str,
        filename: str | Path,
        params: dict = {},
        timeout: int | None = None,
    ) -> int | None:
    try:
        with get(url, params = params, headers = header, timeout = timeout, stream = True) as r:
            if r.ok:
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(5242880):
                        if chunk:
                            f.write(chunk)
                return None
            return r.status_code
    except exceptions.ConnectionError:
        return -1
    except exceptions.Timeout:
        return -2
    except Exception:
        return -3

def pysetup(
        filename: str,
        switch: str
    ) -> None:
    si = STARTUPINFOW()
    pi = PROCESS_INFORMATION()

    if not CreateProcessW(
        None,
        L(f"\"{filename}\"{switch}"),
        None,
        None,
        False,
        DWORD(0),
        None,
        None,
        et(si),
        et(pi)
    ):
        print(f"\033[0;31m{trans("procerr")}{WinError()}\033[0m")
        exit(1)

    try:
        WaitForSingleObject(pi.hProcess, INFINITY)
        exit_code: DWORD = DWORD()
        if not GetExitCodeProcess(
            pi.hProcess,
            et(exit_code)
        ):
            print(f"\033[0;31m{trans("exiterr")}{WinError()}\033[0m")
            exit(1)
        return exit_code.value

    finally:
        CloseHandle(pi.hProcess)
        CloseHandle(pi.hThread)

def install(
        url: str,
        filename: Path,
        switch: str = "",
        pyver: str = "3",
        pythonfolder: str = "Python3",
        params: dict = {},
        timeout: int | None = None,
        info: str | None = None,
        adds: bool = True,
        uninst: bool = False
    ) -> None:
    if filename.exists():
        print(f"{trans("pkgexist")}{filename}")
    else:
        print(f"{trans("collectin")}{filename if info is None else info}...")

        ret = download(url, filename, params, timeout)
        
        if isinstance(ret, int):
            if ret == 404:
                print(f"\033[0;31m{trans("noverfd")}\033[0m")
            elif ret == -1:
                print(f"\033[0;31m{trans("noie")}\033[0m")
            elif ret == -2:
                print(f"\033[0;31m{trans("timeout")}\033[0m")
            elif ret == -3:
                print(f"\033[0;31m{trans("unkerr")}\033[0m")
            else:
                print(f"\033[0;31m{trans("dlfail")} ({trans("stat")}{ret})\033[0m")
            exit(1)

    print(f"{trans("lainst")}...")
    exit_code = pysetup(filename, switch)

    match exit_code:
        case 0:
            if uninst:
                print(trans("uninstsuc"))
            else:
                print(trans("instsuc"))
            whereisver = localprograms / "Python" / pythonfolder
            writemanage(pyver, whereisver, "x64", adds, True)
            exit(0)
        case 1223 | 1602:
            print(f"\033[0;31m{trans("instcancel")}\033[0m")
            exit(1)
        case 1638:
            print(f"\033[0;31m{trans("anoinst")}\033[0m")
            exit(1)
        case _:
            print(f"\033[0;31m{trans("occur")} ({trans("exit")}{exit_code})\033[0m")
            exit(1)

def remove(
        filename: str,
        info: str | None = None
    ) -> None:
    print(f"{trans("removin")}{info if info is not None else filename}")
    if not DeleteFileW(L(filename)):
        print(f"\033[0;31m{trans("rminsterr")}\033[0m")
        exit(1)
    else:
        print(trans("rmsuc"))
        exit(0)

def build_args(argv: list) -> str:
    parts: list = []
    i = 2
    while i < len(argv):
        if argv[i] == "-c" and i + 1 < len(argv):
            parts.append("-c")
            parts.append(f'"{argv[i + 1]}"')
            i += 2
        else:
            parts.append(argv[i])
            i += 1
    return " ".join(parts)

def run_python(exe_template: str, freethread: bool = False, use_pythonw: bool = False) -> None:
    where = homepath / "versions.json"
    if not where.exists():
        old = getjson()
    else:
        with open(where, "r", encoding = "utf-8") as f:
            old = load(f)

    try:
        v = args[1]
        freethread = freethread if freethread else v.endswith("t")
        if use_pythonw:
            if freethread:
                print(f"\033[0;31m{trans("pywterr").format(v)}\033[0m")
                exit(1)
        exe_template = "python{v0}.{v1}t.exe" if freethread else exe_template
        v = v.removesuffix("t") if v.endswith("t") else v
    except IndexError:
        print(f"\033[0;31m{trans("invsyn")}\033[0m")
        exit(1)

    v = old["alias"][v] if v in old["alias"] else v

    if freethread:
        if v not in old["freethread"]:
            print(f"\033[0;31m{trans("threadnote")}\033[0m")
            exit(1)
        print(f"\033[0;33m{trans("ifaild")} \"impy inst {args[1].removesuffix("t")}t\" {trans("modit")}\033[0m")

    whereisjson: Path = homepath / "manage.json"
    if not whereisjson.exists():
        print(f"\033[0;31m{trans("instst")}\033[0m")
        exit(1)

    with open(whereisjson, "r", encoding = "utf-8") as f:
        pyaaa: dict = load(f)
    
    try:
        w = pyaaa[v]["path"]
    except KeyError:
        print(f"\033[0;31m{trans("ferr")}\033[0m")
        exit(1)

    v0, v1 = v.split(".")[0], v.split(".")[1]
    exe_name = exe_template.format(v0 = v0, v1 = v1)
    arg = build_args(args)

    si = STARTUPINFOW()
    pi = PROCESS_INFORMATION()

    if not CreateProcessW(
        None,
        L(f"\"{w}\\{exe_name}\" {arg}"),
        None,
        None,
        True,
        DWORD(0),
        None,
        None,
        et(si),
        et(pi)
    ):
        print(f"\033[0;31m{trans("procerr")}{WinError()}\033[0m")
        exit(1)

    try:
        WaitForSingleObject(pi.hProcess, INFINITY)
        exit_code: DWORD = DWORD()
        if not GetExitCodeProcess(
            pi.hProcess,
            et(exit_code)
        ):
            print(f"\033[0;31m{trans("exiterr")}{WinError()}\033[0m")
            exit(1)
        if exit_code.value != 0:
            print(f"\033[0;31m\"{" ".join(args)}\"{trans("nwork")} ({trans("exit")} {exit_code.value})\033[0m")
    finally:
        CloseHandle(pi.hProcess)
        CloseHandle(pi.hThread)

if __name__ == "__main__":
    if args == []:
        print(f"\033[0;31m{trans("cantempty")}\033[0m")
        exit(1)

    match args[0]:
        case "help":
            print(f"help\t{trans("showcmd")}")
            print(f"about\t{trans("impt")}")
            print(f"upd\t{trans("cupd")}")
            print(f"reld\t{trans("rjson")}")
            print(f"inst\t{trans("instpy")}")
            print(f"\thelp\t{trans("allpy")}")
            print(f"\t\t-s\t{trans("skipeol")}")
            print(f"\t(V)\t{trans("instpy")}")
            print(f"\t(V)t\t{trans("insthread")}")
            print(f"uninst\t{trans("uninstpy")}")
            print(f"list\t{trans("insted")}")
            print(f"setdef\t{trans("setdef")}")
            print(f"add\t{trans("addpy")}")
            print(f"del\t{trans("rminst")}")
            print(f"\t(V)\t{trans("rminst")}")
            print(f"py\t{trans("runpy")} ({trans("like")} \"impy py 3.14 main.py\")")
            print(f"\t(V)\t{trans("runpy")}")
            print(f"\t(V)t\t{trans("runpyt")}")
            print(f"pyw\t{trans("runpyw")} ({trans("like")} \"impy pyw 3.14 main.py\")")
            print(f"\t(V)\t{trans("runpyw")}")

        case "about":
            print(f"ImPy {impt}\n[ {", ".join(cincl)} ]\n{trans("copy")}\n{impyascii}")

        case "upd":
            old = getjson()
            match impt:
                case x if x == old["update"]["dev"]:
                    print(f"\033[1;36m‼ {trans("future")} ({trans("build")} {x})\033[0m")
                case x if x == old["update"]["new"]:
                    print(f"\033[0;32m√ {trans("uptodate")} ({trans("build")}{x})\033[0m")
                case x if impt in old["update"]["compate"]:
                    print(f"\033[0;33m! {trans("compate")} {old['update']['new']}{trans("excl")}\033[0m")
                case x if impt in old["update"]["expires"]:
                    print(f"\033[0;31m× {trans("iseol")} {old['update']['new']}{trans("excl")}\033[0m")
                case _:
                    print(f"\033[0;31m× {trans("oops")}\033[0m")

        case "inst":
            old = getjson()
            try:
                a = args[1]
            except IndexError:
                print(f"\033[0;31m{trans("invsyn")}\033[0m")
                exit(1)
            if a == "help":
                try:
                    if args[2] in ("--skip-eol", "-s"):
                        skip_eol = True
                    else:
                        skip_eol = False
                except IndexError:
                    skip_eol = False
                a: list = old["eol"] + old["security"] + old["active"]
                print(trans("insthelpbar"))
                for k, v in old["alias"].items():
                    if v in old["eol"] and skip_eol:
                        continue
                    if len(k) > 7:
                        print(f"{k[:6]}-\t{v}")
                        print(k[6:])
                    else:
                        print(f"{k}\t{v}")
                print(trans("ngap"))
                print(trans("instverbar"))

                s: int = 0
                for i in a:
                    match i:
                        case x if x in old["eol"]:
                            if skip_eol:
                                continue
                            cat = f"\033[0;31m× {trans("eolw")}\033[0m"
                            s += 1
                        case x if x in old["active"]:
                            if x in old["latest"]:
                                cat = f"\033[1;36m‼ {trans("latestw")}\033[0m"
                            else:
                                cat = f"\033[0;32m√ {trans("activew")}\033[0m"
                            s += 1
                        case x if x in old["security"]:
                            cat = f"\033[0;33m! {trans("securityw")}\033[0m"
                            s += 1
                        case _:
                            print(f"\033[0;31m{trans("ferr")}\033[0m")
                            exit(1)
                    print(f"{cat}\t{i}")
                print(trans("total").format(s))
                for c in old["credits"][loc]:
                    match loc:
                        case "zh_CN":
                            print(f"\n鸣谢 {c['name']} {c['info']}！")
                        case "zh_TW":
                            print(f"\n鳴謝 {c['name']} {c['info']}！")
                        case _:
                            print(f"\nThanks {c['name']} for {c['info']}!")
            else:
                try:
                    v = args[1]
                except IndexError:
                    print(f"\033[0;31m{trans("invsyn")}\033[0m")
                    exit(1)
                tswit = v.endswith("t")
                v = v.removesuffix("t") if v.endswith("t") else v
                syn = old["eol"] + old["security"] + old["active"]

                v = old["alias"][v] if v in old["alias"] else v
                if v not in syn:
                    print(f"\033[0;31m{trans("unkver")}\033[0m")
                    exit(1)
                shouldfn = setups / f"python-{v}-amd64.exe"
                try:
                    match args[2:]:
                        case x if tswit:
                            switch = " /passive Include_pip=1 Include_freethreaded=1"
                        case _:
                            switch = " /passive Include_pip=1"
                except IndexError:
                    switch = " /passive Include_pip=1"
                
                if v in old["eol"]:
                    spec = v + trans("brkeol")
                elif v in old["security"]:
                    spec = v + trans("brksec")
                else:
                    spec = v

                insturl = getjson("route.json")["python"][v]
                install(
                    insturl,
                    shouldfn,
                    switch,
                    v,
                    f"Python{v.split(".")[0]}{v.split(".")[1]}",
                    {},
                    None,
                    f"Python {spec}",
                    True,
                    False
                )

        case "uninst":
            old = getjson()
            try:
                v = args[1]
            except IndexError:
                print(f"\033[0;31m{trans("invsyn")}\033[0m")
                exit(1)
            tswit = v.endswith("t")
            v = v.removesuffix("t") if v.endswith("t") else v
            syn = old["eol"] + old["security"] + old["active"]

            v = old["alias"][v] if v in old["alias"] else v
            if v not in syn:
                print(f"\033[0;31m{trans("unkver")}\033[0m")
                exit(1)
            shouldfn = setups / f"python-{v}-amd64.exe"

            if v in old["eol"]:
                spec = v + trans("brkeol")
            elif v in old["security"]:
                spec = v + trans("brksec")
            else:
                spec = v

            insturl = getjson("route.json")["python"][v]
            install(
                insturl,
                shouldfn,
                " /uninstall",
                v,
                f"Python{v.split(".")[0]}{v.split(".")[1]}",
                {},
                None,
                f"Python {spec}",
                False,
                True
            )

        case "list":
            whereisjson: Path = homepath / "manage.json"
            if not whereisjson.exists():
                print(f"\033[0;31m{trans("instst")}\033[0m")
                exit(1)

            with open(whereisjson, "r", encoding = "utf-8") as f:
                c: dict = load(f)
            if c == {}:
                print(f"\033[0;31m{trans("ferr")}\033[0m")
                exit(1)
            print(trans("lsvap"))
            s = list(c.keys())
            s.sort()

            n = 0
                
            for i in s:
                try:
                    a = c[i]["arch"]
                except KeyError:
                    a = "?"

                try:
                    p = c[i]["path"]
                except KeyError:
                    p = "?"

                try:
                    d = f"\033[0;32m{trans("brkdef")}\033[0m" if c[i]["default"] else f"\033[0;31m{trans("brkndef")}\033[0m"
                except KeyError:
                    d = "?"

                isdef = c[i]["default"]
                
                if len(i) > 7:
                    print(f"{i[:6]}-\t{a}\t{d}\t{p}")
                    print(i[6:])
                else:
                    print(f"{i}\t{a}\t{d}\t{p}")

                n += 1

            print(trans("total").format(n))
            print(trans("ngap"))

        case "reld":
            try:
                getjson()
                print(trans("relsuc"))

            except Exception as e:
                print(f"\033[0;31m{trans("unkerr")} ({e})\033[0m")

        case "py":
            run_python("python.exe")

        case "pyw":
            run_python("pythonw.exe", use_pythonw = True)

        case "del":
            where = homepath / "versions.json"
            if not where.exists():
                old = getjson()
            else:
                with open(where, "r", encoding = "utf-8") as f:
                    old = load(f)
            try:
                v = args[1]
            except IndexError:
                print(f"\033[0;31m{trans("invsyn")}\033[0m")
                exit(1)

            v = old["alias"][v] if v in old["alias"] else v
            instr = setups / f"python-{v}-amd64.exe"
            if not instr.exists():
                print(trans("nothingrm"))
            else:
                if v in old["eol"]:
                    spec = v + trans("brkeol")
                elif v in old["security"]:
                    spec = v + trans("brksec")
                else:
                    spec = v
                remove(str(instr), trans("instofpy").format(spec))

        case "setdef":
            old = getjson()
            whereisjson: Path = homepath / "manage.json"
            if not whereisjson.exists():
                print(f"\033[0;31m{trans("instst")}\033[0m")
                exit(1)

            try:
                v = args[1]
            except IndexError:
                print(f"\033[0;31m{trans("invsyn")}\033[0m")
                exit(1)

            v = old["alias"][v] if v in old["alias"] else v

            with open(whereisjson, "r", encoding = "utf-8") as f:
                c: dict = load(f)
            if c == {} or v not in c.keys():
                print(f"\033[0;31m{trans("ferr")}\033[0m")
                exit(1)

            regk = OpenKey(
                HKEY_CURRENT_USER,
                r"Environment",
                0,
                KEY_READ | KEY_WRITE
            )

            try:
                cpath, dtype = QueryValueEx(regk, "Path")

            except FileNotFoundError:
                cpath = ""
                dtype = REG_EXPAND_SZ

            cpathls = cpath.split(";")
            if "" in cpathls:
                while cpathls.count("") != 0:
                    cpathls.remove("")
            ks = list(c.keys())
            ks.remove(v)
            for k in ks:
                pstr = c[k]["path"]
                pscripts = rf"{pstr}\Scripts"
                while pstr in cpathls or pscripts in cpathls:
                    if pstr in cpathls and pscripts in cpathls:
                        cpathls.remove(pstr)
                        cpathls.remove(pscripts)
                    elif pstr in cpathls:
                        cpathls.remove(pstr)
                    elif pscripts in cpathls:
                        cpathls.remove(pscripts)
                    else:
                        break
                writemanage(k, pstr, "x64")

            if c[v]["path"] in cpathls:
                if rf"{c[v]["path"]}\Scripts" in cpathls:
                    ...
                else:
                    cpathls = [rf"{c[v]["path"]}\Scripts"] + cpathls
            elif rf"{c[v]["path"]}\Scripts" in cpathls:
                ...
            else:
                cpathls = [c[v]["path"], rf"{c[v]["path"]}\Scripts"] + cpathls
            
            cpath = ";".join(i for i in cpathls)
            SetValueEx(regk, "Path", 0, REG_EXPAND_SZ, cpath)
            CloseKey(regk)

            writemanage(v, c[v]["path"], "x64", True, True)

            print(trans("setdefsuc").format(v))

        case "add":
            old = getjson()
            try:
                v = args[1]
                p = args[2]
            except IndexError:
                print(f"\033[0;31m{trans("invsyn")}\033[0m")
                exit(1)

            v = old["alias"][v] if v in old["alias"] else v
            python = Path(p) / "python.exe"
            pythonw = Path(p) / "pythonw.exe"

            if python.exists() and pythonw.exists():
                writemanage(v, p)
                print(trans("addpysuc"))
            else:
                print(f"\033[0;31m{trans("invpath")}\033[0m")
        
        case _:
            print(f"\033[0;31m{trans("invsyn")}\033[0m")
            exit(1)