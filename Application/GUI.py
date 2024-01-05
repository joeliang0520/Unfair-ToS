from tkinter import *
from document_preprocess import Tos
from hglighting_summary import Highlighter
from tkinter import filedialog
import threading
import pandas as pd
import re

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()
   
def setting_window(highlighter:Highlighter):
    def change_api_key(highlighter:Highlighter):
        
        def update(highlighter:Highlighter, api_key_entry:Entry):
            highlighter.openai_key = api_key_entry.get()
            if highlighter.openai_key == None or highlighter.openai_key == "":
                #set to red color
                current_key.config(text = 'No key is provided', fg = 'red')
                api_warning.config(text ='No OpenAI Key is Provided. Pleas updated it in Setting before using the service', fg = 'red')
            else:
                api_warning.config(text ='Welcome to Unfair ToS. Current Model: ' + highlighter.model, fg = 'black')
                current_key.config(text = highlighter.openai_key, fg = 'black')
            openai_api_layer.destroy()
            
        openai_api_layer = Toplevel(setting)
        openai_api_layer.title("Change API Key")
        Label(openai_api_layer, text ="New API Key:").grid(row = 0, column = 0)
        api_key_entry = Entry(openai_api_layer)
        api_key_entry.grid(row = 0, column = 1)
        Button(openai_api_layer, text = "Save", command = \
               lambda: update(highlighter,api_key_entry)).grid(row = 1, column = 0)
        Button(openai_api_layer, text = "Cancel", command = \
               lambda: openai_api_layer.destroy()).grid(row = 1, column = 1)
          
    def change_model(highlighter:Highlighter):
        def update(highlighter:Highlighter, new_model:StringVar):
            highlighter.model = new_model.get()
            current_model.config(text = highlighter.model)
            
            if highlighter.openai_key != None and highlighter.openai_key != "":
                api_warning.config(text ='Welcome to Unfair ToS. Current Model: ' + highlighter.model, fg = 'black')
            model_layer.destroy()
        
        model_layer = Toplevel(setting)
        model_layer.title("Change Model")
        model = Frame(model_layer)
        Label(model, text ="New Model: ").grid(row = 0, column = 0)
        options = [ 
        "gpt-4", 
        "gpt-3.5-turbo-1106", 
        "gpt-3.5-turbo", 
        "gpt-4-1106-preview"
        ]
        new_model = StringVar(model)
        new_model.set(highlighter.model)
        model_list = OptionMenu(model, new_model, *options)
        model_list.grid(row = 0, column = 1)
        model.pack()
        buttons = Frame(model_layer)
        Button(buttons, text = "Save", command = \
               lambda: update(highlighter,new_model)).grid(row = 0, column = 0)
        Button(buttons, text = "Cancel", command = \
               lambda: model_layer.destroy()).grid(row = 0, column = 1)
        buttons.pack()
        Label(model_layer, text ="Warning: Different models may have different cost per tokens").pack()
    
    def clear_api_key():
        warning = Toplevel(setting)
        warning.geometry("500x100")
        warning.title("Warning")
        Label(warning, text ="Warning: This action will remove the current API key").pack()
        
        def clear():
            highlighter.openai_key = None
            current_key.config(text = 'No key is provided', fg = 'red')
            api_warning.config(text ='No OpenAI Key is Provided. Pleas updated it in Setting before using the service', fg = 'red')
            warning.destroy()
        
        Button(warning, text = "OK", command = clear).pack()
        Button(warning, text = "Cancel", command = lambda: warning.destroy()).pack()
        
    setting = Toplevel(root)
    setting.title("General Setting")
    setting.geometry("500x200")
    Label(setting, text ="Current API Key: ").grid(row = 0, column = 0)
    current_key = Label(setting, text ="")
    if highlighter.openai_key == None or highlighter.openai_key == "":
        #set to red color
        current_key.config(text = 'No key is provided', fg = 'red')
    else:
        current_key.config(text = highlighter.openai_key, fg = 'black')
        
    current_key.grid(row = 0, column = 1)
    Button(setting, text = "Change API Key", command = lambda: 
        change_api_key(highlighter)).grid(row = 0, column = 3)
    Button(setting,text='Clear API Key',command=clear_api_key).grid(row=0,column=4)
    Label(setting, text ="Current Model: ").grid(row = 1, column = 0)
    current_model = Label(setting, text =highlighter.model)
    current_model.grid(row = 1, column = 1)
    Button(setting, text = "Change Model", command = lambda:change_model(highlighter)).grid(row = 1, column = 3)

def UploadAction():
    succesfull_upload = False
    try:
        filename = filedialog.askopenfilename()
        filetype = filename.split('.')[-1]
        if filetype == 'txt':
            document.read_tos_as_txt(filename)
            document.cleaning_text()
            highlighter.update_document(document)
            clean_or_original.grid(row=1, column=0, sticky="ew", padx=5)
            succesfull_upload = True

        elif filetype == 'csv':
            document.read_tos_as_csv(filename)
            document.cleaning_text()
            highlighter.update_document(document)
            clean_or_original.grid(row=1, column=0, sticky="ew", padx=5)
            succesfull_upload = True
            
        elif filename != '':
            warning = Toplevel(root)
            warning.title("Error")
            Label(warning, text ="Unfair ToS only support txt and csv file").pack()
            Button(warning, text = "OK", command = lambda: warning.destroy()).pack()
        
        #covert the document to string
        if succesfull_upload:
            if document.is_tokenized:
                text = '\n'.join(list(document.raw_content))
            else:
                text  = document.raw_content
        
            content.delete('1.0', END)
            content.insert(INSERT,text)
            summary.delete('1.0', END)
            summary.insert('1.0','ToS Imported. Please click Highlight to start')
            
            if clean_or_original.config('relief')[-1] == 'sunken':
                clean_or_original.config(text = "Show Cleaned",relief="raised")
        else:
            warning = Toplevel(root)
            warning.geometry("500x100")
            warning.title("Message")
            Label(warning, text ="No file is imported").pack()
            Button(warning, text = "OK", command = lambda: warning.destroy()).pack()
                 
    except Exception as e:
        warning = Toplevel(root)
        warning.title("Error")
        Label(warning, text='Error occurs when uploading the document').pack()
        Label(warning, text = e).pack()
        Button(warning, text = "OK", command = lambda: warning.destroy()).pack()
        
def clear_textbox():
    try:
        warning = Toplevel(root)
        warning.geometry("500x100")
        warning.title("Warning")
        Label(warning, text ="Warning: This action will remove texts in the system (not recoverable)").pack()
        
        def cleaning():
            content.delete('1.0',END)
            content.insert('1.0','No Term of Service is Provided. Please paste your Term of Service here or import from file')
            summary.delete('1.0',END)
            summary.insert('1.0','No Term of Service is Provided. Please paste your Term of Service here or import from file')
            clean_or_original.grid_forget()
            new_document = Tos()
            highlighter.update_document(new_document)
            warning.destroy()
            warning2 = Toplevel(root)
            warning2.geometry("500x100")
            warning2.title("Message")
            Label(warning2, text ="All texts are successfully removed").pack()
            Button(warning2, text = "OK", command = lambda: warning2.destroy()).pack()
        
        Button(warning, text = "OK", command = cleaning).pack()
        Button(warning, text = "Cancel", command = lambda: warning.destroy()).pack()
        
    except Exception as e:
        warning = Toplevel(root)
        warning.title("Error")
        Label(warning, text='Error occurs when clearing the document').pack()
        Label(warning, text = e).pack()
        Button(warning, text = "OK", command = lambda: warning.destroy()).pack()

def toggle():
    if clean_or_original.config('relief')[-1] == 'sunken':
        if highlighter.document.is_tokenized:
            text = '\n'.join(list(highlighter.document.raw_content))
        else:
            text  = highlighter.document.raw_content
        clean_or_original.config(text = "Show Cleaned",relief="raised")
    else:
        text = '\n'.join(list(highlighter.document.clean_text))
        clean_or_original.config(text = "Show Original",relief="sunken")
        
    content.delete('1.0', END)
    content.insert('1.0',text)

def update_from_text_box():
    warning = Toplevel(root)
    warning.geometry("500x100")
    warning.title("Warning")
    Label(warning, text ="Warning: This will replace the original document in System").pack()
    def update():
        text = content.get("1.0",END)
        
        document = highlighter.document
        document.raw_content = text
        document.is_tokenized = False
        document.cleaning_text()
        highlighter.update_document(document)
        
        content.delete('1.0', END)
        content.insert(INSERT,text)
        summary.delete('1.0', END)
        summary.insert('1.0','ToS Imported. Please click Highlight to start')
        
        warning.destroy()
        warning2 = Toplevel(root)
        warning2.geometry("500x100")
        warning2.title("Message")
        Label(warning2, text ="Document is updated").pack()
        Button(warning2, text = "OK", command = lambda: warning2.destroy()).pack()
    
    Button(warning, text = "OK", command = update).pack()
    Button(warning, text = "Cancel", command = lambda: warning.destroy()).pack()

def changeOnHover(button, colorOnHover, colorOnLeave):
 
    # adjusting backgroung of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover))
 
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave))

def hightlight():
    try:
        window = Toplevel(root)
        window.title("Highlighting")
        window.geometry("500x100")
        Label(window, text ="Highlighting...").pack()
        highlighter.hightlight_sentences()
        # tem = pd.read_csv('/Users/joeliang/Desktop/SynologyDrive/UofT/ECE1786/project/Unfair-ToS/Dataset for Text Summary Model/cleaned/more_than_40_sentences/model_results/Crunchyroll_Terms of Service_summary.csv')
        # clean = pd.read_csv('/Users/joeliang/Desktop/SynologyDrive/UofT/ECE1786/project/Unfair-ToS/Dataset for Text Summary Model/cleaned/more_than_40_sentences/original/Crunchyroll_Terms of Service.csv')
        # highlighter.document.clean_text = clean.iloc[:,0].tolist()
        # highlighter.index = [int(re.sub(r'[^\d]+', '', i)) for i in tem['Highlight'].tolist()]
        print(highlighter.index)
        highlighter.highlighted_summary = tem['Summary'].tolist()
        window.destroy()
        counter = 0
        content.delete('1.0', END)
        summary.delete('1.0', END)
        
        for i in range(0,len(highlighter.document.clean_text)):
            text = highlighter.document.clean_text[i]
            if i in highlighter.index:
                #find i+1 's index in highlighter.index
                indexes = highlighter.index.index(i)
                sum = highlighter.highlighted_summary[indexes]
                difference = len(text) - len(sum)
                content.insert(INSERT,text+'\n','hightlight')
                content.insert('end','\n')
                summary.insert(INSERT,sum)
                if difference > 0:
                    summary.insert(INSERT,text[difference:]+'\n','hidden')
                else:
                    summary.insert(INSERT,'\n','hidden')
                summary.insert('end','\n')
            else:
                content.insert(INSERT,text+'\n')
                content.insert('end','\n')
                summary.insert(INSERT,text+'\n','hidden')
                summary.insert('end','\n')
                
                
    except Exception as e:
        warning = Toplevel(root)
        warning.title("Error")
        Label(warning, text='Error occurs when highlighting the document').pack()
        Label(warning, text = e).pack()
        Button(warning, text = "OK", command = lambda: warning.destroy()).pack()

        
#initialize the document and highlighter      
document = Tos()
highlighter = Highlighter(document)

root = Tk()
root.title('Unfair ToS')
root.rowconfigure(0, minsize=500, weight=1)
root.columnconfigure(1, minsize=1200, weight=1)

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Import From File", command=UploadAction)
filemenu.add_command(label="Import From Textbox", command=update_from_text_box)
filemenu.add_command(label="Show Cleaned/Original Text", command=toggle)
filemenu.add_command(label="Remove All Text", command=clear_textbox)
filemenu.add_command(label="Hightlight", command=hightlight)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="General", command=lambda: setting_window(highlighter))
menubar.add_cascade(label="Setting", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

options = Frame(root, relief=RAISED, bd=2)
Button(options, text = "Import From File", command = UploadAction,height= 3, width=10).grid(row=0, column=0, sticky="ew", padx=5, pady=5)
Button(options, text = "Setting", command = lambda: setting_window(highlighter),height= 3, width=10).grid(row=2, column=0, sticky="ew", padx=5)
clean_or_original = Button(options, text = "Show Cleaned", command = toggle, relief="raised",height= 3, width=5)

edit = Frame(root, relief=RAISED, bd=2)
Button(edit, text = "Clear", command = clear_textbox,height= 2, width=5).grid(row=0, column=1, sticky="e", padx=15)
Button(edit, text = "Update", command = update_from_text_box,height= 2, width=5).grid(row=0, column=2, sticky="e")
hightlight_bt = Button(edit, text = "Highlight", command = hightlight,height= 2, width=5)
hightlight_bt.grid(row=0, column=3, sticky="w", padx=15)

text_box = Frame(root)
text_box.rowconfigure(0, minsize=400, weight=1)
content = Text(text_box)
content.insert('1.0','No Term of Service is Provided. Please paste your Term of Service here or import from file')
content.tag_config('hightlight', background="yellow", foreground="red")

summary = Text(text_box)
summary.insert('1.0','No Term of Service is Provided. Please paste your Term of Service here or import from file')
summary.tag_config('hidden', foreground="white")
content.grid(row=0, column=0, sticky="nsew")
summary.grid(row=0, column=1, sticky="nsew")

options.grid(row=0, column=0, sticky="ns")
text_box.grid(row=0, column=1, sticky="nsew")
edit.grid(row=1,column=1, sticky="nsew")

if highlighter.openai_key == None or highlighter.openai_key == "":
    #set to red color
    api_warning = Label(root, text ='No OpenAI Key is Provided. Please update it in Setting before using the service', fg = 'red')
    api_warning.grid(row =3, columnspan=3)
    
root.config(menu=menubar)
root.mainloop()