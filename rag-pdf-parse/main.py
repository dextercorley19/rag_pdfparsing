from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import nltk
import re
from openai import OpenAI
import os

output_string = StringIO()
with open('/app/PenaltyBoxIII-OperatingManual.pdf', 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(),
                       output_type='text', codec=None) #can be 'html', 'xml', 'text', 'tag'
    
# Get the extracted text
extracted_text = output_string.getvalue()

# tokenize the text
tokens = nltk.word_tokenize(extracted_text)

def group_words(words, group_size=100):
    grouped_words = {}
    group = []
    key_counter = 1
    word_count = 0

    for word in words:
        group.append(word)
        word_count += 1

        # Check if we have reached the group size or if the word ends with a period
        if word_count >= group_size and word.endswith('.'):
            # Join the words in the group with a space and add to the dictionary
            grouped_words[f"group_{key_counter}"] = " ".join(group)
            key_counter += 1
            group = []
            word_count = 0
    
    # Add any remaining words as the last group
    if group:
        grouped_words[f"group_{key_counter}"] = " ".join(group)
    
    return grouped_words

grouped_dict = group_words(tokens)

def clean_text(text):
    # Remove multiple periods and other special characters
    text = re.sub(r'\.{2,}', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\s+([,.?!:;)’”])', r'\1', text)    
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r"‘ ", "'", text)
    text = re.sub(r'“ ', '“', text)

# Strip leading and trailing whitespace

    text = text.strip()
    return text

def clean_groups(grouped_dict):
    cleaned_dict = {}
    for key, value in grouped_dict.items():
        cleaned_dict[key] = clean_text(value)
    return cleaned_dict

cleaned_dict = clean_groups(grouped_dict)

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI()

group_num = client.embeddings.create(
  model="text-embedding-ada-002",
  input=cleaned_dict['group_86'],
  encoding_format="float"
)
print(group_num)