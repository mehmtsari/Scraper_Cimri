# -*- coding: utf-8 -*-
import requests 
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import time



from pywinauto.application import Application
from pywinauto import timings


class VPN:
    def __init__(self,path) -> None:
        try:
            self.app = Application(backend="uia").connect(path=path)
        except:
            self.app = Application(backend='uia').start(path)
            time.sleep(10)
        
        self.root = self.app.window(title="Proton VPN")
        timings.Timings.slow()
        self.quick_connect_button = self.root.child_window(title="Quick Connect", auto_id="SidebarQuickConnectButton", control_type="Button")
        self.quick_disconnect_button = self.root.child_window(title="Disconnect", auto_id="SidebarQuickConnectButton", control_type="Button")
        print('VPN KONTROLCÜSÜ BAŞLATILDI!')
    
    def connect(self):
        self.quick_connect_button.click()
    
    def disconnect(self):
        self.quick_disconnect_button.click()
        
        
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

#  [tagname,element_name],[tagname,[tagname,element_name]],[tagname,[[tagname,element_name],[tagname,[[tagname,element_name],[tagname,element_name]]]]]          
class saveXML:
    def __init__(self,justreading:bool,tree_name:str = None) -> None:
        self.mode = justreading
        
        if not self.mode:
            self.XMLTree = ET.Element(tree_name)
        print('XML KONTROLCÜSÜ BAŞLATILDI!')
        
    def read(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return BeautifulSoup(f.read(),'xml')
        
    def find_all(self,element_name):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return BeautifulSoup(f.read(),'xml').find_all(element_name)
    
    def create_element(self,element_name: str, elements: list = None, just_return = False):
        """
        Creates an XML element with the given element_name and adds its sub-elements (elements).
        If no sub-elements are specified, only the main element is created.

        :param element_name: The name of the XML element to create. Must be a string.
        :param elements: The sub-elements of the element. If desired, can be specified as a tuple in the form (sub_element_name, [sub_element_elements]).
        Each sub_element_elements list creates a new sub-element with the name sub_element_name that will be located under the sub-elements.
        The elements list is a list of these tuples and can be used to create multiple sub-elements at the same time.
        For example: [('element_1', 'element_name'), ('element_2', [('sub_element_1', []), ('sub_element_2',[(down_element_1,'element_name')])])]
        :param just_return: If set to True, the element is created but not stored, and only the created element is returned.
        By default, its value is False, which means the created element is stored and an element object is returned.
        :return: The created XML element.
        """
        if self.mode:
            raise Exception('just_reading mode Active')

        element = ET.Element(element_name)
        
        if elements:
            for item in elements:
                if isinstance(item[0], str) and isinstance(item[1],list):
                    sub_element_name = item[0]
                    sub_elements = item[1]
                    sub_element = self.create_element(sub_element_name, sub_elements,True)
                    element.append(sub_element)
                else:
                    tag_name = item[0]
                    tag_text = item[1]
                    ET.SubElement(element, tag_name).text = tag_text
                    
        if just_return:
            return element
        else:
            self.XMLTree.append(element)
            return element

    def saveXML(self,file_path):
        if self.mode:
            raise Exception('just_reading mode Active')
        with open(file_path, 'wb') as f:
            f.write(ET.tostring(self.XMLTree, encoding='utf-8', method='xml'))
                
            



class Scrapper:
    def __init__(self,vpn_choice) -> None:
        self.xml = saveXML(justreading=False,tree_name='itemlist')
        self.xmlname = None
        self.cont = 1
        self.VPN__ = vpn_choice
        #VPN SETTINGS
        if self.VPN__:
            self.vpn = VPN("C:\Program Files (x86)\Proton Technologies\ProtonVPN\ProtonVPN.exe")
            self.VPN_CONNECT = False
        
        self.max_try = 1
        
    def save_log(self,text):
        with open('log-dosyasi.txt','a',encoding='utf-8') as file:
            file.write(str(text))
            file.write('\n\n')
            
    def return_requests(self,url):
        while True:
            cont = requests.get(url)
            if cont.ok:
                return cont.content
            
        
        
    
    def get_sitemap(self,url):
        response = BeautifulSoup(self.return_requests(url),'xml').find_all('loc')
        return [elem.text for elem in response]
    
    def get_productsxml(self,url):
        response = BeautifulSoup(self.return_requests(url),'xml').find_all('url')
        return [elem.find('loc').text for elem in response]
    
    def save_productlist(self):
        products = self.get_sitemap('https://www.cimri.com/sitemaps/product.xml')
        saver = saveXML(justreading=False,tree_name='products_list')
        
        for product in products:
            saver.create_element(element_name='item',elements=[('url',product)])
        saver.saveXML('products_list.xml')
    
    def load_productlist(self):
        try:
            with open('products_list.xml', 'r', encoding='utf-8') as f:
                return [item.text for item in BeautifulSoup(f.read(),'xml').find_all('url')]
        except:
            print('PRODUCT LİSTESİ BULUNMAMAKTA OLUŞTURULACAKTIR.')
            self.save_productlist()
            return self.load_productlist()
    
    def check_internet_connection(self):
        try:
            requests.get('https://www.google.com')
            return True
        except:
            return False
    
    def return_data(self,url):
        wait_time = 7
        while True:
            if self.check_internet_connection():
                try:
                    content = requests.get(url)
                    soup = BeautifulSoup(content.text,'html.parser')
                    
                    if content.status_code == 410:
                        print(f'{url} Atlanıyor!!#####################')
                        return False
                    
                    if soup.find('html').attrs['lang'] != 'tr':
                        print('Site Bloklandı!')
                        print('Vpn Mode Değiştiriliyor...')
                        self.max_try = 7
                        raise Exception
                    
                    
                    if soup.text == '':
                        print('soup text boş')
                        print(soup)
                        raise Exception
                    
                    if soup == None:
                        print('soup Boş')
                        print(soup)
                        raise Exception
                    else:   
                        return soup
                except:                 
                    if self.max_try > 5:
                        if self.VPN__:
                            if self.VPN_CONNECT:
                                print('\n>Deneme Sınırı Aşıldı VPN Kapatılıyor..\n')
                                self.vpn.disconnect()
                                self.VPN_CONNECT = False
                            else:
                                print('\n>Deneme Sınırı Aşıldı VPN Açılıyor..\n')
                                self.vpn.connect()
                                self.VPN_CONNECT = True
                        self.max_try = 0
                        wait_time = 7
                        time.sleep(15)
    
                    else:
                        
                        print('\n>Tekrar deneniyor...{}(Kalan Deneme Hakkı: {})'.format(wait_time,5-self.max_try)) 
                        time.sleep(wait_time)
                        wait_time += 2
                        self.max_try += 1
            else:
                print('İnternet Bağlantısı Yavaş Veya Bulunmamakta.. Bekleniyor...')
                time.sleep(20)
    
    def get_product(self,url):
        print(f'{url} Başlıyor!')
        try:
            self.soup  = self.return_data(url)
            if not self.soup:
                return
            
            seo_keyword = str(url).replace('en-ucuz-','**').replace('-fiyatlari','**').split('**')[1]
            
            barcode = str(url).rsplit(',',maxsplit=1)[1]
                
            manufacturer = self.soup.find('a',{'class':'s1wytv2f-3 gxVdZH'}).text
            title = self.soup.find('h1',{'class':'s1wytv2f-2 jTAVuj'}).text  #self.soup.find('div',{'class':'s1a29zcm-1 cmgeOC'}).find('div',{'class':'s98wa6g-0 feTYBN'}).find('div',{'class':'s1a29zcm-6 cvvIFh'}).find('div',{'class':'s1a29zcm-7 dPVoLl'}).find('div',{'class':'s1wytv2f-0 bpjMIm'}).find('div',{'class':'s1wytv2f-2 jTAVuj'}).text
            try:
                description = self.soup.find('div',{'class':'s1vwbahk-0 kUraLN'}).text #self.soup.find('div',{'class':'s1a29zcm-1 cmgeOC'}).find('div',{'class':'s98wa6g-0 feTYBN'}).find('div',{'class':'s1a29zcm-6 cvvIFh'}).find('div',{'class':'s1a29zcm-7 dPVoLl'}).find('div',{'class':'s1vwbahk-0 kUraLN'}).text
            except:
                description = ""
            try:
                description +=  self.soup.find('div',{'class':'zo7519-1 fHwXAI'}).text
            except:
                description += ""
            
            image = self.soup.find('ul',{'class':'s1wxq1uo-1 hnSmng'}).find_all('img')   #self.soup.find('div',{'class':'s1a29zcm-1 cmgeOC'}).find('div',{'class':'s98wa6g-0 feTYBN'}).find('div',{'class':'s1a29zcm-6 cvvIFh'}).find('ul',{'class':'s1wxq1uo-1 hnSmng'}).find_all('img')
            images = []
            for img in image[:11]:
                cat_img = img['src']
                
                if not cat_img.endswith('.jpg'):
                    cat_img =  'http:' + img['data-src']
                if not cat_img.startswith('http:'):
                    cat_img = 'http:' + cat_img
                images.append(cat_img)
            main_image = images[0]
            images.pop(0)
            price = self.soup.find('span',{'class':'s1wl91l5-4 cBVHJG'}).text
            try:
                features = str(self.soup.find('div',{'class':'s10v53f3-0 dvgoOH'}))
            except:
                features = ''
            description += features
            
            
            categories = self.soup.find('ol',{'class':'s1hjsdw0-1 dgosJN','id':'breadcrumbList'}).find_all('li')
            categories.pop(0)
            categories.pop()
            
            cat_items = []
            for r in range(0,10):
                try:
                    category = categories[r].find('a').text
                    item  = ('category',category)
                    cat_items.append(item)
                except:
                    item = ('category',None)
                    cat_items.append(item)
            
                
            
            elements = [('product_id',barcode),
                        ('model',barcode),
                        ('sku',barcode),
                        ('upc',None),
                        ('ean',None),
                        ('jan',None),
                        ('isbn',None),
                        ('mpn',None),
                        ('location',url),
                        ('quantity',None),
                        ('stock_status_id',None),
                        ('image',main_image),
                        ('manufacturer_id',None),
                        ('shipping',None),
                        ('price',price),
                        ('points',None),
                        ('tax_class_id',None),
                        ('date_available',None),
                        ('weight',None),
                        ('weight_class_id',None),
                        ('lenght',None),
                        ('width',None),
                        ('height',None),
                        ('lenght_class_id',None),
                        ('subtrack',None),
                        ('minimum',None),
                        ('sort_order',None),
                        ('status',None),
                        ('viewed',None),
                        ('date_added',str(datetime.now())),
                        ('date_modified',None),
                        ('import_batch',None),
                        ('manufacturer',manufacturer),
                        ('price_special',None),
                        ('stock_status',None),
                        ('link',None),
                        ('stores',None),
                        ('seo_keyword_tr',seo_keyword),
                        ('name_tr',title),
                        ('description_tr',description),
                        ('tag_tr',None),
                        ('meta_title_tr',title),
                        ('meta_description_tr',description),
                        ('meta_keyword_tr',None),
                        ('reward_group_1',None),
                        ('reward_group_2',None)]
            
            for r in range(0,10):
                try:
                    element = ('image_{}'.format(r+1),images[r])
                except:
                    element = ('image_{}'.format(r+1),None)
                elements.append(element)

            elements +=  [('product_filter',None),
                            ('product_attribute',None),
                            ('product_category',cat_items),
                            ('product_discount',None),
                            ('product_special',None),
                            ('special_price_for_group_1',None),
                            ('special_price_for_group_1_start',None),
                            ('special_price_for_group_1_end',None),
                            ('special_price_for_group_2',None),
                            ('special_price_for_group_2_start',None),
                            ('special_price_for_group_2_end',None),
                            ('related_product_id',None),
                            ('related_product_name',None),
                            ('product_option',None),
                            ]
            
            
            
                
            
            self.xml.create_element(element_name='item',
                                    elements=elements
                                            )
            
            print(f'{self.cont}-{title} Eklendi!')
        except Exception as ex:
            print(f'{str(url)} Başarısız...')
            self.save_log(f'{str(url)} {ex}')
            return
        self.cont += 1


    def load_txt(self,filename):
        with open(filename,'r',encoding='utf-8') as file:
            return file.read().split('\n')
              
            
    def load_categories(self):
        main = self.get_sitemap('https://www.cimri.com/sitemaps/category.xml')
        categorys = []
        for catlist in main:
            cats = self.get_sitemap(catlist)
            categorys.extend(cats)
        return categorys 
    
    def get_products(self,url):
        self.page_url = url
        for i in range(1,51):
            print(f'Sayfa {i}')
            soup = self.return_data(self.page_url)
            products = soup.find('div',{'class':'s1cegxbo-0 envLfj'}).find('div',{'class':'s1a29zcm-6 cvvIFh'}).find('div',{'class':'s1cegxbo-1 cACjAF'}).find_all('div',{'id':'cimri-product'})
            for product in products:
                product_inf = product.find('a',{'class':'link-detail'})
                data_id = product_inf.attrs['data-id']
                data_href = 'https://www.cimri.com' + product_inf.attrs['href']
                data_title = product_inf.attrs['title']
                self.get_product(data_href)
            try:
                button = soup.find('div',{'class':'s1cegxbo-0 envLfj'}).find('div',{'class':'s1a29zcm-6 cvvIFh'}).find('a',{'class':'s1pk8cwy-4 eSWEIV','element':'a','aria-label':'Next Page'})
                self.page_url = 'https://www.cimri.com'+ button.attrs['href']
            except:
                print('#############Sayfa Sonu..')
                return
            
    def get_subcategories(self,url):
        soup = self.return_data(url)

        categories = soup.find('ul', {'class': 's1tg1k8o-9 gKwibs'}).find_all('li')
        subcategories = []
        
        for category in categories:
            try:
                category_link = category.find('a')
                category_title = category_link.attrs['title']
                category_href = 'https://www.cimri.com' + category_link.attrs['href']
            except:
                print(category_link,' Atlandı!')
                continue
            if not any(category_href == subcategory['href'] for subcategory in subcategories):
                subcategories.append({'title': category_title,'href': category_href})
                

        return subcategories
    
    def get_all_categories(self,url, category_list=None):
        if category_list is None:
            category_list = []
        try:
            categories = self.get_subcategories(url)
        except:
            category_list.append({'title':'Alt kategori','href':url})
            return category_list
            
        for category in categories:
            if not any(category['href'] == existing_category['href'] for existing_category in category_list):
                try:
                    self.get_all_categories(category['href'], category_list=category_list)
                except:
                    category_list.append(category)
                    print(f'{category} Bulundu!')
        return category_list
    
    
    def run_for_product_list(self):
        self.productlist = self.load_productlist()
        print('Product List Yüklendi')
        print(len(self.productlist))

        for product in self.productlist:
            self.xmlname = './products/'+product.replace('https://www.cimri.com/','').replace('-','_') + '.xml'
            print(product.strip())
            self.categories = self.get_productsxml(product.strip())
            print('Kategoriler Alındı.')
            for product in self.categories:
                self.get_product(product)
            self.xml.saveXML(self.xmlname)
                
    
    def run_for_category_list(self):
        self.categories = self.load_categories()
        for category in self.categories:
            self.xmlname = './products/'+category.replace('https://www.cimri.com/','').replace('-','_') + '.xml'
            print(f'{category} İçin Başlıyor...')
            self.get_products(category)
            self.xml.saveXML(self.xmlname)
        
    def run_for_txt_list(self,filename):
        self.categories = self.load_txt(filename)
        for category in self.categories:
            self.xmlname = './products/'+category.replace('https://www.cimri.com/','').replace('-','_') + '.xml'
            if category is None:
                continue
            if category.strip() == '':
                continue
            print(f'{category} İçin Başlıyor...')
            self.get_products(category)
            self.xml.saveXML(self.xmlname)
        
    def run_for_txt_maincategory_list(self,filename):
        self.categories = self.load_txt(filename)
        for category in self.categories:
            self.xmlname = './products/'+category.replace('https://www.cimri.com/','').replace('-','_') + '.xml'
            if category is None:
                continue
            if category.strip() == '':
                continue
            print(f'{category} için Alt kategoriler aranıyor..')
            subcategories = self.get_all_categories(category.strip())
            print('Alt Kategoriler bulundu. Veri çekme işlemi başlatılıyor..')
            for subcategory in subcategories:
                print(str(subcategory['title'])+' için Başlatılıyor..')
                self.get_products(subcategory['href'])
            self.xml.saveXML(self.xmlname)
                
            


if __name__ == '__main__':                
    def choice():
        while True:
            msg = int(input('   Lütfen Seçim Yapın: '))   
            if msg > 4 or msg < 1:
                print('Seçiminiz 1,2,3 veya 4 olmalı!')
            else:
                return msg
    
    def vpn_choice():
        while True:
            msg = str(input('   Proton VPN Kullanılsın mı?: '))   
            if msg.lower() == 'e':
                return True
            elif msg.lower() == 'h':
                return False
            else:
                continue
            



    

    text = """\n  Seçenekler
        1. Ürünler listesinden Veri çek
        2. En Alt kategorilerden Veri çek
        3. Txt dosyasının içerisindeki en alt kategorilerden Veri çek
        4. Txt dosyasının içerisindeki kategorilerin en alt kategorilerinden Veri çek\n"""
    print(text)

    msg = choice()
    vpn = vpn_choice()

    sc = Scrapper(vpn)
        
    try:    
        if msg == 1:
            sc.run_for_product_list()
        elif msg == 2:
            sc.run_for_category_list()
        elif msg == 3:
            filename = str(input('\n    Dosya Konumunu Girin: '))
            if not filename.endswith('.txt'):
                filename = filename.strip() + '.txt'
            sc.run_for_txt_list(filename)
        elif msg == 4:
            filename = str(input('\n    Dosya Konumunu Girin: '))
            if not filename.endswith('.txt'):
                filename = filename.strip() + '.txt'
            sc.run_for_txt_maincategory_list(filename)
        print('Bütün işlem Başarıyla tamamlandı!')
    except:
        sc.xml.saveXML(sc.xmlname)
        
        