import PyPDF2
from django.core.files.storage import FileSystemStorage
from PyPDF2 import *
import pdf2image
import json
import random

from main.operations.FileUtilities import FileUtilities


class UploadFile:
    @staticmethod
    def save_PDF(file, session):
        if file is None:
            return
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        pdf_file = PyPDF2.PdfFileReader(file)
        first_page = pdf_file.getPage(0)
        image = UploadFile.convert_page_to_image(first_page)
        current_state_string = session.get("files")
        if current_state_string is None:
            current_state_string = "[]"
        current_state = json.loads(current_state_string)
        current_state.append({
            "actual_filename": filename,
            "user_filename": file.name,
            "image": image,
            "pages_number": UploadFile.count_pages(pdf_file)
        })
        return current_state

    @staticmethod
    def convert_page_to_image(page):
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(page)
        pdf_tmp_filename = FileUtilities.generate_tmp_name("pdf_first_page_", ".pdf")
        FileUtilities.write_pdf(pdf_tmp_filename, pdf_writer)
        image = pdf2image.convert_from_path("storage/"+pdf_tmp_filename)
        filename = FileUtilities.generate_tmp_name('cover_', ".jpg")
        image[0].save("storage/"+filename, 'JPEG')
        return filename

    @staticmethod
    def count_pages(pdf_reader):
        return pdf_reader.numPages
