


# import os
# from azure.ai.textanalytics import TextAnalyticsClient, ExtractiveSummaryAction
# from azure.core.credentials import AzureKeyCredential
# from PyPDF2 import PdfReader

# # Set your key and endpoint here
# key = 'fed5dbd18382414381b07dbd04af5b1d'
# endpoint = 'https://hipo.cognitiveservices.azure.com/'

# # Authenticate the client using your key and endpoint 
# def authenticate_client():
#     ta_credential = AzureKeyCredential(key)
#     text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
#     return text_analytics_client

# client = authenticate_client()

# def sample_extractive_summarization(client, document):
#     poller = client.begin_analyze_actions(
#         document,
#         actions=[ExtractiveSummaryAction(max_sentence_count=4)],
#     )

#     document_results = poller.result()
#     for result in document_results:
#         extract_summary_result = result[0] 
#         if extract_summary_result.is_error:
#             print(f"...Is an error with code '{extract_summary_result.code}' and message '{extract_summary_result.message}'")
#         else:
#             print("Summary extracted: \n{}".format(
#                 " ".join([sentence.text for sentence in extract_summary_result.sentences])
#             ))

# def read_pdf(file_path):
#     reader = PdfReader(file_path)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text()
#     return text

# # Path to your PDF file
# pdf_path = 'NGC Certificate-151.pdf'
# pdf_text = read_pdf(pdf_path)

# # Summarize the text extracted from the PDF
# sample_extractive_summarization(client, [pdf_text])


import os
from azure.ai.textanalytics import TextAnalyticsClient, ExtractiveSummaryAction
from azure.core.credentials import AzureKeyCredential
from PyPDF2 import PdfReader

# Set your key and endpoint here
key = 'fed5dbd18382414381b07dbd04af5b1d'
endpoint = 'https://hipo.cognitiveservices.azure.com/'

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def sample_extractive_summarization(client, document):
    poller = client.begin_analyze_actions(
        document,
        actions=[ExtractiveSummaryAction(max_sentence_count=4)],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0] 
        if extract_summary_result.is_error:
            print(f"...Is an error with code '{extract_summary_result.code}' and message '{extract_summary_result.message}'")
        else:
            print("Summary extracted: \n{}".format(
                " ".join([sentence.text for sentence in extract_summary_result.sentences])
            ))

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_relevant_sentences(text, keywords):
    sentences = text.split('.')
    relevant_sentences = [sentence for sentence in sentences if any(keyword in sentence for keyword in keywords)]
    return relevant_sentences

# Path to your PDF file
# pdf_path = 'NGC Certificate-151.pdf'
pdf_path = 'Saisreesatya_CV.pdf'
pdf_text = read_pdf(pdf_path)

# Keywords to search for
keywords = ["MediBot", "COE", "Work Ethic"]

# Extract relevant sentences containing the keywords
relevant_sentences = extract_relevant_sentences(pdf_text, keywords)
if relevant_sentences:
    print("Extracted relevant sentences:")
    for sentence in relevant_sentences:
        print(sentence)
    
    # Summarize the relevant sentences
    sample_extractive_summarization(client, [" ".join(relevant_sentences)])
else:
    print("No relevant sentences found.")
