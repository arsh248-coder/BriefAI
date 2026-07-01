import os
from pypdf import PdfReader
import docx

def list_documents(folder_path: str):
    home = os.path.expanduser("~")

    path_map = {
        "downloads": os.path.join(home, "Downloads"),
        "desktop": os.path.join(home, "OneDrive - McMaster University", "Desktop"),
        "documents": os.path.join(home, "Documents")
    }

    # 1. Determine which folders to check
    if folder_path.lower() == "all":
        folders_to_check = path_map.values()
    else:
        resolved = path_map.get(folder_path.lower(), None)
        if not resolved:
            raise Exception(f"Invalid folder: {folder_path}. Must be downloads, desktop, documents, or all.")
        folders_to_check = [resolved]

    files = []

    # 2. Iterate through the chosen folders
    for folder in folders_to_check:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                # Match both PDF and Word files
                if f.lower().endswith((".pdf", ".docx")):
                    files.append({
                        "name": f,
                        "path": os.path.join(folder, f)
                    })

    return files


def read_pdf(path: str):
    if not os.path.exists(path):
        raise Exception(f"File not found: {path}")

    reader = PdfReader(path)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    return {
        "path": path,
        "content": text[:8000]  # prevent token overflow
    }


def read_text_file(path: str):
    if not os.path.exists(path):
        raise Exception(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return {
            "path": path,
            "content": f.read()
        }


def read_word_file(file_path: str):
    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    full_text.append(cell.text)
        return {
            "path": file_path,
            "content": "\n".join(full_text)[:8000] # prevent token overflow
        }
    except Exception as e:
        return f"Error parsing Word file: {str(e)}"