import re
import unicodedata

def remove_special_chars(text: str) -> str:
    """Удаляет специальные символы, кроме медицинских терминов."""
    text = re.sub(r"[^a-zA-Zа-яА-Я0-9.,()%-]", " ", text)  # Разрешаем точки, запятые, проценты и скобки
    text = re.sub(r"\s+", " ", text).strip()  # Убираем лишние пробелы
    return text

def normalize_unicode(text: str) -> str:
    """Приводит символы к нормальной Unicode-форме (например, 'ﬁ' → 'fi')."""
    return unicodedata.normalize("NFKC", text)

def clean_text(text: str) -> str:
    """Полная очистка текста."""
    text = normalize_unicode(text)
    text = remove_special_chars(text)
    return text

def read_file(file_path: str) -> str:
    """Читает файл с пробой разных кодировок."""
    encodings = ["utf-8", "cp1251", "ISO-8859-1"]
    
    for enc in encodings:
        try:
            with open(file_path, encoding=enc) as f:
                print(f"Файл успешно прочитан в кодировке: {enc}")
                return f.read()
        except UnicodeDecodeError:
            print(f"Не удалось открыть файл в кодировке: {enc}")    
    raise ValueError("Не удалось открыть файл с использованием доступных кодировок.")

def split_text_into_chunks(text: str, chunk_size: int = 300, chunk_overlap: int = 20):
    """Разбивает текст на чанки."""
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)