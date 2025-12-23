import textract
from multiprocessing import Pool

def _extract_text(file_path):
    """
    Extracts text from a document in a separate process.
    """
    try:
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        print(f"Error reading document: {e}")
        return ""

def read_document(file_path):
    """
    Reads the content of a document using a separate process.
    """
    with Pool(1) as p:
        text = p.apply(_extract_text, (file_path,))
    return text
