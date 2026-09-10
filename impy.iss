[Setup]
AppName=ImPy
AppVersion=26.1.4
VersionInfoVersion=26.1.4.0
AppPublisher=MBLC7
AppCopyright=Copyright (C) 2026 MBLC7
DefaultDirName={localappdata}\Programs\ImPy\Client
DefaultGroupName=ImPy
OutputDir=Output
OutputBaseFilename=ImPy-{#SetupSetting("AppVersion")}-x64
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
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "zh_CN"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "zh_TW"; MessagesFile: "compiler:Languages\ChineseTraditional.isl"

[CustomMessages]
en.FullInstallation=Full Installation
zh_CN.FullInstallation=完整安装
zh_TW.FullInstallation=完整安裝

en.CompactInstallation=Compact Installation
zh_CN.CompactInstallation=精简安装
zh_TW.CompactInstallation=精簡安裝

en.CustomInstallation=Custom Installation
zh_CN.CustomInstallation=自定义安装
zh_TW.CustomInstallation=自訂安裝

en.ImPymainsource=ImPy main source
zh_CN.ImPymainsource=ImPy 主程序
zh_TW.ImPymainsource=ImPy 主程式

en.ImPybuildsource=ImPy build source
zh_CN.ImPybuildsource=ImPy 构建源码
zh_TW.ImPybuildsource=ImPy 建置源碼

en.UninstallImPy=Uninstall ImPy
zh_CN.UninstallImPy=卸载 ImPy
zh_TW.UninstallImPy=解除安裝 ImPy

[Types]
Name: "full"; Description: "{cm:FullInstallation}"
Name: "compact"; Description: "{cm:CompactInstallation}"
Name: "custom"; Description: "{cm:CustomInstallation}"; Flags: iscustom

[Components]
Name: "main"; Description: "{cm:ImPymainsource}"; Types: full compact custom; Flags: fixed
Name: "build"; Description: "{cm:ImPybuildsource}"; Types: full custom

[Files]
Source: "impy.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "build\*"; Components: main
Source: "impy.build\*"; DestDir: "{app}\build"; Flags: ignoreversion recursesubdirs; Components: build

[Icons]
Name: "{group}\{cm:UninstallImPy}"; Filename: "{uninstallexe}"
Name: "{group}\ImPy"; Filename: "{app}\impy.exe"
Name: "{group}\ImPy CPT"; \
    Filename: "{cmd}"; \
    Parameters: "/k ""{app}\cpt.bat"""; \
    WorkingDir: "{app}"; \
    IconFilename: "{app}\impy.exe"

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; \
    Check: NeedsAddPath('{app}')

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKCU, 'Environment', 'Path', OrigPath) then
    Result := True
  else
    Result := Pos(Param, OrigPath) = 0;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  OrigPath: string;
  NewPath: string;
begin
  if CurUninstallStep = usPostUninstall then
    if RegQueryStringValue(HKCU, 'Environment', 'Path', OrigPath) then
    begin
      StringChangeEx(OrigPath, '{app};', '', True);
      StringChangeEx(OrigPath, '{app}', '', True);
      RegWriteStringValue(HKCU, 'Environment', 'Path', OrigPath);
    end;
end;

[UninstallDelete]
Type: filesandordirs; Name: "{app}"