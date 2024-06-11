import csv
import logging
import sys
import wikipedia
from enum import Enum

from parrot import Parrot
from wikipedia import PageError, DisambiguationError


class Attribute(object):
    def __init__(self) -> None:
        self.name = ""
        self.visible = True
        self.global_attribute = True


class EnumAttributes(str, Enum):
    velocity = "Velocity expression"
    keyboard = "Keyboard"
    external_control = "External control"
    dates = "Dates"
    polyphony = "Polyphony"
    synthesis_type = "Synthesis type"
    brand = "Brand"
    aftertouch = "Aftertouch"


class EnumFieldName(str, Enum):
    ID = "ID"
    name = "Name"
    description = "Description"
    price = "Regular price"
    categories = "Categories"
    tags = "Tags"
    images = "Images"


class Product(object):

    def __init__(self, my_id=0, name="", description="") -> None:
        self.ID = my_id
        self.name = f'Roland {name}'
        self.description = description
        self.price = ""
        self.categories = "Synthesizers > Roland"
        self.tags = f'Roland, Synthesizers, {self.name}'
        self.images = "https://luism.co/wp-content/uploads/2024/03/5433939.png"
        self.metadata = None

    def as_empty_description(self):
        return True if self.description == "" else False

    def copy_all_content(self, row: dict):
        self.metadata = row

    def fill_content(self, my_parrot):
        # search web with keyword
        # self.description = wikipedia.summary(self.name)
        # ny = wikipedia.page("New York")
        # ny.title ny.summary
        try:
            self.description = wikipedia.page(self.name).summary
        except PageError as e:
            logging.error("no page found")
            return
        except DisambiguationError as e:
            logging.error("DisambiguationError")
            return
        # print(self.description)
        paraphrases = my_parrot.augment(input_phrase=self.description, max_return_phrases=2)
        if paraphrases is None:
            logging.error("no paraphrases")
            return
        if len(paraphrases) > 0:
            if len(paraphrases[0]) > 0:
                self.description = paraphrases[0][0]



class ScraPy(object):

    def __init__(self):
        self.parrot = Parrot()

    def parse_csv(self):
        with open('wc-product-export-1.csv', newline='', encoding='utf-8-sig') as csvfile:
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
                    p = Product(my_id=row[EnumFieldName.ID], name=row[EnumFieldName.name],
                                description=row[EnumFieldName.description])
                    if p.as_empty_description():
                        #fill all content
                        p.fill_content(self.parrot)
                        if not p.as_empty_description():
                            product_list.append(p)

            logging.info(f'we process {len(product_list)} items')
        return product_list

    def write_csv(self, file_name, product_list):
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = [EnumFieldName.ID.value, EnumFieldName.description.value, EnumFieldName.categories.value,
                          EnumFieldName.images.value, EnumFieldName.tags.value]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product in product_list:
                writer.writerow({EnumFieldName.ID.value: product.ID,
                                 EnumFieldName.description.value: product.description,
                                 EnumFieldName.categories.value: product.categories,
                                 EnumFieldName.images.value: product.images,
                                 EnumFieldName.tags.value: product.tags})


if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    my_p = ScraPy()
    my_list = my_p.parse_csv()
    my_p.write_csv('products.csv', my_list)