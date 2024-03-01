
import csv
import logging


with open('wc-product-export-1.csv', newline='') as csvfile:
    my_dict_reader = csv.DictReader(csvfile)
    
    logging.info(f"Dialect {my_dict_reader.dialect} with {my_dict_reader.line_num} lines") 
    if isinstance(my_dict_reader, csv.DictReader):
         logging.info(f"Fields {my_dict_reader.fieldnames}")
    else:
        logging.warning("not possible to parse as dictionary")
    
    i = 0
    for row in my_dict_reader:
        if isinstance(row, dict):
            for k, v in row.items():
                if k== "Name":
                    logging.info(f" line {i} -> Name {v}")
        i+=i
        
 