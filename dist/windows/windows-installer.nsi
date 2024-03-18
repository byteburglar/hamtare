OutFile "HamtareInstaller.exe"
VIProductVersion "0.1.0.0"
VIAddVersionKey FileVersion "0.1"
VIAddVersionKey CompanyName "ByteBurglar"
VIAddVersionKey ProductName "Hamtare"
VIAddVersionKey FileDescription "The best (and only) GUI to download videos, using yt-dlp and tkinter, in < 200 lines of Python."
VIAddVersionKey LegalCopyright "Copyleft (L) ByteBurglar"

Name "Hamtare"
BrandingText "Hamtare Installer"
InstallDir "$PROGRAMFILES\Hamtare"
InstallDirRegKey HKCU "Software\Hamtare" "Install_Dir"
RequestExecutionLevel admin

Page components
Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  File "Hamtare.exe"
  WriteRegStr HKCU "Software\Hamtare" "" $INSTDIR
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\Hamtare.exe"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"
  DeleteRegKey HKCU "Software\Hamtare"
SectionEnd

!define ICON_NAME "Hamtare"
!define ICON_PATH "$INSTDIR\Hamtare.exe"
!define ICON_TARGET "$DESKTOP\${ICON_NAME}.lnk"

Section "Create Desktop Icon"
    CreateShortCut "${ICON_TARGET}" "${ICON_PATH}"
SectionEnd

!define STARTMENU_FOLDER "Hamtare"
!define STARTMENU_SHORTCUT "$SMPROGRAMS\${STARTMENU_FOLDER}\Hamtare.lnk"

Section "Create Start Menu Shortcut"
    CreateDirectory "$SMPROGRAMS\${STARTMENU_FOLDER}"
    CreateShortCut "${STARTMENU_SHORTCUT}" "${ICON_PATH}"
SectionEnd
