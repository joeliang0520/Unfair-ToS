import os
import pandas as pd
import numpy as np
import re
import nltk
import requests
import json
import csv

# Class for reading and preprocessing the document, and store the result in a dataframe
# input: path to the document
# input: service provider name
class ToS:
    def __init__(self, serivce_provider_name, document = None):
        self.name = serivce_provider_name
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.clean_text = None
        if document == None:
            self.raw_content = ""
            print('Warning: No document is provided, please use read_tos_as_csv or read_tos_as_txt to read the document')
        elif document.islist():
            self.is_tokenized = True
            print('Warning: The provided document is list of string, system will treat it as tokenized text')
            if not document[0].istring():
                print('Error: Please make sure the tokenized document is a list of string')
            self.raw_content = document
        elif document.istring():
            self.is_tokenized = False
            self.raw_content = document
        else:
            print('Error: Document has to be either a string, list of string or None ',document.type(),'is provided')
    
    def read_tos_as_csv(self, path):
        try:
            if not os.path.exists(path):
                #throw exception
                raise Exception('File not found')
            df = pd.read_csv(path)
            self.raw_content = df['content']
            self.is_dataframe = True
        except Exception as e:
            print('Error in processing csv file: ',e)

    def read_tos_as_txt(self, path):
        try:
            if not os.path.exists(path):
                #throw exception
                raise Exception('File not found')
            with open(path, 'r', encoding='utf-8') as f:
                self.raw_content = f.read()
        except Exception as e:
            print('Error in processing txt file: ',e)
    
    def clean_text(self):
        def clean(content):
            content = [x.replace('\n', ' ').replace('e.g. ','e.g.') for x in content]
            content = [re.sub(r'[^\x00-\x7F]+|&nbsp',' ', x) for x in content]
            #replace digit.digit.digit with space
            content = [re.sub('\d+\.\d+\.\d+', ' ', x) for x in content]
            content = [re.sub('\d+\.\d+', ' ', x) for x in content]
            # #remove html tags
            content = [re.sub('<[^<]+?>', '', x) for x in content]
            content = [re.sub('[<;>]+', '', x) for x in content]
            # remove quotation marks
            content = [re.sub('\"|\'', '', x) for x in content]
            # split row into several rows by .
            content = [x.split('. ') for x in content]
            # #flatten the list
            content = [item for sublist in content for item in sublist]
            # #remove extra space
            content = [re.sub(' +', ' ', x) for x in content]
            content = [x.strip() for x in content]
            content = [x for x in content if x != '' and x != '.']
            content = [x.lower() for x in content]
            #remove less than 3 words
            content = [x for x in content if len(x.split()) > 5]
            # #replace'â\x80\x99' with '
            # #drop duplicate
            #remove any character that is not in string.printable
            content_lst = content
            content = set(content)
            print(len(content_lst) - len(content), 'duplicates removed')
            return content       

        try:
            if self.raw_content == None:
                raise Exception('No content found, Please make sure you have\
                                 read the document using either read_tos_as_csv or \
                                read_tos_as_txt')
            
            content = self.raw_content

            if not self.is_tokenized:
                content = self.tokenizer.tokenize(content)
                
            content  = clean(clean)

            self.clean_text = content 

        except Exception as e:
            print('Error in cleaning text: ',e)

    