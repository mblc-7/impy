[Setup]
AppName=ImPy on x64WAS (With ARM64 Setups)
AppVersion=26.1.9
VersionInfoVersion=26.1.9.0
AppPublisher=MBLC7
AppCopyright=Copyright (C) 2026 MBLC7
DefaultDirName={localappdata}\Programs\ImPy\client-x64was
DefaultGroupName=ImPy x64WAS
OutputDir=Output
OutputBaseFilename=ImPy-{#SetupSetting("AppVersion")}-x64was
Compression=lzma2
ShowLanguageDialog=yes
SolidCompression=yes
ChangesEnvironment=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
SetupIconFile=impy.ico
UninstallDisplayIcon={app}\impy.exe

[Languages]
Name: "en_US"; MessagesFile: "compiler:Default.isl"
Name: "zh_CN"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "zh_TW"; MessagesFile: "compiler:Languages\ChineseTraditional.isl"

[CustomMessages]
en_US.UninstallImPy=Uninstall ImPy
zh_CN.UninstallImPy=卸载 ImPy
zh_TW.UninstallImPy=解除安裝 ImPy

[Files]
Source: "impy-x64was.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{cm:UninstallImPy}"; Filename: "{uninstallexe}"
Name: "{group}\ImPy"; Filename: "{app}\impy-x64was.exe"
Name: "{group}\ImPy CPT"; \
    Filename: "{cmd}"; \
    Parameters: "/k ""{app}\cpt-x64was.bat"""; \
    WorkingDir: "{app}"; \
    IconFilename: "{app}\impy-x64was.exe"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"