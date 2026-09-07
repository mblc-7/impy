# ImPy

Make Python easy to manage

## Minimum Requirements

* Windows XP+ (recommend Windows 10+)
* x64 and ARM64

## Self Compile Guide

### Requirements

* Windows x64
* Python 3.10+
* Inno Setup
* Files in repository:
  * `impy.py`
  * `impy.iss`
  * `impy.ico`
  * `cpt.bat`
  * `locmap.json`

### Steps

Firstly, make sure your current work directory which you put all the required files in repository.

```Batchfile
cd DirectoryHere
```

Secondly, make sure you had added `%LOCALAPPDATA%\Programs\Python31X\Scripts` in `%PATH%`.

If you haven't install Nuitka yet, write:

```Batchfile
pip install nuitka
```

Then copy these down:
First phrase:

```Batchfile
set version=26.1.2
```

Second phrase:

```Batchfile
nuitka --standalone ^
    --file-version=%version% ^
    --company-name=MBLC7 ^
    --product-name=ImPy ^
    --file-description="Make Python easy to manage"^
    --include-package=niquests ^
    --include-package=urllib3 ^
    --include-package=urllib3.contrib ^
    --include-package=urllib3.contrib.resolver ^
    --no-deployment-flag=self-execution ^
    --jobs=8 ^
    --msvc=14.5 ^
    --windows-icon-from-ico=impy.ico ^
    --include-data-files=cpt.bat=cpt.bat ^
    --include-data-files=locmap.json=locmap.json ^
    impy.py && ^
```
