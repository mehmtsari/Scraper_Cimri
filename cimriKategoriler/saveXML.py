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
                
            
        
"""
xml = saveXML('elements')

elements = [
    ('name'),
    ('age', '30'),
    ('address', [
        ('street', '123 Main St'),
        ('city', 'Anytown'),
        ('state', [
            ('shortname','TR'),
            ('name','Turkey')
        ])
    ])]
person_element = xml.create_element('person', elements)
print(ET.tostring(xml.XMLTree, encoding='unicode'))
"""