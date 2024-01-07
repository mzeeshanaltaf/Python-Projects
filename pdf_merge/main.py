# This program merges the pdf files in given folder.
# It has the following features:
#   * Search for pdf files in 'pdf_folder'
#   * Merge all the available pdf files into a single pdf file named as 'output_pdf'.
#   * Merged pdf file is stored in the same folder i.e. 'pdf_folder'

import PyPDF2
import os

merger = PyPDF2.PdfMerger()
pdf_folder = "./pdffiles"
output_pdf = "mergedPDF.pdf"

# List of pdffiles in provided folder
pdf_files = [os.path.join(pdf_folder, file) for file in os.listdir(pdf_folder) if file.endswith(".pdf")]

if not pdf_files:
    print("No PDF files found!")

else:
    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(f"{pdf_folder}/{output_pdf}")
    print(f"File has been merged in '{pdf_folder}' folder with name '{output_pdf}'.")
