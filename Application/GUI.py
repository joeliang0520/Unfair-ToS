from tkinter import *
import customtkinter
from document_preprocess import Tos
from hglighting_summary import Highlighter
from tkinter import filedialog
import threading
import pandas as pd
import re
from tkinter import ttk
from PIL import ImageTk, Image
   
def setting_window(highlighter:Highlighter):
    def change_api_key(highlighter:Highlighter):
        dialog = customtkinter.CTkInputDialog(text="New API Key:", title="Change API Key")
        highlighter.openai_key = dialog.get_input()
        if highlighter.openai_key == None or highlighter.openai_key == "":
            #set to red color
            current_key.configure(text = 'No key is provided', fg = 'red')
            api_warning.configure(text ='No OpenAI Key is Provided. Pleas updated it in Setting before using the service', text_color = 'red')
        else:
            api_warning.configure(text ='Welcome to Unfair ToS. Current Model: ' + highlighter.model, text_color = 'black')
            current_key.configure(text = highlighter.openai_key[:3]+"****"+highlighter.openai_key[-3:], fg = 'black')
          
    def change_model(highlighter:Highlighter):
        def update(highlighter:Highlighter, new_model:StringVar):
            highlighter.model = new_model.get()
            current_model.configure(text = highlighter.model)
            
            if highlighter.openai_key != None and highlighter.openai_key != "":
                api_warning.configure(text ='Welcome to Unfair ToS. Current Model: ' + highlighter.model, text_color = 'black')
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
            current_key.configure(text = 'No key is provided', fg = 'red')
            api_warning.configure(text ='No OpenAI Key is Provided. Pleas updated it in Setting before using the service', text_color = 'red')
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
        current_key.configure(text = 'No key is provided', fg = 'red')
    else:
        current_key.configure(text = highlighter.openai_key[:3]+"***"+highlighter.openai_key[-3], fg = 'black')
        
    current_key.grid(row = 0, column = 1)
    Button(setting, text = "Change API Key", command = lambda: 
        change_api_key(highlighter)).grid(row = 0, column = 3)
    Button(setting,text='Clear API Key',command=clear_api_key).grid(row=0,column=4)
    Label(setting, text ="Current Model: ").grid(row = 1, column = 0)
    current_model = Label(setting, text =highlighter.model)
    current_model.grid(row = 1, column = 1)
    Button(setting, text = "Change Model", command = lambda:change_model(highlighter)).grid(row = 1, column = 3)

def service_provder_name():
    dialog = customtkinter.CTkInputDialog(text="Please enter the service provider name:", title="Service Provider Name")
    highlighter.document.name = dialog.get_input()
    summary.delete('1.0', END)
    summary.insert('1.0',highlighter.document.name + '\'s ToS is succesfully imported. Please click Highlight to start')
            
def UploadAction():
    succesfull_upload = False
    try:
        filename = filedialog.askopenfilename()
        filetype = filename.split('.')[-1]
        if filetype == 'txt':
            highlighter.document.read_tos_as_txt(filename)
            highlighter.document.cleaning_text()
            succesfull_upload = True

        elif filetype == 'csv':
            highlighter.document.read_tos_as_csv(filename)
            highlighter.document.cleaning_text()
            succesfull_upload = True
            
        elif filename != '':
            warning = Toplevel(root)
            warning.title("Error")
            Label(warning, text ="Unfair ToS only support txt and csv file").pack()
            Button(warning, text = "OK", command = lambda: warning.destroy()).pack()
        
        #covert the document to string
        if succesfull_upload:
            service_provder_name()
            if document.is_tokenized:
                text = '\n'.join(list(highlighter.document.raw_content))
            else:
                text  = highlighter.document.raw_content
        
            content.delete('1.0', END)
            content.insert(INSERT,text)
            global shown_cleaned
            hightlight_bt.configure(state='normal')
            clean_or_original.grid(row=0, column=4, sticky="ew", padx=5)
            if shown_cleaned == 'Show Original':
                shown_cleaned = "Show Cleaned"
                
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
            hightlight_bt.configure(state='disabled')
            show_demo_bt.configure(state='normal')
        
        Button(warning, text = "OK", command = cleaning).pack()
        Button(warning, text = "Cancel", command = lambda: warning.destroy()).pack()
        
    except Exception as e:
        warning = Toplevel(root)
        warning.title("Error")
        Label(warning, text='Error occurs when clearing the document').pack()
        Label(warning, text = e).pack()
        Button(warning, text = "OK", command = lambda: warning.destroy()).pack()

def toggle():
    global shown_cleaned
    if shown_cleaned == 'Show Original':
        if highlighter.document.is_tokenized:
            text = '\n'.join(list(highlighter.document.raw_content))
        else:
            text  = highlighter.document.raw_content
        shown_cleaned = 'Show Cleaned'
    else:
        text = '\n'.join(list(highlighter.document.clean_text))
        shown_cleaned = 'Show Original'
        
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
        service_provder_name()
        
        content.delete('end', END)
        content.insert(INSERT,text)
        
        hightlight_bt.configure(state='normal')
        
        clean_or_original.grid(row=0, column=4, sticky="ew", padx=5)
        global shown_cleaned
        if shown_cleaned == 'Show Original':
            shown_cleaned = "Show Cleaned"
        
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
    button.bind("<Enter>", func=lambda e: button.configure(
        background=colorOnHover))
 
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.configure(
        background=colorOnLeave))

def hightlight(demo):
    try:
        window = Toplevel(root)
        window.title("Highlighting")
        window.geometry("500x500")
        Label(window, text ="Highlighting is in progress").pack()
        progressbar = ttk.Progressbar(window,mode="indeterminate")
        progressbar.start()
        progressbar.pack()
        hightlight_bt.configure(state='disabled')

        if not demo:
            highlighter.hightlight_sentences()
            
        content.delete('1.0', END)
        summary.delete('1.0', END)
        
        for i in range(0,len(highlighter.document.clean_text)):
            text = highlighter.document.clean_text[i]
            if i in highlighter.index:
                indexes = highlighter.index.index(i)
                sum = highlighter.highlighted_summary[indexes]
                difference = len(text) - len(sum)
                content.insert(INSERT,text+'\n','hightlight')
                content.insert('end','\n')
                summary.insert(INSERT,sum)
                if difference > 0:
                    summary.insert(INSERT,text[len(sum):]+'\n','hidden')
                else:
                    summary.insert(INSERT,'\n','hidden')
                summary.insert('end','\n')
            else:
                content.insert(INSERT,text+'\n')
                content.insert('end','\n')
                summary.insert(INSERT,text+'\n','hidden')
                summary.insert('end','\n')
                
        window.destroy()    
                
    except Exception as e:
        window.destroy()
        warning = Toplevel(root)
        warning.title("Error")
        Label(warning, text='Error occurs when highlighting the document').pack()
        hightlight_bt.configure(state='normal')
        Label(warning, text = e).pack()
        Button(warning, text = "OK", command = lambda: warning.destroy()).pack()
        
def hightlight_button(demo):
    window = Toplevel(root)
    window.title("Warning")
    window.geometry("500x400")
    def cost_calculator():
        text = ' '.join(list(highlighter.document.clean_text))
        token = len(text.split(' '))
        if highlighter.model == 'gpt-4':
            cost = token /750 * 0.01
        elif highlighter.model == 'gpt-3.5-turbo-1106':
            cost = token /750 * 0.001
        elif highlighter.model == 'gpt-3.5-turbo':
            cost = token /750 * 0.001
        elif highlighter.model == 'gpt-4-1106-preview':
            cost = token /750 * 0.03
        return str(cost)
    
    if demo:
        print('You are using demo mode')
        tem = pd.read_csv('Application/data/Crunchyroll_Terms of Service_summary.csv')
        clean = pd.read_csv('Application/data/Crunchyroll_Terms of Service.csv')
        highlighter.document.clean_text = clean.iloc[:,0].tolist()
        highlighter.index = [int(re.sub(r'[^\d]+', '', i)) for i in tem['Highlight'].tolist()]
        highlighter.highlighted_summary = tem['Summary'].tolist()
        Label(window, text ="You are using the demo. There will be no cost").pack()
    else:
        Label(window, text ="You are about to start the hightlighting process").pack()
        Label(window, text ="This action is not recoverable and will directly bill to you OpenAI account").pack()
        Label(window, text ="\n").pack()
        Label(window, text ="Current Model: "+ highlighter.model).pack()
        Label(window, text ='Estimated Input Cost based on selected model is ' + cost_calculator()).pack()
        Label(window, text ="Please make sure you have enough OpenAI credit").pack()
        Label(window, text ="\n").pack()
        Label(window, text ="PLEASE PAY ATTENTION",fg='red').pack()
        Label(window, text ="This is a beta version.",fg='red').pack() 
        Label(window, text ="Unfair-ToS is not responsible for any cost ocurred when using this service.", fg ='red').pack()
        Label(window, text ="\n").pack()
    
    def proess(demo):
        window.destroy()
        threading.Thread(target= lambda: hightlight(demo)).start()
        show_demo_bt.configure(state='disabled')
    
    Button(window, text = "OK", command = lambda: proess(demo)).pack()
    Button(window, text = "Cancel", command = lambda: window.destroy()).pack()
    

def show_demo():
    global demo
    demo = True
    hightlight_button(demo)
    demo = False

def multiple_yview(*args):
    content.yview(*args)
    summary.yview(*args)
    
#initialize the document and highlighter      
document = Tos()
highlighter = Highlighter(document)
demo = False
root = customtkinter.CTk()
root.title('Unfair ToS')
root.geometry("1200x500")
customtkinter.set_appearance_mode("light")
menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Import From File", command=UploadAction)
filemenu.add_command(label="Import From Textbox", command=update_from_text_box)
filemenu.add_command(label="Show Cleaned/Original Text", command=toggle)
filemenu.add_command(label="Remove All Text", command=clear_textbox)
filemenu.add_separator()
filemenu.add_command(label="Hightlight", command=hightlight_button)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="All Setting", command=lambda: setting_window(highlighter))
menubar.add_cascade(label="Setting", menu=editmenu)

file_icon = customtkinter.CTkImage(Image.open('Application/data/file.png'))
setting_icon = customtkinter.CTkImage(Image.open('Application/data/icons8-settings-50.png'))
demo_icon = customtkinter.CTkImage(Image.open('Application/data/icons8-demo-64.png'))
options = customtkinter.CTkFrame(root)
customtkinter.CTkButton(options, text = "", image=file_icon, 
                        command = lambda: threading.Thread(target=UploadAction).start(),
                        width = 50, height = 50,fg_color='transparent').grid(row=0, column=0, padx=5, pady=5)
customtkinter.CTkButton(options, text = "", image = setting_icon,
                        command = lambda: setting_window(highlighter),width = 50, height = 50
                        ,fg_color='transparent').grid(row=1, column=0, padx=5)
show_demo_bt = customtkinter.CTkButton(options, text = "", image=demo_icon, command = show_demo,
                                       width = 50, height = 50,fg_color='transparent')
show_demo_bt.grid(row=4, column=0, padx=5, pady=5)
shown_cleaned = False
text_box = customtkinter.CTkFrame(root)
text_box.rowconfigure(0, weight=0)
text_box.rowconfigure(1, weight=10)
text_box.rowconfigure(2, weight=0)

content_edit = customtkinter.CTkFrame(text_box)

customtkinter.CTkButton(content_edit, text = "Clear", command = lambda: threading.Thread(target=clear_textbox).start()
                        ,width=50,height=50).grid(row=0, column=1, sticky="e", padx=15)
customtkinter.CTkButton(content_edit, text = "Update", command = lambda: threading.Thread(target=update_from_text_box).start()
                        ,width=50,height=50).grid(row=0, column=2, sticky="e", padx=15)
hightlight_bt = customtkinter.CTkButton(content_edit, text = "Highlight", height=50,command = lambda:  hightlight_button(demo),state='disabled')
hightlight_bt.grid(row=0, column=3, sticky="w", padx=15)
clean_or_original = customtkinter.CTkSwitch(content_edit,command = lambda: threading.Thread(target=toggle).start(),text='Show Cleaned Text')

text_scroll = customtkinter.CTkScrollbar(text_box)
content = customtkinter.CTkTextbox(text_box,width=500, yscrollcommand=text_scroll.set)
content.insert('1.0','No Term of Service is Provided. Please paste your Term of Service here or import from file')
content.tag_config('hightlight', background="yellow", foreground="red")
summary = customtkinter.CTkTextbox(text_box,width=500, yscrollcommand=text_scroll.set)
summary.insert('1.0','No Term of Service is Provided. Please paste your Term of Service here or import from file')
summary.tag_config('hidden', foreground="white")
text_scroll.configure(command=multiple_yview)
text_box.columnconfigure(0, weight=1)
text_box.columnconfigure(1, weight=1)

content_label = customtkinter.CTkLabel(text_box, text='Original Text')
summary_label = customtkinter.CTkLabel(text_box, text='Summary')
content_label.grid(row=0, column=0)
summary_label.grid(row=0, column=1)
text_scroll.grid(row=1, column=2, sticky="nsew")

root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=10)
root.rowconfigure(0, weight=10)
root.rowconfigure(1, weight=0)
content.grid(row=1, column=0, sticky="nsew")
summary.grid(row=1, column=1, sticky="nsew")

content_edit.grid(row=2,column=0, sticky="nsew")

options.grid(row=0, column=0, sticky="nsew")
text_box.grid(row=0, column=1, sticky="nsew")

logo = customtkinter.CTkImage(Image.open('Application/data/unfair-tos.png').resize((300, 300)))
customtkinter.CTkLabel(root, text = "",image=logo).grid(row =1, column = 0,sticky="nsew")
customtkinter.set_default_color_theme('blue')
if highlighter.openai_key == None or highlighter.openai_key == "":
    #set to red color
    api_warning = customtkinter.CTkLabel(root, text ='No OpenAI Key is Provided. Please update it in Setting before using the service', text_color='red')
    api_warning.grid(row =1, column = 1, columnspan=2)
    
root.config(menu=menubar)
root.mainloop()