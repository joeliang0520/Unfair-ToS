from document_preprocess import Tos
import pandas as pd
import requests
import json
import re
from io import StringIO

class Highlighter():
    def __init__(self, document:Tos, openai_key = None, model = 'gpt-4-1106-preview'):
        if not isinstance(document, Tos):
            print('Error: document has to be an instance of ToS class')
            return
        self.document = document
        if openai_key == None:
            print('Warning: No openai key is provided, please use set_openai_key to set the key')
        else:
            print('Openai key recevied. Unfair-ToS will not keep your key in the system')
        self.openai_key = openai_key
        
        #used to store the output from the selected model
        self.highlighted_text = None
        self.highlighted_summary = None
        self.index = None
        #used to store the selected model
        self.model = model
    
    @property
    def openai_key(self):
        if self._openai_key == None:
            return None
        return self._openai_key
    @openai_key.setter
    def openai_key(self, key):
        if key != None or key != "":
            print('OpenAI key is Updated. Unfair-ToS will not keep your key in the system')
        else:
            print('Stored OpenAI key is cleared')
        self._openai_key = key
        
    def update_document(self, document):
        if not isinstance(document, Tos):
            print('Error: document has to be an instance of ToS class')
            return
        self.document = document
        self.highlighted_text = None
        self.highlighted_summary = None
        self.system_prompt = None
        print('Warning: Document is updated. All previous results are cleared')
    
    def hightlight_sentences(self, index = True):
        try:
            if self.openai_key == None:
                print('Error: No openai key is provided, please use set_openai_key to set the key')
                #throw exception
                raise Exception('No openai key is provided')
            text_to_summarize = '\n --- \n ### service provider ###'+self.document.name+'\n ### term of service document ### \n'
                    
            if not index:
                print('Warning: Disable index feature will caused increasing in word-tokens consumed by OpenAI')
                for text in self.document.input_df['content']:
                    text_to_summarize += text + '\n'
                #read final prompt.txt as string
                with open('\data\Final Prompt_nonindex.txt', 'r') as file:
                    self.system_prompt = file.read()
                    
            elif self.document.input_df.shape[1] == 1:
                print('Warning: The input ToS document is not indexed but index feature is selected. The system will automatically indexed it')    
                for index,text in enumerate(self.document.input_df['content']):
                    text_to_summarize +='index'+str(index) + ': ' + text + '\n'
                    
                with open('\data\Final Prompt.txt', 'r') as file:
                    self.system_prompt = file.read()
                    
            elif self.document.input_df.shape[1] == 2:
                for index,text in zip(self.document.input_df['input'],self.document.input_df['sentences']):
                    text_to_summarize +='index'+str(index) + ': ' + text + '\n'
                with open('Final Prompt.txt', 'r') as file:
                    self.system_prompt = file.read()
            text_to_summarize += "--- END OF DOCUMENT ---"
            
            print('Input conctraction completed, estimated input word token is {}. Highlighting sentences...'.format(len(text_to_summarize.split(' '))))
            # Headers for the POST request
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.openai_key}'
            }

            # Data payload for the POST request
            data = {
                'model': self.model,
                'messages': [
                    {"role": "system", "content": 'You are a helpfull assistant.'},
                    {"role": "user", "content": self.system_prompt + text_to_summarize}
                ],
            }
            
            # URL for the OpenAI API chat completions endpoint
            url = 'https://api.openai.com/v1/chat/completions'

            # Make the POST request to the OpenAI API
            response = requests.post(url, headers=headers, data=json.dumps(data))
            
            # Check if the request was successful
            if response.status_code == 200:
            # Extract and format the completion output
                response_data = response.json()
                generated_output = response_data['choices'][0]['message']['content']
            else:
                raise Exception(f"Failed to get a response from the OpenAI API. Status code: {response.status_code}, Response: {response.text}")
            
            csvStringIO = StringIO(generated_output)
            result_df = pd.read_csv(csvStringIO, sep=",")
            
            self.highlighted_text = result_df.iloc[:,0]
            self.highlighted_summary = result_df.iloc[:,1].tolist()
            
            if index:
                print('Converting index to sentence...')
                tem= []
                self.index = [int(re.sub(r'[^\d]+', '', i)) for i in self.highlighted_text.tolist()]
                print(self.index)
                for index in self.index:
                    tem.append(self.document.input_df['sentences'][index])
                self.highlighted_text = tem
                print('Successfully converted index to sentence')
            print('Successfully highlighted and summarized sentencs. Please use .highlighted_text and .highlighted_summary to access the results')
                
        except Exception as e:
            print('Error in highlighting sentences: ',e)
            raise Exception('Error in highlighting sentences: ',e)