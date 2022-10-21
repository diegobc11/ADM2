import argparse
import sys
import os
import numpy as np
import csv
import pickle

parser = argparse.ArgumentParser(description='The main program has four mandatory arguments.')
parser.add_argument("encodeDecode", help="en for encoding mode, de to decoding mode.", type=str)
parser.add_argument("compression", help="Compression technique used:\n-bin\n-rle\n-dic\n-for\n-dif", type=str)
parser.add_argument("dataType", help="Data type used:\n-int8\n-int16\n-int32\n-int64\n-string", type=str)
parser.add_argument("filePath", help="Entire path of the file to work with.",type=str)
args = parser.parse_args()

print(args)
# print(args.encodeDecode, args.compression, args.dataType, args.filePath)
if args.encodeDecode not in ["en", "de"]:
    raise NameError(f'The options available for the -ed argument are "en" for encode and "de" for decode, but got {args.encodeDecode} instead.')
else:
    ed = 'en' if args.encodeDecode == 'en' else 'de'

if args.compression not in ["bin", "rle", "dic", "for", "dif"]:
    raise NameError(f'The options available for the -cp argument are "bin", "rle", "dic", "for" and "dif",  but got {args.compression} instead.')
else: 
    if args.compression =='bin': 
        cp = 'bin'
    elif args.compression =='rle':
        cp = 'rle'
    elif args.compression =='dic':
        cp = 'dic'
    elif args.compression =='for':
        cp = 'for'
    else: 
        cp = 'dif'

if args.dataType not in ["int8", "int16", "int32", "int64", "string"]:
    raise NameError(f'The options available for the -dt argument are "int8", "int16", "int32", "int64" and "string",  but got {args.dataType} instead.')
else: 
    if args.dataType =='int8': 
        dt = 'int8'
    elif args.dataType =='int16':
        dt = 'int16'
    elif args.dataType =='int32':
        dt = 'int32'
    elif args.dataType =='int64':
        dt = 'int64'
    else: 
        dt = 'string'

# we first try to open the file to check if the path is correct or not (to avoid missleading errors).
f = open(args.filePath, "r")
path_dir = 'C:/UNIVERSITY/3semADM/A2/'
file_name = os.path.basename(args.filePath)

# The file has a structure like : name-datatype.csv , so we want to extract the datatype.
file_dataType = file_name.split('-')[1]
file_dataType = file_dataType.split('.')[0]

# if the data type of the file is not the same as the one provided raise an error.
if dt != file_dataType:
    raise NameError(f'The data type values do not match...\nProvided data type: {dt}\nFile data type: {file_dataType}')

# files containing integers can only be encoded using bin, for and dif techniques
if file_dataType == 'string':
    if cp == 'bin' or cp == 'for' or cp == 'dif':
        raise NameError(f'The file has a data type {file_dataType}, imcompatible with the technique {cp}, try using "rle" or "dic" instead.')

# we now work with the values passed as arguments in terminal
if ed == 'en':
    print('Encoding the file...')
    # we create a new file where we input the encoded data.
    new_f = open(path_dir + file_name + '.' + cp, 'a')

    if cp == 'bin':
        all_items = []
        temp_item = ""
        counter = 0
        
        for item in f.read():
            if item != '\n':
                temp_item = temp_item + item
                # print(temp_item)
            else:
                # to get all 8 bits of a number use {number:08b} , if not use {number:b9}
                # formatted_item = f'{int(temp_item):08b}'
                formatted_item = f'{int(temp_item):b}'
                new_f.write(formatted_item + '\n')
                all_items.append(formatted_item + "\n")
                temp_item = ""

    if cp == 'bin2':
        
        temp_item = ""
        all_items = []

        with open(args.filePath, 'r') as file:
            csvreader = csv.reader(file, delimiter='\n')
            with open(path_dir + file_name + '.' + cp, mode='w') as new_f:
                for item in csvreader:
                    formatted_item = f'{int(item[0]):b}'
                    all_items.append(formatted_item)
                item_writer = csv.writer(new_f, delimiter='\n')
                item_writer.writerow(all_items)

    if cp == 'bin3':
        temp_item = ""
        all_items = []

        with open(args.filePath, 'r') as file:
            csvreader = csv.reader(file, delimiter='\n')
            with open(path_dir + file_name + '.' + cp, 'wb') as new_file:
                for item in csvreader:
                    formatted_item = f'{int(item[0]):b}'
                    all_items.append(formatted_item)
                    pickle.dump(formatted_item, new_file)

        for i in range(100):
            print(all_items[i])

        # with open(path_dir + file_name + '.' + cp, 'wb') as new_file:
        #     pickle.dump(all_items, new_file)


        
    if cp == 'rle':
        pass

    if cp == 'dic':
        pass

    # if cp == 'for':
    #     # First case, using the mean of the list
    #     all_items = []
    #     for item in f.read():
    #         all_items.append(int(item))
        
    #     # tenemos que implementar un counter para chequear como eliminar los \n

    #     # we take the average as the reference an encoded it as the first entry value
    #     reference = sum(all_items) / len(all_items)
    #     formatted_item = f'{int(reference):b}'
    #     new_f.write(reference + '\n')

    #     for item in all_items:
    #         formatted_item = f'{int(item-reference):b}'
    #         new_f.write(formatted_item + '\n')


        
    if cp == 'dif':
        pass
    
    new_f.close()
    

