import os
import pandas as pd
import re
import nltk

# Class for reading and preprocessing the document, and store the result in a dataframe
# input: path to the document
# input: service provider name

class Tos:
    def __init__(self, serivce_provider_name = None, document = None,used_index = True):
        self.name = 'No name is provided'
        if serivce_provider_name == None:
            print('Warning: No service provider name is provided, please use set_name to set the name')
        else:
            self.name = serivce_provider_name
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.used_index = used_index

        self.clean_text = None
        self.input_df = None

        if document == None:
            self.raw_content = ""
            print('Warning: No document is provided, please use read_tos_as_csv or read_tos_as_txt to read the document')
        elif document.islist():
            self.is_tokenized = True
            print('Attention: The provided document is recognized as a list of strings. The system will automatically treat it as sentences.')
            if not document[0].istring():
                print('Error: Please make sure the tokenized document is a list of string')
            self.raw_content = document
        elif document.istring():
            self.is_tokenized = False
            self.raw_content = document
        else:
            print('Error: Document has to be either a string, list of string or None ',document.type(),'is provided')
      
    @property
    def clean_text(self):
        return self._clean_text
    @clean_text.setter
    def clean_text(self, content):
        self._clean_text = content
        
    @property
    def name(self):
        if name != None:
            name = self._name
            #capitalize the first letter of each word
            name = name.split()
            name = [x.capitalize() for x in name]
            name = ' '.join(name)
        return name
    @name.setter
    def name(self, name):
        self._name = name
        
    # allow user to read the document as csv file, 
    # the document should have a column named 'content' 
    # as the tokenized documents
    # input: path to the csv file
    def read_tos_as_csv(self, path):
        try:
            if not os.path.exists(path):
                #throw exception
                raise Exception('File not found')
            df = pd.read_csv(path)
            #select first column
            self.raw_content = df.iloc[:,0]
            print('Attention: The provided document is recognized as a list of strings. The system will automatically treat it as sentences.')
            self.is_tokenized= True
        except Exception as e:
            print('Error in processing csv file: ',e)
            raise Exception('Error in processing csv file: ',e)

    def read_tos_as_txt(self, path):
        try:
            if not os.path.exists(path):
                #throw exception
                raise Exception('File not found')
            with open(path, 'r', encoding='utf-8') as f:
                self.raw_content = f.read()
            self.is_tokenized = False
        except Exception as e:
            print('Error in processing txt file: ',e)
            raise Exception('Error in processing txt file: ',e)
    
    def cleaning_text(self):
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
            return list(content)

        try:            
            content = self.raw_content
            if self.is_tokenized:
                print('Attention: Skipped tokenization to sentence level')
            if not self.is_tokenized:
                content = self.tokenizer.tokenize(content)
                
            content  = clean(content)
            print('Attention: The provided Terms of Service (ToS) have been successfully preprocessed. \
                   Total Number sentences: ',len(content))
            self.clean_text = content

            ## add string index to the dataframe
            if self.used_index:
                print('Index feature is used to replace the original text')
                self.index = [i for i in range(len(content))]
                self.input_df = pd.DataFrame({'input':self.index, 'sentences':self.clean_text})
            else:
                print('Warning: Failure to utilize the Index feature may result \
                      in elevated consumption of OpenAI tokens.')
                self.input_df = pd.DataFrame({'input':self.index, 'sentences':self.clean_text})


        except Exception as e:
            print('Error in cleaning text: ',e)
            raise Exception('Error in cleaning text: ',e)

    