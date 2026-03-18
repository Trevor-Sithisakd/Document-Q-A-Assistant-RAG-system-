def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def chunk_pages(pages: list[dict], source: str, chunk_size: int, overlap: int) -> list[dict]:
    all_chunks = []

    for page_data in pages:
        page_num = page_data["page"]
        text = page_data["text"]

        page_chunks = chunk_text(text, chunk_size, overlap)

        for idx, chunk in enumerate(page_chunks):
            all_chunks.append({
                "chunk_id": f"{source}_p{page_num}_c{idx}",
                "source": source,
                "page": page_num,
                "text": chunk
            })

    return all_chunks