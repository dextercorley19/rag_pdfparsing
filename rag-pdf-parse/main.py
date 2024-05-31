from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import nltk


output_string = StringIO()
with open('/app/PenaltyBoxIII-OperatingManual.pdf', 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(),
                       output_type='text', codec=None) #can be 'html', 'xml', 'text', 'tag'
    
# Get the extracted text
extracted_text = output_string.getvalue()

# Tokenize the text into sentences
sentences = nltk.sent_tokenize(extracted_text)

# Print sentences
sentence_to_start_at = 40
sentence_to_end_at = 50
for sentence in sentences[sentence_to_start_at:sentence_to_end_at]:
    print(sentence)