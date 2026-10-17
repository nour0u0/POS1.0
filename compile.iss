[Setup]
AppName=OVA POS
AppVersion=1.0
DefaultDirName={autopf}\OVA POS
DefaultGroupName=OVA POS
OutputDir=Installer
OutputBaseFilename=OVA_POS_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=trolley.ico


[Files]
Source: "C:\Users\Nour\Desktop\caiss yousef\dist\OVA POS\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\OVA POS"; Filename: "{app}\OVA POS.exe"; IconFilename: "{app}\trolley.ico"
Name: "{commondesktop}\OVA POS"; Filename: "{app}\OVA POS.exe"; IconFilename: "{app}\trolley.ico"


[Files]
Source: "trolley.ico"; DestDir: "{app}"; Flags: ignoreversion


[Run]
Filename: "{app}\OVA_POS.exe"; Description: "Launch OVA POS"; Flags: nowait postinstall skipifsilent