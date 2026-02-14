; =========================================================
; Image Converter – Installer (FIX DEFINITIVO)
; =========================================================

#define AppName "Image Converter"
#define AppVersion "1.0.0"
#define AppPublisher "Walter Pablo Tellez Ayala"
#define AppExeName "Image_Converter.exe"

#define DistDir "C:\Users\GAMT\Desktop\Proyecto Image_Converter\Image_Converter\dist\Image_Converter"
#define CertPFX "C:\Users\GAMT\Desktop\Proyecto Image_Converter\Image_Converter\Image_Converter_Dev.pfx"

[Setup]
AppId={{B9E8F5C2-3E6A-4C6F-AE77-IMAGECONVERTER}}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}

DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}

OutputDir=dist_installer
OutputBaseFilename=Image_Converter_Setup


Compression=lzma2
SolidCompression=yes

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

PrivilegesRequired=admin
WizardStyle=modern
DisableProgramGroupPage=yes

UninstallDisplayIcon={app}\{#AppExeName}
SetupIconFile=assets\images\icon.ico



[SignTools]
Name: ImageConverterSign; Command: "C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe" sign /fd SHA256 /f "{#CertPFX}" /p Condorito123*#*? /tr http://timestamp.digicert.com /td SHA256 "$f"

[Files]
Source: "{#DistDir}\Image_Converter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#DistDir}\_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{autodesktop}\Image Converter"; Filename: "{app}\Image_Converter.exe"
Name: "{group}\Image Converter"; Filename: "{app}\Image_Converter.exe"
Name: "{group}\Desinstalar Image Converter"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\Image_Converter.exe"; Description: "Ejecutar Image Converter"; Flags: nowait postinstall skipifsilent
