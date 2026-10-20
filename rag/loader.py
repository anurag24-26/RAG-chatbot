from pypdf import PdfReader


class DocumentError(Exception):
    pass


def load_file(uploaded):
    name = uploaded.name
    ext = name.lower().rsplit(".", 1)[-1] if "." in name else ""

    if ext == "txt":
        text = uploaded.getvalue().decode("utf-8", errors="ignore")
        pages = [(1, text)]
    elif ext == "pdf":
        try:
            reader = PdfReader(uploaded)
            pages = [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
        except Exception as exc:
            raise DocumentError(f"{name} could not be read. It may be corrupted or password protected.") from exc
    else:
        raise DocumentError(f"{name} is not supported. Upload PDF or TXT files only.")

    pages = [(number, text.strip()) for number, text in pages if text.strip()]
    if not pages:
        raise DocumentError(f"{name} has no extractable text. Scanned PDFs need OCR first.")
    return pages
