import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

from pywinauto.application import Application
from pywinauto import timings
import threading

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

#  [tagname,element_name],[tagname,[tagname,element_name]],[tagname,[[tagname,element_name],[tagname,[[tagname,element_name],[tagname,element_name]]]]]          
class saveXML:
    def __init__(self,filePATH,justreading:bool,tree_name:str = None) -> None:
        self.mode = justreading
        self.file_path = filePATH
        if not self.mode:
            self.XMLTree = ET.Element(tree_name)
        
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

    def saveXML(self):
        if self.mode:
            raise Exception('just_reading mode Active')
        with open(self.file_path, 'wb') as f:
            f.write(ET.tostring(self.XMLTree, encoding='utf-8', method='xml'))
                


class VPN:
    def __init__(self) -> None:
        try:
            self.app = Application(backend="uia").connect(path="C:\Program Files (x86)\Proton Technologies\ProtonVPN\ProtonVPN.exe")
        except:
            self.app = Application(backend='uia').start("C:\Program Files (x86)\Proton Technologies\ProtonVPN\ProtonVPN.exe")
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

class Scraper:
    def __init__(self):
        self.xml = saveXML('AllCategories.xml',justreading=False,tree_name='itemlist')
        self.category_list = []
        
        #VPN SETTINGS
        self.vpn = VPN()
        self.VPN_CONNECT = False
        
        self.max_try = 1
        
    #def return_data(self,url):
    #    try:
    #        content = requests.get(url)
    #        soup = BeautifulSoup(content.text,'html.parser')
    #        if soup.text == '':
    #            raise Exception
    #        if soup == None:
    #            raise Exception
    #        else:   
    #            return soup
    #    except:
    #        print('Tekrar deneniyor...')    
    #        time.sleep(7)
    #        self.return_data(url)
    
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
                
                
            
    def get_category_info(self, url):
        soup = self.return_data(url)
        
        try:
            img = soup.find('div',{'id':'main_container'}).find('div',{'class':'s1a29zcm-1 cmgeOC'}).find('div',{'class':'s1cegxbo-0 envLfj'}).find('div',{'class':'s1a29zcm-6 cvvIFh'}).find('img')
            cat_img = img['src']
            if not cat_img.endswith('.jpg'):
                cat_img =  img['data-src']
            if not cat_img.startswith('https:'):
                cat_img = 'http:' + cat_img
        except:
            cat_img = None

        try:    
            description = str(soup.find('div',{'id':'main_container'}).find('div',{'class':'s1a29zcm-1 cmgeOC'}).find('div',{'class':'s1cegxbo-0 envLfj'}).find('div',{'class':'s1srlvfg-0 ivmJT'}).find('div',{'class':'s1srlvfg-1 epeeig'}))    
        except:
            description = None
        return {
            'image': cat_img,
            'description': description
        }

    def get_main_category(self,category):
        try:
            soup = self.return_data(category['href'])
            
            category_title = category['title']
            try:
                img = soup.find('div',{'id':'main_container'}).find('div',{'class':'s1a29zcm-1 cmgeOC'}).find('div',{'class':'s1cegxbo-0 envLfj'}).find('div',{'class':'s1a29zcm-6 cvvIFh'}).find('div',{'class':'s1cegxbo-1 cACjAF'}).find('img')
                cat_img = img['src']
                if not cat_img.endswith('.jpg'):
                    cat_img =  img['data-src']
                if not cat_img.startswith('http'):
                    cat_img = 'https:' + cat_img
            except:
                cat_img = None

            try:    
                description = str(soup.find('div',{'id':'main_container'}).find('div',{'class':'s1a29zcm-1 cmgeOC'}).find('div',{'class':'s1cegxbo-0 envLfj'}).find('div',{'class':'s1srlvfg-0 ivmJT'}).find('div',{'class':'s1srlvfg-1 epeeig'}))    
            except:
                description = None
            return {
                'title':category_title,
                'parents':[category_title,],
                'href':category['href'],
                'image': cat_img,
                'description': description
            }
        except Exception as ex:
            print(ex)
            print(soup)
        
    def get_subcategories(self,url,parents = None):
        soup = self.return_data(url)

        categories = soup.find('ul', {'class': 's1tg1k8o-9 gKwibs'}).find_all('li')
        subcategories = []
        for category in categories:
            category_parents = []
            category_parents += parents
            try:
                category_link = category.find('a')
                category_title = category_link.attrs['title']
                category_href = 'https://www.cimri.com' + category_link.attrs['href']
            except:
                print(category_link,' Atlandı!')
                continue
            if not any(category_href == subcategory['href'] for subcategory in subcategories):
                image,description = self.get_category_info(category_href).values()
                category_parents.append(category_title)
                subcategories.append({'title': category_title,'parents':category_parents, 'href': category_href, 'image': image, 'description': description})
                print(f'{category_title} Eklendi!')

        return subcategories



    


    def get_all_categories(self,url, category_list=None,parents=None):
        if category_list is None:
            category_list = []
        if parents is not None:
            categories = self.get_subcategories(url,parents=parents)
        else:
            categories = self.get_subcategories(url)
            
        for category in categories:
            if not any(category['href'] == existing_category['href'] for existing_category in category_list):
                category_list.append(category)
                try:
                    self.get_all_categories(category['href'], category_list=category_list,parents=category['parents'])
                except:
                    pass
        return category_list


    def start__(self,start_category):
        main = sc.get_main_category(start_category)
        print('################{} için Başlıyor...'.format(main['title']))
        return self.get_all_categories(start_category['href'],category_list=[main,],parents=main['parents'])

    def get_categoriesxml(self,url):
        soup = self.return_data(url)
        categories = soup.find('nav',{'class':'d97ymr-0 gvMjuX'}).find('ol',{'class':'d97ymr-1 fyhCRO'}).find_all('li')
        data = []
        for category in categories:
            category_link = category.find('a')
            category_title = category_link.attrs['title']
            category_href = 'https://www.cimri.com' + category_link.attrs['href']
            data.append({'title':category_title,
                         'href':category_href})
        return data
            
            
            
    
    def run(self,categoryxml_url):
        categorys = self.get_categoriesxml(categoryxml_url)
        categorys.pop()
        for category in categorys:
            category_data = self.start__(start_category=category)
            print('Kategori Toplamı : {}'.format(len(category_data)))
            for cat in category_data:
                elements = [('category_id',None),
                            ('image',cat['image']),
                            ('parent_id',None),
                            ('top',None),
                            ('column',None),
                            ('sort_order',None),
                            ('status',None),
                            ('date_added',str(datetime.now())),
                            ('date_modified',None),
                            ('code',None),
                            ('stores',None),
                            ('link',None),]
                parents = ''
                try:
                    cat['parents'].pop()
                except:
                    pass
                for cont,item in enumerate(cat['parents'],1):
                    parents += item
                    if not len(cat['parents']) == cont:
                        parents+= '>'
                    
                elements.append(('full_path_tr',parents))
                    
                elements.extend([
                                ('parent_name_tr',None),
                                ('filters_name_tr',None),
                                ('seo_keyword_tr',None),
                                ('name_tr',cat['title']),
                                ('description_tr',cat['description']),
                                ('meta_title_tr',None),
                                ('meta_description_tr',None),
                                ('meta_keyword_tr',None),
                                ('filters_ids',None)])
                
                
                self.xml.create_element(element_name='item',
                                            elements=elements,
                                            just_return=False)
        self.xml.saveXML()
        print('Veri Başarıyla Oluşturuldu!')

        
        

sc = Scraper()
data = sc.run('https://www.cimri.com/')