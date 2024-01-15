# Unfair-ToS

![unfair-tos](https://github.com/joeliang0520/Unfair-ToS/assets/50597009/123bed0d-d5c9-4362-923f-de1e53b22987)

Terms of service (ToS) are agreements between service providers and their users. These ToS documents often contain complex legal language that users struggle to understand. Such clauses may violate consumer laws, compromise users' rights, and raise privacy concerns.

The Large Language Model's (LLM) proven ability to efficiently extract summaries from complex texts makes it ideal for addressing ToS complexities. The Unfair-ToS employs a GPT-based framework to highlight crucial ToS sentences, offer simplified explanations, and evaluate their fairness, also providing reasons for any unfair terms.

## Model Architecture

![Add a little bit of body text (1) (1)](https://github.com/joeliang0520/Unfair-ToS/assets/50597009/9993fc4a-9042-4100-b9ed-93859384475d)

## Model Result

Please read our [report](https://github.com/joeliang0520/Unfair-ToS/files/13934850/Unfair-ToS.Report.pdf) to learn more about our project motivation, background information, and model evaluation.

## Current Work
We are currently working on a Graphic User Interface to demonstrate the ability of our model. There is an early beta version available in the Application folder, that allows users to upload (txt/csv file) or copy and paste the ToS document, applying our LLM prompts with the different models using your own OPENAI API keys and getting the text highlighting result. The fair/unfair classification feature will be implemented into the GUI in the future release.

![Screenshot 2024-01-14 at 11 31 06 PM](https://github.com/joeliang0520/Unfair-ToS/assets/50597009/57137b42-7cf6-4219-bfbc-0f27a09a491b)


To use this GUI, please clone this repo into your local machine, and install any missing packages. After all the preparation, please run the 'GUI.py' file to start the application.

We prepared a demo ToS document for you to play around with our GUI. Please click the SHOW DEMO button to learn more about this demo. If you want to highlight your own ToS document, you are also required to obtain an OpenAI API key (with enough credits based on the length of ToS and selected model) and upload it using the SETTING function. 

**This is an early beta version! Please use it at your own risk! We are not responsible for any costs or information leaks when using our services**

We are also welcome to any contribution to help us complete the front-end design!

## Model Training
This is the source code for the Unfair ToS project by Jianing Zhang and Jiazhou Liang.

Please use the following guides to access the training datasets, scripts, models, and evaluation metrics to recreate the project.

### Dataset Description

- The folder **Dataset** contains the 100 ToS dataset from the paper 'Detecting and explaining unfairness in consumer contracts through memory networks' used for the text classification model.
  - **ToS-100.csv**: the original dataset from the paper, more details can be found at [Memnet_ToS GitHub](https://github.com/federicoruggeri/Memnet_ToS).
  - **ToS-100-cleaned.csv**: the cleaned dataset for this project, including the original sentences, binary variables for each of the five classes, and a combined variable 'label' for all classes.
  - ToS-100-cleaned-dataset-huggingface: Hugging Face dataset after oversampling, used for fine-tuning the pre-trained GPT-2 model. It is split into 80% training and 20% testing. More information on how to load the dataset into the Hugging Face library can be found [here](https://huggingface.co/docs/datasets/loading).

- The folder **Dataset for Text Summary Model** contains the ToS documents crawled from the ToS;DR website with highlighted sentences by human contributors for text highlighting model. More information about ToS;DR can be found [here](https://tosdr.org/).
  - **html_files** folder contains the raw crawled ToS in HTML format.
  - **text_files** folder contains the raw crawled ToS in TXT format.
  - **cleaned** contains the dataset and model results after cleaning and feeding into the GPT-4 model.
    - **more_than_40_sentences** includes only ToS with more than 40 and less than 50 highlighted sentences from ToS;DR. Different ranges of ToS can be created using the script in `text_summary.ipynb` by changing the parameters indicated in the file. It will create a new folder in the same level as this folder with the name "more_than_[lower_constraint]_sentences."
      - **original** contains all ToS text after cleaning, divided into sentence levels and stored in CSV format.
      - **highlight** contains all ToS highlighted sentences after cleaning.
      - **Combined** adds a label for each sentence in each ToS in **original** (1) if the sentence is highlighted, (0) if not. This dataset will be used as ground truth in our evaluation scripts.
      - **Model Result** contains the GPT-4 output using the current ToS. More details will be explained in the result section.
- **data_extraction_all.py** and **data_extraction_highlight.py** contains the scripts for crawling raw HTML and text formats of ToS and highlighted sentences for ToS.

### Model Training and Evaluation

- **Classification_baseline CNN.ipynb** contains the baseline CNN model for text classification. More details about the training process can be found in the files. We used the 100 ToS.csv mentioned above.
- **Classification.ipynb** contains the fine-tuning process of the pre-trained GPT-2 model using Hugging Face pre trained and auto-tuned interface. More details about its usage can be found [here](https://huggingface.co/docs/transformers/training).
- **Text Summary.ipynb** contains the script to clean the crawled ToS into CSV format at the sentence level. The script uses the OpenAI API to feed the cleaned ToS into the 'gpt-4-turbo-preview' model and creates the output. You need to create your API keys and store them in the local environment to execute the script. More information about the OpenAI API and keys can be found [here](https://openai.com/blog/openai-api).

### Model Result

- **Text Classification**: The fine-tuned GPT-2 model can be found at the following Google Drive link: [Text Classification Model](https://drive.google.com/drive/folders/1xcUodUCSwTzF89c44PKiEGEFEwFR8--i?usp=sharing) due to the size limitation on GitHub. You can use the Hugging Face classification pipeline to load the model and make predictions on new sentences. More detailed information can be found in the last section of **Classification.ipynb** documents.

- **Text Highlighting and Simplification**: Model results and GPT-4 output can be found in 'Dataset for Text Summary Model/cleaned/more_than_40_sentences/model_results'. Within it, the files with:
  - '_baseline.csv' are the highlighted sentences for results from the baseline text rank model.
  - '_summary.csv' contains the highlighted sentences and their simplification for the GPT-4 model. To reduce output token sizes, we use an index to label each sentence. This requires matching it back to the original sentences. More details can be found in **Classification.ipynb**.
  - '_not_predicted.csv' contains all sentences in GPT-4 that are not matched with the ground truth. Please refer to the project report to know why these sentences can be important for users.  
