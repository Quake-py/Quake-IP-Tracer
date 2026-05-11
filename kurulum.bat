@echo off
title QUAKE IP Tracer kütüphane kurulumu
color 0c

echo.
echo 
echo     QUAKE IP TRACER - KUTUPHANE KURULUM EKRANI
echo
echo.
echo Lutfen bekleyin, gerekli kütüphaneler kontrol ediliyor ve kuruluyor...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python bilgisayarinizda yuklu degil veya PATH sistem degiskenine eklenmemis
    echo Lutfen python.org adresinden Python'u indirin ve kurarken "Add Python to PATH" secenegini isaretleyin.
    pause
    exit /b
)

echo [+] Python kurulumu dogrulandi.
echo.


echo [*] Pip guncelleniyor...
python -m pip install --upgrade pip >nul 2>&1


echo [*] 'requests' kutuphanesi kuruluyor...
pip install requests

echo.
echo [*] 'colorama' kutuphanesi kuruluyor...
pip install colorama

echo.
echo
echo [!] KURULUM TAMAMLANDI.
echo 
echo.
echo Artik araci sorunsuzca calistirabilirsiniz.
echo Calistirmak icin: python iptracer.py
echo.
pause
