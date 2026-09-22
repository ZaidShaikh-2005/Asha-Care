#define MyAppName "ASHA Care"
#define MyAppVersion "1.1.1"
#define MyAppPublisher "ASHA Care"
#define MyAppExeName "AshaNurseApp.exe"

[Setup]
AppId={{A7B4E8D2-6F1C-4B92-91C5-ASHANURSE2026}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={localappdata}\Programs\AshaNurseApp
DefaultGroupName={#MyAppName}

SetupIconFile=AshaNurseApp.ico

OutputDir=installer
OutputBaseFilename=AshaNurseApp_Setup_v1.1.1

Compression=lzma2
SolidCompression=yes

PrivilegesRequired=lowest
Uninstallable=yes
WizardStyle=modern

[Files]

; ---------------------------------------------------------
; APPLICATION FILES
; ---------------------------------------------------------

Source: "dist\AshaNurseApp\*"; \
DestDir: "{app}"; \
Flags: recursesubdirs createallsubdirs ignoreversion; \
Excludes: "db.sqlite3,media\*"


; ---------------------------------------------------------
; DATABASE
; Install database only on first installation.
; Existing client database will NOT be overwritten on update.
; ---------------------------------------------------------

Source: "dist\AshaNurseApp\db.sqlite3"; \
DestDir: "{app}"; \
Flags: ignoreversion onlyifdoesntexist uninsneveruninstall


; ---------------------------------------------------------
; MEDIA
; Preserve user uploaded files.
; ---------------------------------------------------------

Source: "dist\AshaNurseApp\media\*"; \
DestDir: "{app}\media"; \
Flags: recursesubdirs createallsubdirs ignoreversion onlyifdoesntexist uninsneveruninstall


[Icons]

; Desktop shortcut
Name: "{autodesktop}\ASHA Care"; \
Filename: "{app}\AshaNurseApp.exe"; \
WorkingDir: "{app}"; \
IconFilename: "{app}\AshaNurseApp.exe"

; Start Menu shortcut
Name: "{group}\ASHA Care"; \
Filename: "{app}\AshaNurseApp.exe"; \
WorkingDir: "{app}"; \
IconFilename: "{app}\AshaNurseApp.exe"


[Run]

Filename: "{app}\AshaNurseApp.exe"; \
Description: "Launch ASHA Care"; \
WorkingDir: "{app}"; \
Flags: nowait postinstall skipifsilent