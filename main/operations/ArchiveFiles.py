import os

import PyPDF2

from main.operations.FileUtilities import FileUtilities
from main.operations.UploadFile import UploadFile
import pdf2image
import zipfile


class ArchiveFiles:

    @classmethod
    def archive(cls, files):
        archives = []
        for file in files:
            actual_name = file['actual_filename']
            user_name = file['user_filename']
            pdf_reader = PyPDF2.PdfFileReader("storage/" + actual_name)
            archive_filename = cls.create_archive(user_name, actual_name)
            archives.append(archive_filename)
        return archives

    @classmethod
    def create_archive(cls, document_filename, actual_filename):
        document_filename = FileUtilities.remove_extension(document_filename)
        archive_filename = FileUtilities.generate_tmp_name("archive_" + document_filename + "_", ".zip")
        archive = zipfile.ZipFile("storage/" + archive_filename, 'w')
        images = pdf2image.convert_from_path("storage/"+actual_filename)
        page_iteration = 1
        for image in images:
            image_filename = document_filename +" страница "+str(page_iteration)+".jpg"
            image.save("storage/"+image_filename)
            archive.write("storage/" + image_filename, image_filename)
            page_iteration += 1

        """
        for i in range(pdf_reader.numPages):
            filename = UploadFile.convert_page_to_image(pdf_reader.getPage(i))
            archive.write("storage/"+filename, filename)
        """
        return archive_filename

    @classmethod
    def flush_image(cls, filename):
        os.remove("storage/" + filename)
