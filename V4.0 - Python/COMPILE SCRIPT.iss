; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Formula UFSM Electronics"
#define MyAppVersion "3.3"
#define MyAppPublisher "Formula UFSM"
#define MyAppURL "https://github.com/Eugenio-Pozzobon/Formula-UFSM-Data-Analysis"
#define MyAppExeName "FormulaUFSM_Electronics.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{B57DED4A-C2B6-4E9B-A054-6733C1BC0176}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=E:\Git\formulaufsm_dataSoftware\LICENSE
InfoBeforeFile=E:\Git\formulaufsm_dataSoftware\INSTALL_GUIDE.MD
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
SetupIconFile=E:\Git\formulaufsm_dataSoftware\projectfolder\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\projectfolder\icon.ico
OutputBaseFilename=FUFSM_ini_setup
ExtraDiskSpaceRequired=604857600 

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "E:\Git\formulaufsm_dataSoftware\projectfolder\*"; DestDir: "{app}\projectfolder\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\src\*"; DestDir: "{app}\src\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\static\*"; DestDir: "{app}\static\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\FormulaUFSM_Electronics.py"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\get-pip.py"; DestDir: "{app}"; Flags: deleteafterinstall ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\LICENSE"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\python-3.9.2-amd64.exe"; DestDir: "{app}"; Flags: deleteafterinstall ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\README.MD"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\INSTALL_GUIDE.MD"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\setupbat.bat"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\launcher.bat"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\FUFSMElectronics_SETUP.exe"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Git\formulaufsm_dataSoftware\FormulaUFSM_Electronics.exe"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Run]
Filename: "{app}\setupbat.bat"

[Icons]
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[UninstallDelete]
Type: filesandordirs; Name: "{app}\_wcu_cacheFiles_"  
Type: filesandordirs; Name: "{app}\__pycache__"    
Type: filesandordirs; Name: "{app}\python39.dll"