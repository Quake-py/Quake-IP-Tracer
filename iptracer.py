import os
import sys
import json
import time
import socket
import threading
import requests
import colorama
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

colorama.init(autoreset=True)

C_BEYAZ = "\033[38;2;255;255;255m"
C_GRI   = "\033[38;2;160;160;160m"
C_KIRMIZI_ACIK  = "\033[38;2;255;85;85m"
C_KIRMIZI_ORTA  = "\033[38;2;220;20;60m"
C_KIRMIZI_KOYU  = "\033[38;2;139;0;0m"
C_SARI   = "\033[38;2;255;215;0m"
C_MAVI   = "\033[38;2;0;255;255m"
C_YESIL  = "\033[38;2;50;205;50m"
SIFIRLA  = "\033[0m"

def logo_yazdir():
    logo_satirlari = [
        "  ██████                         █████              ",
        "  ███▒▒▒▒███                      ▒▒███               ",
        " ███    ▒▒███ █████ ████  ██████   ▒███ █████  ██████ ",
        "▒███     ▒███▒▒███ ▒███  ▒▒▒▒▒███  ▒███▒▒███  ███▒▒███",
        "▒███   ██▒███ ▒███ ▒███   ███████  ▒██████▒  ▒███████ ",
        "▒▒███ ▒▒████  ▒███ ▒███  ███▒▒███  ▒███▒▒███ ▒███▒▒▒  ",
        " ▒▒▒██████▒██ ▒▒████████▒▒████████ ████ █████▒▒██████ ",
        "   ▒▒▒▒▒▒ ▒▒   ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒ ▒▒▒▒ ▒▒▒▒▒  ▒▒▒▒▒▒  ",
        "  ─────────────────────────────────────────────────────",
        "                   [ BY QUAKE ]"
    ]
    
    r_bas, g_bas, b_bas = 255, 255, 255
    r_bitis, g_bitis, b_bitis = 139, 0, 0
    adim = len(logo_satirlari)
    
    for i, satir in enumerate(logo_satirlari):
        r = int(r_bas + (r_bitis - r_bas) * (i / max(1, adim - 1)))
        g = int(g_bas + (g_bitis - g_bas) * (i / max(1, adim - 1)))
        b = int(b_bas + (b_bitis - b_bas) * (i / max(1, adim - 1)))
        
        renk = f"\033[38;2;{r};{g};{b}m"
        print(f"{renk}{satir}{SIFIRLA}")
        time.sleep(0.04) 
    print() 


def ekrani_temizle():
    os.system('cls' if os.name == 'nt' else 'clear')

def durum_yazdir(durum, mesaj):
    semboller = {
        "BILGI": f"{C_MAVI}[i]", 
        "BASARILI": f"{C_YESIL}[+]", 
        "UYARI": f"{C_SARI}[!]", 
        "HATA": f"{C_KIRMIZI_ACIK}[X]", 
        "ISLEM": f"{C_KIRMIZI_ORTA}[*]"
    }
    print(f"{semboller.get(durum, '[?]')} {C_BEYAZ}{mesaj}{SIFIRLA}")

def yukleniyor_animasyonu(mesaj, sure=1.0):
    karakterler = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    bitis = time.time() + sure
    idx = 0
    while time.time() < bitis:
        sys.stdout.write(f"\r{C_KIRMIZI_ORTA}[{karakterler[idx % len(karakterler)]}] {C_GRI}{mesaj}...")
        sys.stdout.flush()
        time.sleep(0.08)
        idx += 1
    sys.stdout.write("\r" + " " * (len(mesaj) + 20) + "\r")

def rapor_kaydet(veri, dosya_adi):
    klasor = "raporlar"
    if not os.path.exists(klasor): 
        os.makedirs(klasor)
    
    yol = os.path.join(klasor, f"{dosya_adi}_{datetime.now().strftime('%H%M%S')}.json")
    try:
        with open(yol, 'w', encoding='utf-8') as f: 
            json.dump(veri, f, indent=4, ensure_ascii=False)
        durum_yazdir("BASARILI", f"Sonuçlar bilgisayarınıza kaydedildi: {yol}")
    except: 
        durum_yazdir("HATA", "Dosya kaydedilemedi.")

class AgAraclari:
    def __init__(self):
        self.oturum = requests.Session()

        self.portlar = {
            21: "Dosya Transferi (FTP)", 
            22: "Uzaktan Yönetim (SSH)", 
            80: "Web Sitesi (HTTP)", 
            443: "Güvenli Web (HTTPS)", 
            3389: "Uzak Masaüstü (RDP)"
        }

    def ip_analizi(self, ip_adresi):
        print(f"\n{C_BEYAZ}--- IP Adresi Analizi ---")
        durum_yazdir("BILGI", "Bu işlem, hedefin dünya üzerindeki fiziksel yerini ve internet sağlayıcısını bulur.")
        yukleniyor_animasyonu("Adım 1: Veritabanlarına bağlanılıyor")
        
        try:
            cevap = self.oturum.get(f"http://ip-api.com/json/{ip_adresi}", timeout=8).json()
            if cevap.get('status') == 'fail': 
                durum_yazdir("HATA", "Geçersiz veya bulunamayan IP adresi.")
                return None
            
            yukleniyor_animasyonu("Adım 2: Veriler çözümleniyor")
            durum_yazdir("BASARILI", "Analiz tamamlandı. Sonuçlar:")
            print(f"  {C_GRI}Ülke        : {C_BEYAZ}{cevap.get('country')}")
            print(f"  {C_GRI}Şehir       : {C_BEYAZ}{cevap.get('city')}")
            print(f"  {C_GRI}İnternet Sğ.: {C_BEYAZ}{cevap.get('isp')}")
            return cevap
        except: 
            durum_yazdir("HATA", "Bağlantı hatası yaşandı. Lütfen internetinizi kontrol edin.")
            return None

    def port_tarama(self, ip_adresi):
        print(f"\n{C_BEYAZ}--- Açık Port (Kapı) Taraması ---")
        durum_yazdir("BILGI", "Bu işlem, hedef sistemde dışarıya açık olan servisleri (örn. web sitesi) tespit eder.")
        durum_yazdir("ISLEM", f"{ip_adresi} üzerindeki kapılar kontrol ediliyor...")
        
        bulunanlar = []
        def tarayici_görev(port_no):
            try:
                soket = socket.socket()
                soket.settimeout(2.0)
                
                if soket.connect_ex((ip_adresi, port_no)) == 0:
                    gorev = self.portlar.get(port_no, 'Bilinmeyen Servis')
                    durum_yazdir("BASARILI", f"Açık Port Bulundu: {port_no} -> {gorev}")
                    bulunanlar.append(port_no)
                soket.close()
            except: pass
            
        with ThreadPoolExecutor(max_workers=10) as havuz: 
            havuz.map(tarayici_görev, self.portlar.keys())
            
        if not bulunanlar:
            durum_yazdir("BILGI", "Test edilen yaygın portların tamamı kapalı ve güvenli görünüyor.")

    def alan_adi_analizi(self, alan_adi):
        print(f"\n{C_BEYAZ}--- Alan Adı (Web Sitesi) Analizi ---")
        durum_yazdir("BILGI", "Bu işlem, web sitesinin arka planındaki gerçek IP adresini bulur.")
        yukleniyor_animasyonu("Adım 1: DNS sunucularına soruluyor")
        
        try:
            gercek_ip = socket.gethostbyname(alan_adi)
            durum_yazdir("BASARILI", f"Web sitesinin gerçek IP adresi bulundu: {gercek_ip}")
        except: 
            durum_yazdir("HATA", "Alan adı çözümlenemedi. Adresi doğru yazdığınızdan emin olun.")

    def ag_yolu_trace(self, hedef):
        print(f"\n{C_BEYAZ}--- Ağ Yolu Analizi (TraceRoute) ---")
        durum_yazdir("BILGI", "Bu işlem, sizin bilgisayarınızdan hedefe gidene kadar verinin hangi santrallerden geçtiğini tek tek gösterir.")
        durum_yazdir("ISLEM", "Yol haritası çıkarılıyor, bu işlem hedefin uzaklığına göre 10-15 saniye sürebilir...")
        
        komut = ["tracert" if os.name == 'nt' else "traceroute", hedef]
        try:
            islem = subprocess.Popen(komut, stdout=subprocess.PIPE, text=True)
            for sira, satir in enumerate(islem.stdout):
                if satir.strip(): 
                    print(f"  {C_GRI}{satir.strip()}")
                
                if sira > 8: 
                    break
            islem.kill()
            durum_yazdir("BASARILI", "Yol haritası analizi tamamlandı.")
        except: 
            durum_yazdir("HATA", "Ağ yolu haritası çıkarılamadı.")

    def baglanti_testi(self):
        print(f"\n{C_BEYAZ}--- Bağlantı Testi ---")
        durum_yazdir("BILGI", "Bu aracın bilgi aldığı dış sunucuların çalışıp çalışmadığını kontrol eder.")
        yukleniyor_animasyonu("Sunucular test ediliyor")
        
        try:
            cevap = self.oturum.get("http://ip-api.com/json/", timeout=5)
            if cevap.status_code == 200:
                durum_yazdir("BASARILI", "Tüm dış sunucular aktif ve araca yanıt veriyor.")
            else:
                durum_yazdir("UYARI", "Dış sunuculara ulaşılamıyor, internetiniz kısıtlı olabilir.")
        except: 
            durum_yazdir("HATA", "İnternet bağlantınız yok veya engelleniyor.")

    def kendi_agimi_kontrol_et(self):
        print(f"\n{C_BEYAZ}--- Yerel Ağ Kontrolü ---")
        durum_yazdir("BILGI", "Bilgisayarınızın mevcut ağdaki temel kimlik bilgilerini gösterir.")
        
        try:
            bilgisayar_adi = socket.gethostname()
            yerel_ip = socket.gethostbyname(bilgisayar_adi)
            
            
            try:
                dis_ip = self.oturum.get("https://api.ipify.org", timeout=5).text
            except:
                dis_ip = "Bulunamadı"
                
            durum_yazdir("BASARILI", "Yerel ağ bilgileri alındı:")
            print(f"  {C_GRI}Bilgisayar Adı  : {C_BEYAZ}{bilgisayar_adi}")
            print(f"  {C_GRI}Modem İçi IP    : {C_MAVI}{yerel_ip}")
            print(f"  {C_GRI}Dış (Public) IP : {C_KIRMIZI_ACIK}{dis_ip}")
        except: 
            durum_yazdir("HATA", "Ağ bilgileri okunamadı.")

def ana_menu():
    ekrani_temizle()
    logo_yazdir()

    
    araclar = AgAraclari()
    while True:
        print(f"\n{C_KIRMIZI_ORTA}=== YAPMAK İSTEDİĞİNİZ İŞLEMİ SEÇİN ===")
        print(f"  {C_KIRMIZI_ORTA}[1] {C_BEYAZ}IP Adresi Analizi")
        print(f"  {C_KIRMIZI_ORTA}[2] {C_BEYAZ}Alan Adı (Web Sitesi) Analizi")
        print(f"  {C_KIRMIZI_ORTA}[3] {C_BEYAZ}Açık Port (Kapı) Taraması")
        print(f"  {C_KIRMIZI_ORTA}[4] {C_BEYAZ}Ağ Yolu Analizi (Harita)")
        print(f"  {C_KIRMIZI_ORTA}[5] {C_BEYAZ}Kendi Ağımı Kontrol Et")
        print(f"  {C_KIRMIZI_ORTA}[6] {C_BEYAZ}Bağlantı ve Sistem Testi")
        print(f"  {C_KIRMIZI_ORTA}[Q] {C_BEYAZ}Programı Kapat")
        
        secim = input(f"\n{C_KIRMIZI_ORTA} Seçiminiz >> {C_BEYAZ}").strip().upper()
        
        if secim == '1':
            hedef = input(f"  {C_GRI}Lütfen hedef IP adresini yazın: {C_BEYAZ}")
            veri = araclar.ip_analizi(hedef)
            if veri:
                kayit = input(f"\n  {C_GRI}Bu sonucu bilgisayarınıza kaydetmek ister misiniz? (E/H): {C_BEYAZ}").strip().upper()
                if kayit == 'E':
                    rapor_kaydet(veri, f"ip_{hedef}")
            input(f"\n{C_GRI}Menüye dönmek için Enter'a basın...")
            ekrani_temizle()
            logo_yazdir()

            
        elif secim == '2': 
            hedef = input(f"  {C_GRI}Lütfen web sitesi adresini yazın (örn: google.com): {C_BEYAZ}")
            araclar.alan_adi_analizi(hedef)
            input(f"\n{C_GRI}Menüye dönmek için Enter'a basın...")
            ekrani_temizle()
            logo_yazdir()

            
        elif secim == '3': 
            hedef = input(f"  {C_GRI}Lütfen taramak istediğiniz IP adresini yazın: {C_BEYAZ}")
            araclar.port_tarama(hedef)
            input(f"\n{C_GRI}Menüye dönmek için Enter'a basın...")
            ekrani_temizle()
            logo_yazdir()

            
        elif secim == '4': 
            hedef = input(f"  {C_GRI}Ağ yolunu çizmek istediğiniz IP adresini yazın: {C_BEYAZ}")
            araclar.ag_yolu_trace(hedef)
            input(f"\n{C_GRI}Menüye dönmek için Enter'a basın...")
            ekrani_temizle()
            logo_yazdir()

            
        elif secim == '5': 
            araclar.kendi_agimi_kontrol_et()
            input(f"\n{C_GRI}Menüye dönmek için Enter'a basın...")
            ekrani_temizle()
            logo_yazdir()

            
        elif secim == '6': 
            araclar.baglanti_testi()
            input(f"\n{C_GRI}Menüye dönmek için Enter'a basın...")
            ekrani_temizle()
            logo_yazdir()

            
        elif secim == 'Q': 
            print(f"\n{C_KIRMIZI_ORTA}[!] Program kapatılıyor. Güvenli günler dileriz.{SIFIRLA}")
            break

if __name__ == "__main__":
    try: 
        ana_menu()
    except KeyboardInterrupt: 
        print(f"\n{C_KIRMIZI_ORTA}[!] Zorla kapatıldı.{SIFIRLA}")
        sys.exit()
