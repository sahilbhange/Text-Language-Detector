# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 16:40:59 2018

@author: Sandman
"""

import argparse
import os
from google.cloud import translate
import six
import pandas as pd
import re

# Import the Google Cloud credential file in the current environment
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\Sandman\****\Translate API-****.json'

translate_client = translate.Client()

# Open the file with text 
with open('C:\\Users\\Sandman\*****\File_name.txt','r', encoding="utf8") as f:
    lines = f.readlines()


# Create header with Input Text to detect language,
# artcl_year -- to extract the article year from the text
# confidence -- confidence at which the translator detected the language
# Langauge_detected -- Language detected by the google translator
header = ["input_text", "confidence", "artcl_year", "Language_detected"]
file = open("C:\\Users\\Sandman\*****\output_filename.csv", 'w',encoding='utf8')
file.write(','.join(header) + '\n')

for i in range(len(lines)):
    str=lines[i]
    result = translate_client.detect_language(str)
    input_str = format(result['input'])
    confidence = format(result['confidence'])
    str_lang = format(result['language'])
    try:    
        artcl_year=re.search(r"(\d{4})", str).group(1)
    except KeyError:
        artcl_year=00
        print("Malformed String",str)
    #artcl_year=re.search(r"(\d{4})", str).group(1)
    row_string = ''
    row_string += '"' + input_str.replace('"', '').replace('\n', '') + '"' + ','
    row_string += '"' + confidence.replace('"', '').replace('\n', '') + '"' + ','
    row_string += '"' + artcl_year.replace('"', '').replace('\n', '') + '"' + ','
    row_string += '"' + str_lang.replace('"', '').replace('\n', '') + '"' + '\n'
    file.write(row_string)


        #row_list.extend((input_str, confidence, str_lang))
        #list_all.append(row_list)

file.close()
print("Generated table csv File")

df=pd.read_csv('C:\\Users\\Sandman\****\File_name.csv',encoding='utf-8')

def func(year):
    if year < 1800:
        return "Before 1800"
    elif year >= 1800 and year <= 1849:
        return "1800-1849" 
    elif year >= 1850 and year <= 1899:
        return "1850-1899"
    elif year >= 1900 and year <= 1949:
        return "1900-1949"
    elif year >= 1950 and year <= 2018:
        return "1950 and After"
    else:
        return "NA" 
    
df['range_year'] = df['artcl_year'].apply(func)

df.to_csv("Sheynin_after_800_year_range.csv")



