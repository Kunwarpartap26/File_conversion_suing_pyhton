import os
import pandas as pd
from PIL import Image
import zipfile, rarfile, py7zr
import pypandoc
import pdfplumber
from docx import Document
from pdf2docx import Converter


OUTPUT_DIR = os.path.join(os.getcwd(), "output")              # Always save in "output" folder
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert(input_path, output_format):
    filename, ext = os.path.splitext(input_path)
    ext = ext.lower()
    base_name = os.path.basename(filename)                   # keep only filename without path

   
    if ext == ".pdf" and output_format == "docx":                  # /-------------------- Documents --------------------/
        output_path = os.path.join(OUTPUT_DIR, base_name + ".docx")
        try:
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            return output_path
        except Exception as e:
            raise ValueError("Error converting PDF to DOCX: " + str(e))

    if ext == ".docx" and output_format == "pdf":
        output_path = os.path.join(OUTPUT_DIR, base_name + ".pdf")
        pypandoc.convert_file(input_path, "pdf", outputfile=output_path)
        return output_path

    if ext == ".txt" and output_format == "docx":
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        doc = Document()
        doc.add_paragraph(text)
        output_path = os.path.join(OUTPUT_DIR, base_name + ".docx")
        doc.save(output_path)
        return output_path

    if ext == ".txt" and output_format == "md":
        output_path = os.path.join(OUTPUT_DIR, base_name + ".md")
        pypandoc.convert_file(input_path, "markdown", outputfile=output_path)
        return output_path

    if ext == ".csv" and output_format == "xlsx":
        df = pd.read_csv(input_path)
        output_path = os.path.join(OUTPUT_DIR, base_name + ".xlsx")
        df.to_excel(output_path, index=False)
        return output_path

  
    if ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:              # -------------------- Images --------------------
        img = Image.open(input_path)
        output_path = os.path.join(OUTPUT_DIR, base_name + "." + output_format)
        img.save(output_path)
        return output_path

 
    if ext == ".zip" and output_format == "extract":                   # -------------------- Archives --------------------
        output_dir = os.path.join(OUTPUT_DIR, base_name + "_extracted")
        with zipfile.ZipFile(input_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)
        return output_dir

    if ext == ".rar" and output_format == "extract":
        output_dir = os.path.join(OUTPUT_DIR, base_name + "_extracted")
        with rarfile.RarFile(input_path) as rf:
            rf.extractall(output_dir)
        return output_dir

    if ext == ".7z" and output_format == "extract":
        output_dir = os.path.join(OUTPUT_DIR, base_name + "_extracted")
        with py7zr.SevenZipFile(input_path, mode="r") as z:
            z.extractall(path=output_dir)
        return output_dir


    raise ValueError("Unsupported conversion: {} → {}".format(ext, output_format))
