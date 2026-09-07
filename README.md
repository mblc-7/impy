# ImPy

Make Python easy to manage

## Minimum Requirements

* Windows XP+ (recommend Windows 10+)
* x64 and ARM64

## Self Compile Guide

### Requirements

* Windows x64
* Python 3.10+
* Inno Setup 7
* Files in repository:
  * `impy.py`
  * `impy.iss`
  * `impy.ico`
  * `cpt.bat`
  * `locmap.json`


### Prepare

* make sure your current work directory which you put all the required files in repository.
  ```Batchfile
  cd %impyfolder%
  ```
  (change `%impyfolder%` to your actual directory)
* make sure you add these to `%PATH%`:
  * `%LocalAppData%\Programs\Python31X\Scripts` (change `Python31X` to your actual Python folder)
  * `C:\PROGRA~1\Inno Setup 7` (make sure you are using Inno Setup 7)
* install Nuitka
  ```Batchfile
  pip install nuitka
  ```

### Compile

Copy these down and paste to Command Prompt to run it:

```Batchfile
set version=26.1.2
```

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
    impy.py
```

### Make up a setup

Copy these down and paste to Command Prompt to run it:

```Batchfile
ISCC impy.iss
```

**NOTE:** if you want to test the setup, copy these down and paste to Command Prompt to run it:

```Batchfile
start .\Output\ImPy-%version%-x64.exe
```
