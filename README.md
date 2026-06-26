# QUAKE IP Tracer 

Bu araç, Hedef IP'lerin coğrafi konumunu bulma, açık portları tarama, alan adı çözümlerini yapma ve internet yolu analizi (traceroute) gibi özellikler vardır. Öylesine yapılan bir tool.

## Özellikler
1. **IP Adresi Analizi:** Hedefin bulunduğu ülkeyi, şehri ve internet sağlayıcısını tespit eder.
2. **Alan Adı Analizi:** Herhangi bir web sitesinin arka plandaki gerçek sunucu IP'sini bulur.
3. **Açık Port Taraması:** Güvenlik duvarının izin verdiği yaygın iletişim portlarını test eder.
4. **Ağ Yolu Analizi:** Sizin cihazınızdan hedefe giden verinin internet üzerindeki santral (router) duraklarını listeler.
5. **Kendi Ağımı Kontrol Et:** Yerel bilgisayar adınızı ve ağ (LAN) içi IP'nizi veya Public IP adresinizi görüntüler.
6. **Sistem Testi:** Aracın ihtiyaç duyduğu dış API'lere erişimin açık olup olmadığını denetler.

## Gereksinimler
Projenin sorunsuz çalışabilmesi için sisteminizde **Python 3.x** kurulu olmalıdır. Ardından aşağıdaki harici kütüphanelerin yüklenmesi gerekmektedir:

- `requests`: İnternet üzerinden coğrafi veri ve API çekebilmek için.
- `colorama`: Aracın arayüzündeki profesyonel renkli çıktıların terminalinizde (CMD) düzgün görünebilmesi için.

## Kurulum ve Çalıştırma

Kütüphaneleri tek tek yüklemekle uğraşmamak için sizin için hazırladığım otomatik kurulum dosyasını kullanabilirsiniz:

1. Klasördeki `kurulum.bat` dosyasına çift tıklayın. Bu dosya, gerekli olan `requests` ve `colorama` kütüphanelerini bilgisayarınıza otomatik olarak kuracaktır.
2. Kurulum bittikten sonra projeyi çalıştırmak için CMD'den şu komutu girin:
   ```bash
   python iptracer.py
   ```

(Bu tool öylesine yapıldı. Herhangi bir şey kabul etmiyorum. Sadece eğlence amaçlı yapıldı.)
