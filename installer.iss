#define MyAppName "Asha Nurse App"
#define MyAppVersion "1.1.1"
#define MyAppPublisher "Asha Nurse"
#define MyAppExeName "AshaNurseApp.exe"

[Setup]
AppId={{A7B4E8D2-6F1C-4B92-91C5-ASHANURSE2026}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

SetupIconFile=AshaNurseApp.ico

DefaultDirName={localappdata}\Programs\AshaNurseApp
DefaultGroupName={#MyAppName}

OutputDir=installer
OutputBaseFilename=AshaNurseApp_Setup_v1.1.1

Compression=lzma
SolidCompression=yes

PrivilegesRequired=lowest
Uninstallable=yes

[Files]

; Application files
Source: "dist\AshaNurseApp\*"; DestDir: "{app}"; \
Flags: recursesubdirs createallsubdirs ignoreversion; \
Excludes: "db.sqlite3,media\*"

; Database - install only if it does not already exist
Source: "dist\AshaNurseApp\db.sqlite3"; DestDir: "{app}"; \
Flags: ignoreversion onlyifdoesntexist uninsneveruninstall

; User uploaded files - never overwrite existing files
Source: "dist\AshaNurseApp\media\*"; DestDir: "{app}\media"; \
Flags: recursesubdirs createallsubdirs ignoreversion onlyifdoesntexist uninsneveruninstall

[Icons]

Name: "{autodesktop}\Asha Nurse App"; \
Filename: "{app}\AshaNurseApp.exe"

Name: "{group}\Asha Nurse App"; \
Filename: "{app}\AshaNurseApp.exe"

[Run]

Filename: "{app}\AshaNurseApp.exe"; \
Description: "Launch Asha Nurse App"; \
Flags: nowait postinstall skipifsilent