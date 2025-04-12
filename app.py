import streamlit as st
import os
from pathlib import Path
from typing import List
import mimetypes
from markitdown import MarkItDown


# Icone associate ai formati supportati
FORMAT_ICONS = {
    '.pdf': '📄',
    '.docx': '📝',
    '.pptx': '📊',
    '.xlsx': '📈',
    '.xls': '📈',
    '.html': '🌐',
    '.csv': '📑',
    '.json': '🧾',
    '.xml': '🗂️',
    '.jpg': '🖼️',
    '.jpeg': '🖼️',
    '.png': '🖼️',
    '.mp3': '🎵',
    '.wav': '🎶',
    '.zip': '🗜️',
    '.epub': '📚',
    '.txt': '📄'
}

st.title("🛠️ MarkItDown File Converter")

uploaded_files = st.file_uploader("Carica uno o più file", type=None, accept_multiple_files=True)

directory_path = st.text_input("Oppure inserisci un percorso locale per caricare tutti i file nella cartella")

loaded_files = []

# Caricamento da file uploader
if uploaded_files:
    for file in uploaded_files:
        loaded_files.append((file.name, file, os.path.splitext(file.name)[1]))

# Caricamento da directory locale
if directory_path:
    dir_path = Path(directory_path)
    if dir_path.exists() and dir_path.is_dir():
        for file_path in dir_path.iterdir():
            if file_path.is_file():
                ext = file_path.suffix.lower()
                loaded_files.append((file_path.name, file_path, ext))

if loaded_files:
    st.subheader("📂 File Caricati")
    selected_files = []
    for i, (name, file_obj, ext) in enumerate(loaded_files):
        icon = FORMAT_ICONS.get(ext, '📁')
        selected = st.checkbox(f"{icon} {name}", key=i)
        if selected:
            selected_files.append((name, file_obj, ext))

    if st.button("▶️ Elabora") and selected_files:
        st.subheader("📄 Risultati Conversione")
        markdown_converter = MarkItDown()
        for name, file_obj, ext in selected_files:
            st.markdown(f"**{name}**")
            try:
                if hasattr(file_obj, 'read'):  # UploadedFile
                    result = markdown_converter.convert_stream(file_obj)
                else:  # FilePath
                    with open(file_obj, 'rb') as f:
                        result = markdown_converter.convert_stream(f)
                st.code(result.text_content, language='markdown')
            except Exception as e:
                st.error(f"Errore nella conversione di {name}: {e}")
else:
    st.info("Carica dei file o inserisci un percorso per iniziare.")
