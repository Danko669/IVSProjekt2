[Setup]
AppName=Kalkulačka IVS
AppVersion=1.0
AppPublisher=xbaloud00_xkralva00_xmaskal00
DefaultDirName={pf}\KalkulackaIVS
DefaultGroupName=Kalkulacka IVS
OutputDir=.\
OutputBaseFilename=calc_win_install
Compression=lzma
SolidCompression=yes
//UninstallDisplayIcon={app}\calc.exe
Uninstallable=yes


//SetupIconFile=..\src\ikona.ico

[Files]
Source: "..\dist\calc.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Kalkulacka"; Filename: "{app}\calc.exe"
Name: "{commondesktop}\Kalkulacka"; Filename: "{app}\calc.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Vytvořit zástupce na ploše"; GroupDescription: "Další ikony:"; Flags: unchecked