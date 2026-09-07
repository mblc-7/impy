[Setup]
AppName=ImPy
AppVersion=26.1.2
VersionInfoVersion=26.1.2.0
AppPublisher=MBLC7
AppCopyright=Copyright (C) 2026 MBLC7
DefaultDirName={commonpf}\ImPy
DefaultGroupName=ImPy
OutputDir=Output
OutputBaseFilename=ImPy-{#SetupSetting("AppVersion")}-pure-x64
Compression=lzma2
ShowLanguageDialog=yes
SolidCompression=yes
ChangesEnvironment=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
SetupIconFile=impy.ico
UninstallDisplayIcon={app}\impy.exe

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "zh_CN"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "zh_TW"; MessagesFile: "compiler:Languages\ChineseTraditional.isl"

[CustomMessages]
en.UninstallImPy=Uninstall ImPy
zh_CN.UninstallImPy=卸载 ImPy
zh_TW.UninstallImPy=解除安裝 ImPy


[Files]
Source: "impy.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{cm:UninstallImPy}"; Filename: "{uninstallexe}"
Name: "{group}\ImPy"; Filename: "{app}\impy.exe"
Name: "{group}\ImPy CPT"; \
    Filename: "{cmd}"; \
    Parameters: "/k ""{app}\cpt.bat"""; \
    WorkingDir: "{app}"; \
    IconFilename: "{app}\impy.exe"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"