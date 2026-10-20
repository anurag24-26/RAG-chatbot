def split_text(text, size=800, overlap=150):
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            cut = max(text.rfind("\n\n", start, end), text.rfind(". ", start, end))
            if cut > start + size // 2:
                end = cut + 1
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def build_chunks(documents, size=800, overlap=150):
    chunks = []
    for source, pages in documents.items():
        for page, text in pages:
            for piece in split_text(text, size, overlap):
                chunks.append({"source": source, "page": page, "text": piece})
    return chunks
