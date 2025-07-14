@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ====== Konfigurasi ======
set MAINFILE=main.py
set TEMP_VERSION=appver.tmp
set UPX_PATH=C:\Tools\upx-5.0.1-win64   REM <- Ganti sesuai lokasi UPX kamu

REM ====== Cek Python ======
echo [i] Mengecek keberadaan Python...
where python >nul 2>&1 || (
    echo [!] Python tidak ditemukan!
    pause
    exit /b
)

REM ====== Ambil APP_VERSION dari main.py ======
echo [i] Mengekstrak versi dari %MAINFILE%...
python "%~dp0get_version.py" > %TEMP_VERSION%
if not exist %TEMP_VERSION% (
    echo [!] Gagal mengambil versi dari get_version.py
    pause
    exit /b
)
set /p VERSION=<%TEMP_VERSION%
del %TEMP_VERSION%

REM ====== Nama Output EXE ======
set EXENAME=AutoPoster-v%VERSION%.exe

REM ====== Cek Nuitka ======
echo [i] Mengecek Nuitka...
python -m nuitka --version >nul 2>&1 || (
    echo [!] Nuitka belum terinstall. Jalankan: pip install nuitka
    pause
    exit /b
)

REM ====== Mulai Build ======
echo [🔧] Memulai build %MAINFILE% menjadi %EXENAME%...

python -m nuitka ^
  --onefile ^
  --standalone ^
  --show-progress ^
  --windows-icon-from-ico="%~dp0icon.ico" ^
  --output-filename=%EXENAME% ^
  %MAINFILE%

REM ====== Kompres dengan UPX (opsional) ======
if exist %EXENAME% (
    echo [📦] Mengompres %EXENAME% dengan UPX...
    "%UPX_PATH%\upx.exe" --best --lzma %EXENAME%
) else (
    echo [⚠️] File %EXENAME% tidak ditemukan. Gagal kompres.
    goto :end
)

:end
echo.
echo [✅] Build selesai! Output: %EXENAME%
pause
exit /b
