
import csv
from enum import StrEnum
import logging
import sys

class Attribute(object):
    def __init__(self) -> None:
        self.name = ""
        self.visible = True
        self.global_attribute = True

class EnumAttributes(StrEnum):
    velocity = "Velocity expression"
    keyboard = "Keyboard"
    external_control = "External control"
    dates = "Dates"
    polyphony = "Polyphony" 
    synthesis_type = "Synthesis type"
    brand = "Brand"
    aftertouch = "Aftertouch"


class EnumFieldName(StrEnum):
     ID = "ID"
     name = "Name"
     description = "Descripton"
     price = "Regular price"
     categories = "Categories"
     tags = "Tags"
     images = "Images"
     
class Product(object):
 

    def __init__(self, id=0, name="", descrition="") -> None:
        self.ID = id
        self.name = name
        self.descrition = descrition
        self.price = ""
        self.categories = "Synthesizers > Roland"
        self.tags = ["Roland", "Synthesizers"]
        self.images = "https://luism.co/wp-content/uploads/2024/03/image_template.png"
        self.metadata = None

    def as_empty_description(self):
        return True if self.descrition == "" else False
    
    def copy_all_content(self, row: dict):
        self.metadata = row
    
    def fill_content(self):
        #search web with keyword
        pass


class ScraPy(object):

    def parse_csv(self):

        with open('wc-product-export-1.csv', newline='') as csvfile:
            my_dict_reader = csv.DictReader(csvfile)
            
            logging.info(f"Dialect {my_dict_reader.dialect} with {my_dict_reader.line_num} lines") 
            if isinstance(my_dict_reader, csv.DictReader):
                logging.info(f"Fields {my_dict_reader.fieldnames}")
            else:
                logging.warning("not possible to parse as dictionary")
            
            product_list = list()
            for row in my_dict_reader:
                if isinstance(row, dict):
                    # check if description is empty
                    p = Product()
                    # p = Product(id=row[EnumFieldName.ID], name = row[EnumFieldName.name], descrition = row[EnumFieldName.description]) 
                    if p.as_empty_description():
                        #fill all content
                        p.fill_content()
                    else:
                        p.copy_all_content(row) 
        
if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    my_p = ScraPy()
    my_p.parse_csv()