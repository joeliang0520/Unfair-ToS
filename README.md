# Unfair-ToS

![unfair-tos](https://github.com/joeliang0520/Unfair-ToS/assets/50597009/123bed0d-d5c9-4362-923f-de1e53b22987)

Terms of service (ToS) are agreements between service providers and their users. These ToS documents often contain complex legal language that users struggle to understand. Such clauses may violate consumer laws, compromise users' rights, and raise privacy concerns.

The Large Language Model's (LLM) proven ability to efficiently extract summaries from complex texts makes it ideal for addressing ToS complexities. The Unfair-ToS employs a GPT-based framework to highlight crucial ToS sentences, offer simplified explanations, and evaluate their fairness, also providing reasons for any unfair terms.

## Model Architecture

![Add a little bit of body text (1) (1)](https://github.com/joeliang0520/Unfair-ToS/assets/50597009/9993fc4a-9042-4100-b9ed-93859384475d)

This model leverages GPT-4 through prompts to highlight sentences and generate simplifications for each highlighted sentence from the input, cleaned Terms of Service (ToS). The prompt used in our model has been fine-tuned using 11 ToS documents, comprising approximately 1500 sentences, through prompt engineering. GPT-4 identifies important sentences, and these serve as input to the text classification model.

Each sentence undergoes tokenization using HuggingFace's predefined 'GPT2' tokenizer and is then fed into the pre-trained 'gpt2' model. This model has been fine-tuned on a dataset of 100 ToS using the same tokenizer and padded to the maximum length. The output of the model falls into one of five classes. The purpose of this model is to assign a label to each highlighted sentence, assisting users in identifying the fairness of sentences.

## Model Showcase
Please read our [report](https://github.com/joeliang0520/Unfair-ToS/files/13934850/Unfair-ToS.Report.pdf) to learn more about our project motivation, background information, and model evaluation.

### Some highlight

Inspired by Yoon Kim's paper, we implemented a baseline CNN classification model with k1 = 4 and k2 = 4 for fair/unfair classification. However, its F1 score is only 0.193, indicating a bias towards classifying samples into the class with the majority, which is the 'fair' class. Consequently, the baseline CNN struggles to accurately identify 'unfair' sentences within the samples. 

<p align="center">
<img src="https://github.com/joeliang0520/Unfair-ToS/assets/50597009/dbff8063-99d6-4515-a139-88e42efc5f92" alt="drawing" width="900"/>
</p>

In contrast, our fine-tuned GPT-2 model surpasses the baseline in both metrics. These findings suggest that the GPT-2 model exhibits greater resilience to class imbalance, particularly when 'fair' sentences dominate the corpus, as is often the case.

<p align="center">
<img src="https://github.com/joeliang0520/Unfair-ToS/assets/50597009/9d9a30b3-f4fc-40f3-b49a-e25725edf6a0" alt="drawing" width="700"/>
</p>

## Current Work
We are presently developing a Graphic User Interface to showcase the capabilities of our model. An early beta version is now accessible in the Application folder, enabling users to upload a (txt/csv) file or copy and paste the Terms of Service (ToS) document. This allows the application of our Language Model (LLM) prompts with various models using your personal OPENAI API keys, yielding highlighted text results. The fair/unfair classification feature will be integrated into the GUI in a future release.

![Screenshot 2024-01-14 at 11 31 06 PM](https://github.com/joeliang0520/Unfair-ToS/assets/50597009/57137b42-7cf6-4219-bfbc-0f27a09a491b)

To utilize this GUI, kindly clone this repository into your local machine and install any missing packages. Following the completion of all preparations, execute the 'GUI.py' file to initiate the application.

We have provided a demo Terms of Service (ToS) document for you to experiment with using our GUI. Please click the "SHOW DEMO" button for more information about this demonstration. If you wish to highlight your own ToS document, you must obtain an OpenAI API key (with sufficient credits based on the length of the ToS and the selected model) and upload it using the SETTING function.

**Note: This version is an early beta release. Please use it at your own risk. We are not liable for any costs or information leaks incurred while using our services.**

We also welcome any contributions to assist us in completing the front-end design!

## Model Training
This is the source code for the Unfair ToS project by Jianing Zhang and Jiazhou Liang.

Please use the following guides to access the training datasets, scripts, models, and evaluation metrics to recreate the project.

### Dataset Description

- The folder **Dataset** contains the 100 ToS dataset from the paper 'Detecting and explaining unfairness in consumer contracts through memory networks' used for the text classification model.
  - **ToS-100.csv**: the original dataset from the paper, more details can be found at [Memnet_ToS GitHub](https://github.com/federicoruggeri/Memnet_ToS).
  - **ToS-100-cleaned.csv**: the cleaned dataset for this project, including the original sentences, binary variables for each of the five classes, and a combined variable 'label' for all classes.
  - ToS-100-cleaned-dataset-huggingface: Hugging Face dataset after oversampling, used for fine-tuning the pre-trained GPT-2 model. It is split into 80% training and 20% testing. More information on how to load the dataset into the Hugging Face library can be found [here](https://huggingface.co/docs/datasets/loading).

- Due to its size, please use [link](https://drive.google.com/drive/folders/1Iors--UYkz9BbJrslQHTUVts9PfRB22T?usp=sharing) to access the **Dataset for Text Summary Model**. It contains the ToS documents crawled from the ToS;DR website with highlighted sentences by human contributors for text highlighting model. More information about ToS;DR can be found [here](https://tosdr.org/).
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
