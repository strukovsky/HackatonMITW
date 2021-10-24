import PyPDF2

from main.operations.FileUtilities import FileUtilities


class SplitFiles:
    def __init__(self):
        self.filenames = []

    def split(self, files):
        for file in files:
            actual_filename = file['actual_filename']
            user_filename = file['user_filename']
            self.split_one_file(actual_filename, user_filename)
        return self.filenames

    def split_one_file(self, filename, user_filename):
        pdf_file = PyPDF2.PdfFileReader("storage/"+filename)
        for i in range(pdf_file.numPages):
            page = pdf_file.getPage(i)
            self.write_one_page(page, i + 1, user_filename)

    def write_one_page(self, page, page_num, filename):
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(page)
        filename = FileUtilities.remove_extension(filename)
        resulting_filename = filename
        resulting_filename += " страница "
        resulting_filename += str(page_num)
        resulting_filename += ".pdf"
        self.filenames.append(resulting_filename)
        FileUtilities.write_pdf(resulting_filename, pdf_writer)
