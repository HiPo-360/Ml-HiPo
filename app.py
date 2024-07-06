from flask import Flask, request, jsonify
from azure.ai.textanalytics import TextAnalyticsClient, ExtractiveSummaryAction
from azure.core.credentials import AzureKeyCredential
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

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
    summary = ""
    for result in document_results:
        extract_summary_result = result[0] 
        if extract_summary_result.is_error:
            return f"...Is an error with code '{extract_summary_result.code}' and message '{extract_summary_result.message}'"
        else:
            summary = " ".join([sentence.text for sentence in extract_summary_result.sentences])
    return summary

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_relevant_sentences(text, keywords):
    sentences = text.split('.')
    relevant_sentences = [sentence for sentence in sentences if any(keyword in sentence for keyword in keywords)]
    return relevant_sentences

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        pdf_text = read_pdf(file)
        keywords = ["MediBot", "COE", "Work Ethic"]  # Hardcoded keywords
        relevant_sentences = extract_relevant_sentences(pdf_text, keywords)
        if relevant_sentences:
            summary = sample_extractive_summarization(client, [" ".join(relevant_sentences)])
            return jsonify({"summary": summary})
        else:
            return jsonify({"error": "No relevant sentences found"})
    return jsonify({"error": "Unknown error"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
