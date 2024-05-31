from pdfminer.high_level import extract_text

text = extract_text("/app/PenaltyBoxIII-OperatingManual.pdf")
print(text)