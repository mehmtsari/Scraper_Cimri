#Kullanım Kılavuzu#

	1- cimriUrunler python dosyasının olduğu konumu komut istemcisi[cmd] üzerinde açın ve cimriUrunler.py dosyasını python ile çalıştırın.
Uygulama açıldığında 
	
Seçenekler;

1. Ürünler listesinden Veri çek ;  'https://www.cimri.com/sitemaps/product.xml' site map üzerindeki ürünler listesinden sırasıyla bitene kadar bütün ürünleri çeker.

2. En Alt kategorilerden Veri çek ; 'https://www.cimri.com/sitemaps/category.xml' içerisindeki kategori listeleri içerisinde gezinerek en alt kategorilerden sırasıyla bütün ürünleri çeker.

3. Txt dosyasının içerisindeki en alt kategorilerden Veri çek (bir txt dosyası içerisinde her satırda bir link olacak şekilde en alt kategoriler yerleştirilir ve yerleştirilen kategorilerde veri çekme işlemi yapılır)#Tavsiye edilen

4. Txt dosyasının içerisindeki kategorilerin en alt kategorilerini sapta ve verilerini çek (bir txt dosyası içerisinde her satırda bir link olacak kategoriler yapıştırılır sistem ilk olarak o kategorinin içerisindeki en alt kategorileri saptar. Sonrasında o en alt kategoriler üzerinde veri çekme işlemine başlar.)


Opsiyonel seçenek VPN:

Web site ağ trafiğini engellediği için program içerisinde ProtonVPN eklentisi bulunmaktadır. Bu seçenek için bilgisayarınızda proton vpn bulunmalıdır.
Bu link üzerinden indirilebilir, https://protonvpn.com/download
Eğer e seçeneği ile bu Opsiyonel seçeneği onaylarsanız. Web site ağ trafiği oluştuğunda, veya ip adresi engellendiğinde. 
Vpn açılır ve en hızlı sunucuya bağlanır. Bağlanılan sunucuda bir trafik olduğunda vpn kapatılır ve local ip üzerinden işlem devam eder. 
Bu işlem bu şekilde döngü halinde ilerler ve veri çekerken herhangi bir sorun veya hız kaybı yaşamamayı hedefler.
#Seçilmesi gerekmektedir hız kaybı yaşanmaması için.
